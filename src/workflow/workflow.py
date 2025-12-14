"""
LangGraph 워크플로우 정의.

PDF → TOC 기반 챕터/섹션 감지 → 문단 분할 → 아이디어 추출
"""
from typing import Optional
from tqdm import tqdm
from langgraph.graph import StateGraph, END

from src.workflow.state import PipelineState, create_initial_state
from src.workflow.nodes import (
    extract_text,
    chunk_paragraphs,
    extract_idea,
    check_duplicate,
    save_to_db,
)
from src.model.schemas import DetectedChapter, DetectedSection
from src.utils.pdf.hierarchy_detector import (
    detect_chapters_from_toc,
    build_hierarchy_path,
    get_leaf_sections,
)

from src.db.connection import get_session
from src.db.models import Book
from src.db.operations import (
    create_book,
    get_book_by_title,
    create_chapter_from_llm,
    save_all_sections_recursive,
    reset_chapter_counter,
)


# ============================================================
# 아이디어 추출 그래프 (중복 체크 포함)
# ============================================================

def _route_after_duplicate_check(state: PipelineState) -> str:
    """중복 체크 후 라우팅."""
    is_duplicate = state.get("is_duplicate", False)
    return "skip" if is_duplicate else "save"


def _skip_duplicate(state: PipelineState) -> PipelineState:
    """중복 스킵 (no-op)."""
    return state


def create_idea_extraction_graph() -> StateGraph:
    """
    아이디어 추출 그래프 생성.

    워크플로우:
    ```
    [extract_idea]
         │
         ▼
    [check_duplicate]
         │
         ├── (중복) ──→ [skip] ──→ END
         │
         └── (신규) ──→ [save] ──→ END
    ```
    """
    workflow = StateGraph(PipelineState)

    workflow.add_node("extract", extract_idea)
    workflow.add_node("check_dup", check_duplicate)
    workflow.add_node("save", save_to_db)
    workflow.add_node("skip", _skip_duplicate)

    workflow.set_entry_point("extract")
    workflow.add_edge("extract", "check_dup")

    workflow.add_conditional_edges(
        "check_dup",
        _route_after_duplicate_check,
        {"skip": "skip", "save": "save"}
    )

    workflow.add_edge("save", END)
    workflow.add_edge("skip", END)

    return workflow.compile()


# 컴파일된 그래프 인스턴스
idea_extraction_graph = create_idea_extraction_graph()


# ============================================================
# PDF 파이프라인 실행 (TOC 기반)
# ============================================================

def run_pdf_pipeline(
    pdf_path: str,
    resume: bool = False,
    book_id: Optional[int] = None,
    model_version: str = "gemini-2.5-flash",
) -> dict:
    """
    PDF 파이프라인 실행 (TOC 기반).

    1. PDF → Plain Text + TOC 추출 (pymupdf)
    2. TOC 기반 챕터/섹션 구조 생성 (LLM 불필요)
    3. 말단 섹션별 문단 분할 및 아이디어 추출 (LLM 사용)
    """
    session = get_session()

    try:
        # Step 1: 초기 상태 생성 및 텍스트/TOC 추출
        initial_state = create_initial_state(
            pdf_path=pdf_path,
            book_id=book_id,
            resume=resume,
            model_version=model_version,
        )

        print("📄 PDF → Plain Text + TOC 추출 중...")
        state = extract_text(initial_state)

        if state.get("error"):
            return {"error": state["error"]}

        plain_text = state.get("plain_text", "")
        toc = state.get("toc", [])
        has_toc = state.get("has_toc", False)
        page_positions = state.get("page_positions", [])

        print(f"   → {len(plain_text):,} 문자 추출됨")
        print(f"   → TOC 항목: {len(toc)}개 {'✅' if has_toc else '❌ (TOC 없음)'}")

        # Step 2: TOC 기반 챕터/섹션 구조 생성
        if not has_toc:
            return {"error": "PDF에 TOC가 없습니다. TOC가 있는 PDF만 지원됩니다."}

        print("🔍 TOC 기반 챕터/섹션 감지 중...")
        chapters = detect_chapters_from_toc(
            pdf_path=pdf_path,
            plain_text=plain_text,
            page_positions=page_positions,
        )
        print(f"   → {len(chapters)}개 챕터 감지됨")

        # 섹션 수 출력
        for chapter in chapters:
            section_count = _count_sections(chapter.sections)
            print(f"   # {chapter.title} ({section_count} sections)")

        state["chapters"] = chapters

        # Step 3: DB에 책 생성
        book = _create_book(session, state)
        state["book_id"] = book.id

        # Step 4: 챕터/섹션별 처리
        stats = _process_toc_chapters(
            session=session,
            state=state,
            book=book,
            chapters=chapters,
        )

        _print_summary(stats)
        return stats

    finally:
        session.close()


def _count_sections(sections: list[DetectedSection]) -> int:
    """섹션 수 재귀 카운트."""
    count = len(sections)
    for section in sections:
        count += _count_sections(section.children)
    return count


