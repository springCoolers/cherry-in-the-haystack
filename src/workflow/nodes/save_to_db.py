"""
데이터베이스 저장 노드.

추출된 아이디어와 청크를 DB에 저장.
"""

from src.workflow.state import PipelineState
from src.db.connection import get_session
from src.db.models import ParagraphChunk as DBParagraphChunk, KeyIdea, Section


def save_to_db(state: PipelineState) -> PipelineState:
    """
    데이터베이스에 저장.

    - ParagraphChunk 저장
    - KeyIdea 저장
    - Section 저장 (필요시)

    Args:
        state: PipelineState (extracted_idea, book_id, current_chunk 필수)

    Returns:
        업데이트된 PipelineState (saved_chunk_id 추가)
    """
    extracted_idea = state.get("extracted_idea")
    book_id = state.get("book_id")
    current_chunk = state.get("current_chunk")
    is_duplicate = state.get("is_duplicate", False)

    # 중복이면 저장하지 않음
    if is_duplicate:
        return state

    # 추출된 아이디어가 없으면 저장하지 않음
    if not extracted_idea:
        return state

    # book_id 필수
    if not book_id:
        return {**state, "error": "book_id is required for database save"}

    try:
        session = get_session()

        try:
            # 청크 정보 추출
            if hasattr(current_chunk, "text"):
                body_text = current_chunk.text
                paragraph_index = getattr(current_chunk, "paragraph_index", 0)
                chapter_id = getattr(current_chunk, "chapter_id", None)
                chapter_paragraph_index = getattr(current_chunk, "chapter_paragraph_index", None)
                section_title = getattr(current_chunk, "section_title", None)
            elif isinstance(current_chunk, dict):
                body_text = current_chunk.get("text") or current_chunk.get("body_text", "")
                paragraph_index = current_chunk.get("paragraph_index", 0)
                chapter_id = current_chunk.get("chapter_id")
                chapter_paragraph_index = current_chunk.get("chapter_paragraph_index")
                section_title = current_chunk.get("section_title")
            else:
                body_text = str(current_chunk)
                paragraph_index = 0
                chapter_id = None
                chapter_paragraph_index = None
                section_title = None

            # 섹션 ID 처리 (section_title이 있으면 Section 생성/조회)
            section_id = None
            if section_title and chapter_id:
                section_id = _get_or_create_section(session, chapter_id, section_title)

            # 1. ParagraphChunk 저장
            db_chunk = DBParagraphChunk(
                book_id=book_id,
                chapter_id=chapter_id,
                section_id=section_id,
                paragraph_index=paragraph_index,
                chapter_paragraph_index=chapter_paragraph_index,
                body_text=body_text,
                paragraph_hash=getattr(current_chunk, "paragraph_hash",None),
                simhash64=getattr(current_chunk, "simhash64, None"),
            )
            session.add(db_chunk)
            session.flush()  # Get ID without committing

            # 2. KeyIdea 저장
            # concept 추출
            if hasattr(extracted_idea, "concept"):
                concept = extracted_idea.concept
            elif isinstance(extracted_idea, dict):
                concept = extracted_idea.get("concept", "")
            else:
                concept = str(extracted_idea)

            db_idea = KeyIdea(
                chunk_id=db_chunk.id,
                book_id=book_id,
                core_idea_text=concept,
            )
            session.add(db_idea)
            session.commit()

            return {
                **state,
                "saved_chunk_id": db_chunk.id,
            }

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    except Exception as e:
        return {**state, "error": f"Database save failed: {str(e)}"}


def _get_or_create_section(session, chapter_id: int, section_title: str) -> int:
    """
    섹션 조회 또는 생성.

    Args:
        session: DB 세션
        chapter_id: 챕터 ID
        section_title: 섹션 제목

    Returns:
        섹션 ID
    """
    # 기존 섹션 조회
    existing = session.query(Section).filter(
        Section.chapter_id == chapter_id,
        Section.title == section_title
    ).first()

    if existing:
        return existing.id

    # 새 섹션 생성
    # 섹션 순서 계산
    max_order = session.query(Section).filter(
        Section.chapter_id == chapter_id
    ).count()

    new_section = Section(
        chapter_id=chapter_id,
        title=section_title,
        section_order=max_order + 1,
    )
    session.add(new_section)
    session.flush()

    return new_section.id
