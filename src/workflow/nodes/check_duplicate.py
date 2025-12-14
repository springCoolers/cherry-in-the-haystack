"""
중복 체크 노드.

저장 전 중복 아이디어 체크.
"""

from src.workflow.state import PipelineState
from src.db.connection import get_session
from src.db.models import KeyIdea


def check_duplicate(state: PipelineState) -> PipelineState:
    """
    저장 전 중복 체크.

    동일한 concept이 이미 존재하는지 확인.
    (추후 임베딩 기반 유사도 체크로 확장 가능)

    Args:
        state: PipelineState (extracted_idea, book_id 필수)

    Returns:
        업데이트된 PipelineState (is_duplicate 추가)
    """
    extracted_idea = state.get("extracted_idea")
    book_id = state.get("book_id")

    if not extracted_idea:
        return {**state, "is_duplicate": False}

    # concept 추출
    if hasattr(extracted_idea, "concept"):
        concept = extracted_idea.concept
    elif isinstance(extracted_idea, dict):
        concept = extracted_idea.get("concept", "")
    else:
        concept = str(extracted_idea)

    if not concept:
        return {**state, "is_duplicate": False}

    try:
        session = get_session()
        try:
            # 동일 concept 존재 여부 확인
            query = session.query(KeyIdea).filter(
                KeyIdea.core_idea_text == concept
            )

            # book_id가 있으면 같은 책 내에서만 중복 체크
            if book_id:
                query = query.filter(KeyIdea.book_id == book_id)

            existing = query.first()
            is_duplicate = existing is not None

            # 통계 업데이트
            if is_duplicate:
                stats = state.get("stats", {})
                stats["duplicates_skipped"] = stats.get("duplicates_skipped", 0) + 1
                return {**state, "is_duplicate": True, "stats": stats}

            return {**state, "is_duplicate": False}

        finally:
            session.close()

    except Exception as e:
        # 에러 발생 시 중복이 아닌 것으로 처리 (저장 진행)
        return {**state, "is_duplicate": False, "error": f"Duplicate check warning: {str(e)}"}


def check_duplicate_embedding(state: PipelineState, threshold: float = 0.9) -> PipelineState:
    """
    임베딩 기반 유사도 중복 체크.

    (추후 구현 예정)
    - 현재 아이디어의 임베딩 생성
    - 기존 아이디어들과 코사인 유사도 계산
    - threshold 이상이면 중복으로 판단

    Args:
        state: PipelineState
        threshold: 유사도 임계값 (기본 0.9)

    Returns:
        업데이트된 PipelineState
    """
    # TODO: 임베딩 기반 중복 체크 구현
    # 1. sentence-transformers로 임베딩 생성
    # 2. 기존 아이디어와 코사인 유사도 계산
    # 3. 유사한 아이디어 그룹핑 (idea_group_id)

    return {**state, "is_duplicate": False}
