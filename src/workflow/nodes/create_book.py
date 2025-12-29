"""
책 생성 노드.

책과 전체 챕터/섹션 구조를 DB에 저장.
"""
from src.workflow.state import PipelineState
from src.db.connection import get_session
from src.db.operations import (
    create_book,
    get_book_by_title,
    create_chapter_from_llm,
    save_all_sections_recursive,
    reset_chapter_counter,
)
from src.utils.pdf.hierarchy_detector import get_leaf_sections


def create_book_node(state: PipelineState) -> PipelineState:
    """
    책과 전체 구조를 DB에 저장.

    1. Book 레코드 생성
    2. 모든 Chapter 저장
    3. 모든 Section 재귀 저장
    4. all_sections에 chapter_id, section_id 매핑

    Args:
        state: PipelineState (chapters, metadata 필수)

    Returns:
        업데이트된 PipelineState:
        - book_id: 생성된 책 ID
        - all_sections: chapter_id, section_id가 설정된 섹션 리스트
    """
    chapters = state.get("chapters", [])
    metadata = state.get("metadata", {})
    pdf_path = state.get("pdf_path", "")

    if not chapters:
        return {
            **state,
            "error": "저장할 챕터가 없습니다.",
        }

    # 제목/저자 추출
    title = metadata.get("title") or pdf_path.split("/")[-1].replace(".pdf", "")
    author = metadata.get("author") or "Unknown"

    try:
        session = get_session()

        try:
            # 중복 체크
            existing = get_book_by_title(session, title)
            if existing:
                return {
                    **state,
                    "error": f"'{title}' 책이 이미 존재합니다 (ID: {existing.id})",
                }

            # 챕터 카운터 초기화
            reset_chapter_counter()

            # 책 생성
            book = create_book(
                session,
                title=title,
                author=author,
                source_path=pdf_path,
            )
            print(f"✅ 책 생성: '{title}' (ID: {book.id})")

            # 모든 챕터와 섹션 저장, section_id 매핑 수집
            all_section_id_maps = {}  # {chapter_title: {section_title: section_id}}

            for chapter in chapters:
                # 챕터 저장
                db_chapter = create_chapter_from_llm(
                    session=session,
                    book_id=book.id,
                    chapter=chapter,
                )

                # 섹션 재귀 저장
                section_id_map = save_all_sections_recursive(
                    session=session,
                    chapter_id=db_chapter.id,
                    book_id=book.id,
                    sections=chapter.sections,
                )

                all_section_id_maps[chapter.title] = {
                    "chapter_id": db_chapter.id,
                    "section_map": section_id_map,
                }

            session.commit()

            # all_sections에 chapter_id, section_id 매핑
            all_sections = state.get("all_sections", [])
            updated_sections = []

            for section_info in all_sections:
                chapter = section_info["chapter"]
                section = section_info["section"]

                chapter_data = all_section_id_maps.get(chapter.title, {})
                chapter_id = chapter_data.get("chapter_id")
                section_map = chapter_data.get("section_map", {})
                section_id = section_map.get(section.title)

                updated_sections.append({
                    **section_info,
                    "chapter_id": chapter_id,
                    "section_id": section_id,
                })

            print(f"   → {len(chapters)}개 챕터, {len(updated_sections)}개 섹션 저장됨")

            return {
                **state,
                "book_id": book.id,
                "all_sections": updated_sections,
            }

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    except Exception as e:
        return {
            **state,
            "error": f"책 생성 실패: {str(e)}",
        }
