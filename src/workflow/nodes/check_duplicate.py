from src.workflow.state import PipelineState
from src.db.connection import get_session
from src.db.models import KeyIdea
from src.dedup.dedup_service import DeduplicationService


def check_chunk_duplicate(state: PipelineState) -> PipelineState:
    """청크 레벨 중복 체크 (해시 + 선택적 임베딩).

    1단계: 해시 체크 (SHA256 + SimHash) - 빠름, 무료
    2단계: 임베딩 체크 (enable_semantic_dedup=True 시) - 의미적 유사도

    해시가 놓친 의미적 중복을 임베딩으로 추가 탐지합니다.
    """
    current_chunk = state.get("current_chunk")
    book_id = state.get("book_id")
    enable_semantic = state.get("enable_semantic_dedup", False)
    semantic_threshold = state.get("semantic_threshold", 0.95)

    if not current_chunk:
        return {**state, "is_chunk_duplicate": False}

    text = current_chunk.text if hasattr(current_chunk, 'text') else current_chunk.get('text', '')

    session = get_session()
    try:
        # 1단계: 해시 체크 (빠름)
        dedup_service = DeduplicationService(
            session=session,
            fuzzy_threshold=6,
            semantic_threshold=semantic_threshold,
            enable_semantic=False,  # 해시만 먼저
        )
        result = dedup_service.check_duplicate(text, book_id=book_id)

        if result.is_duplicate:
            stats = state.get("stats", {})
            stats["chunk_duplicates_skipped"] = stats.get("chunk_duplicates_skipped", 0) + 1
            return {
                **state,
                "is_chunk_duplicate": True,
                "chunk_duplicate_type": result.duplicate_type,
                "stats": stats,
            }

        # 2단계: 임베딩 체크 (활성화 시에만)
        if enable_semantic:
            semantic_result = dedup_service.find_semantic_duplicate(
                text, book_id=book_id, cross_book=True
            )
            if semantic_result:
                stats = state.get("stats", {})
                stats["semantic_duplicates_skipped"] = stats.get("semantic_duplicates_skipped", 0) + 1
                return {
                    **state,
                    "is_chunk_duplicate": True,
                    "chunk_duplicate_type": "semantic",
                    "similarity_score": semantic_result[1],
                    "stats": stats,
                }

        return {**state, "is_chunk_duplicate": False}
    finally:
        session.close()

def check_idea_duplicate(state: PipelineState) -> PipelineState:
    """아이디어 레벨 concept 중복 체크"""
    #기존 check_duplicate 로직과 동일, 단 변환 키가 is_idea_duplicate
    extracted_idea = state.get("extracted_idea")
    book_id = state.get("book_id")

    if not extracted_idea:
        return {**state, "is_idea_duplicate": False}

    if hasattr(extracted_idea, "concept"):
        concept = extracted_idea.concept
    elif isinstance(extracted_idea, dict):
        concept = extracted_idea.get("concept","")
    else:
        concept = str(extracted_idea)
    
    if not concept:
        return {**state, "is_idea_duplicate": False}
    
    try:
        session = get_session()
        try:
            existing = session.query(KeyIdea).filter(
                KeyIdea.core_idea_text == concept
            )
            if book_id:
                existing = existing.filter(KeyIdea.book_id == book_id)
            
            if existing.first():
                stats = state.get("stats", {})
                stats["idea_duplicates_skipped"] = stats.get("idea_duplicates_skipped",0) + 1
                return {**state, "is_idea_duplicate": True, "stats":stats}
        finally:
            session.close()
    except Exception as e:
        return {**state, "is_idea_duplicate": False}
    
    return {**state,"is_idea_duplicate": False}