def _create_book(session, state: PipelineState) -> Book:
    """책 생성."""
    metadata = state.get("metadata", {})
    pdf_path = state.get("pdf_path", "")

    title = metadata.get("title") or pdf_path.split("/")[-1].replace(".pdf", "")
    author = metadata.get("author") or "Unknown"

    existing = get_book_by_title(session, title)
    if existing:
        print(f"⚠️  '{title}' 이미 존재 (ID: {existing.id})")
        raise ValueError("책이 이미 존재함")

    # 챕터 카운터 초기화
    reset_chapter_counter()

    book = create_book(
        session,
        title=title,
        author=author,
        source_path=pdf_path,
    )
    print(f"✅ 책 생성 완료: '{title}' (ID: {book.id})")

    return book


def _process_toc_chapters(
    session,
    state: PipelineState,
    book: Book,
    chapters: list[DetectedChapter],
) -> dict:
    """TOC 기반 챕터/섹션 처리."""
    stats = {
        "total_chapters": len(chapters),
        "total_sections": 0,
        "completed_chapters": 0,
        "failed_chapters": 0,
        "total_paragraphs": 0,
        "total_ideas": 0,
        "duplicates_skipped": 0,
        "detection_method": "toc",
    }

    for chapter in tqdm(chapters, desc="📖 챕터 처리"):
        try:
            # DB에 챕터 저장
            db_chapter = create_chapter_from_llm(
                session=session,
                book_id=book.id,
                chapter=chapter,
            )

            # 모든 섹션을 재귀적으로 DB에 먼저 저장
            section_id_map = save_all_sections_recursive(
                session=session,
                chapter_id=db_chapter.id,
                book_id=book.id,
                sections=chapter.sections,
            )

            # 말단 섹션만 처리 (문단 분할 + 아이디어 추출)
            leaf_sections = get_leaf_sections(chapter)
            stats["total_sections"] += len(leaf_sections)

            for section, hierarchy_path in leaf_sections:
                # section_id_map에서 ID 조회 (이미 저장됨)
                section_id = section_id_map.get(section.title)

                _process_section(
                    state=state,
                    book=book,
                    db_chapter=db_chapter,
                    chapter=chapter,
                    section=section,
                    hierarchy_path=hierarchy_path,
                    section_id=section_id,
                    stats=stats,
                )

            stats["completed_chapters"] += 1

        except Exception as e:
            stats["failed_chapters"] += 1
            print(f"\n❌ 챕터 '{chapter.title}' 실패: {e}")

    return stats


def _process_section(
    state: PipelineState,
    book: Book,
    db_chapter,
    chapter: DetectedChapter,
    section: DetectedSection,
    hierarchy_path: str,
    section_id: Optional[int],
    stats: dict,
) -> None:
    """섹션 처리: 청킹 → 아이디어 추출."""
    section_text = section.content

    if len(section_text.strip()) < 100:
        return

    # 섹션은 이미 save_all_sections_recursive()에서 저장됨
    # section_id를 파라미터로 받아서 사용

    # 섹션 상태 생성
    section_state = {
        **state,
        "current_chapter": chapter,
        "current_section": section,
        "current_section_text": section_text,
        "current_chapter_id": db_chapter.id,
        "current_section_id": section_id,
        "hierarchy_path": hierarchy_path,
        "book_id": book.id,
    }

    # 청킹 수행 (LLM 기반 문단 분할)
    section_state = chunk_paragraphs(section_state)
    chunks = section_state.get("chunks", [])
    stats["total_paragraphs"] += len(chunks)

    # 각 청크에 대해 아이디어 추출
    for chunk in chunks:
        # 청크에 section_id 설정
        chunk.section_id = section_id

        chunk_state = {
            **section_state,
            "current_chunk": chunk,
        }

        # 아이디어 추출 그래프 실행
        result_state = idea_extraction_graph.invoke(chunk_state)

        if result_state.get("extracted_idea") and not result_state.get("is_duplicate"):
            stats["total_ideas"] += 1
        if result_state.get("is_duplicate"):
            stats["duplicates_skipped"] += 1


def _print_summary(stats: dict) -> None:
    """처리 요약 출력."""
    print("\n" + "=" * 60)
    print("📊 처리 요약")
    print("=" * 60)
    print(f"감지 방법: {stats.get('detection_method', 'toc')}")
    print(f"총 챕터: {stats.get('total_chapters', 0)}")
    print(f"총 섹션: {stats.get('total_sections', 0)}")
    print(f"완료: {stats.get('completed_chapters', 0)}")
    print(f"실패: {stats.get('failed_chapters', 0)}")
    print(f"총 문단: {stats.get('total_paragraphs', 0)}")
    print(f"추출된 아이디어: {stats.get('total_ideas', 0)}")
    print(f"중복 스킵: {stats.get('duplicates_skipped', 0)}")
    print("=" * 60)
