"""
문단 분할 노드.

섹션 텍스트를 의미 있는 문단 단위로 분할.
LLM 기반 의미적 청킹 사용.
"""

from src.workflow.state import PipelineState
from src.model.schemas import HierarchicalChunk, DetectedSection
from src.utils.pdf.hierarchy_detector import split_into_paragraphs


def chunk_paragraphs(state: PipelineState) -> PipelineState:
    """
    현재 섹션을 문단으로 분할.

    LLM 기반 계층 구조 처리:
    - current_section_text: 현재 섹션의 본문 텍스트
    - current_section: DetectedSection 객체
    - hierarchy_path: 계층 경로 문자열

    Args:
        state: PipelineState (current_section_text 필수)

    Returns:
        업데이트된 PipelineState (chunks 추가)
    """
    section_text = state.get("current_section_text")
    chapter_id = state.get("current_chapter_id")
    book_id = state.get("book_id")
    hierarchy_path = state.get("hierarchy_path", "")

    # 현재 섹션 정보 (LLM 감지 기반)
    current_section = state.get("current_section")
    section_title = None
    section_level = 2

    if current_section:
        if isinstance(current_section, DetectedSection):
            section_title = current_section.title
            section_level = current_section.level
        elif hasattr(current_section, "title"):
            section_title = current_section.title

    # 챕터 제목 (상위 컨텍스트)
    current_chapter = state.get("current_chapter")
    chapter_title = None
    if current_chapter:
        if isinstance(current_chapter, str):
            chapter_title = current_chapter
        elif hasattr(current_chapter, "title"):
            chapter_title = current_chapter.title

    if not section_text:
        return {**state, "chunks": [], "error": "section text is required"}

    try:
        # LLM 기반 문단 분할
        paragraphs = split_into_paragraphs(
            text=section_text,
            section_title=section_title,
        )

        # HierarchicalChunk 리스트 생성
        chunks = []
        for i, para in enumerate(paragraphs):
            chunk = HierarchicalChunk(
                text=para["text"],
                chapter_id=chapter_id,
                chapter_title=chapter_title,
                section_title=section_title,
                paragraph_index=i,
                chapter_paragraph_index=i,
                start_char=para.get("start_char", 0),
                end_char=para.get("end_char", 0),
                section_level=section_level,
                detection_method="llm",
                hierarchy_path=hierarchy_path,
            )
            chunks.append(chunk)

        return {
            **state,
            "chunks": chunks,
            "current_chunk_index": 0,
        }

    except Exception as e:
        # LLM 실패 시 폴백: 규칙 기반 분할
        chunks = _simple_split(
            text=section_text,
            chapter_id=chapter_id,
            chapter_title=chapter_title,
            section_title=section_title,
            hierarchy_path=hierarchy_path,
        )

        return {
            **state,
            "chunks": chunks,
            "current_chunk_index": 0,
        }


def _simple_split(
    text: str,
    chapter_id: int = None,
    chapter_title: str = None,
    section_title: str = None,
    hierarchy_path: str = "",
    min_length: int = 100,
    max_length: int = 1500,
) -> list[HierarchicalChunk]:
    """
    간단한 규칙 기반 텍스트 분할 (폴백용).

    Args:
        text: 분할할 텍스트
        chapter_id: 챕터 ID
        chapter_title: 챕터 제목
        section_title: 섹션 제목
        hierarchy_path: 계층 경로
        min_length: 최소 청크 길이
        max_length: 최대 청크 길이

    Returns:
        HierarchicalChunk 리스트
    """
    # 더블 뉴라인으로 분할
    raw_chunks = text.split("\n\n")
    chunks = []
    current_chunk = ""
    paragraph_index = 0
    char_offset = 0

    for raw in raw_chunks:
        raw = raw.strip()
        if not raw:
            continue

        # 현재 청크에 추가
        if current_chunk:
            current_chunk += "\n\n" + raw
        else:
            current_chunk = raw

        # 최대 길이 도달 시 청크 생성
        if len(current_chunk) >= max_length:
            if len(current_chunk) >= min_length:
                chunks.append(HierarchicalChunk(
                    text=current_chunk,
                    chapter_id=chapter_id,
                    chapter_title=chapter_title,
                    section_title=section_title,
                    paragraph_index=paragraph_index,
                    chapter_paragraph_index=paragraph_index,
                    start_char=char_offset,
                    end_char=char_offset + len(current_chunk),
                    detection_method="fallback",
                    hierarchy_path=hierarchy_path,
                ))
                char_offset += len(current_chunk)
                paragraph_index += 1
            current_chunk = ""

    # 남은 텍스트 처리
    if current_chunk and len(current_chunk) >= min_length:
        chunks.append(HierarchicalChunk(
            text=current_chunk,
            chapter_id=chapter_id,
            chapter_title=chapter_title,
            section_title=section_title,
            paragraph_index=paragraph_index,
            chapter_paragraph_index=paragraph_index,
            start_char=char_offset,
            end_char=char_offset + len(current_chunk),
            detection_method="fallback",
            hierarchy_path=hierarchy_path,
        ))

    return chunks
