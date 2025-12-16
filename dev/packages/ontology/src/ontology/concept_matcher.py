"""Concept matcher using LLM for final matching."""

from typing import Dict, List, Any, Optional

from ontology.vector_store import VectorStore


class ConceptMatcher:
    """키워드-개념 매칭 (LLM 사용)."""

    def __init__(self, vector_store: VectorStore) -> None:
        """ConceptMatcher 초기화.
        
        Args:
            vector_store: 벡터 스토어 인스턴스
        """
        self.vector_store = vector_store
        # TODO: LLM 초기화

    def match(
        self, keyword: str, candidates: List[Dict[str, Any]]
    ) -> Optional[str]:
        """LLM으로 최종 매칭 결정.
        
        Args:
            keyword: 매칭할 키워드
            candidates: 후보 개념 리스트
            
        Returns:
            매칭된 개념 ID (매칭 실패시 None)
        """
        # TODO: LLM 매칭 로직
        pass

    def _call_llm(
        self, keyword: str, candidates: List[Dict[str, Any]]
    ) -> Optional[str]:
        """LLM 호출하여 매칭 결정.
        
        Args:
            keyword: 매칭할 키워드
            candidates: 후보 개념 리스트
            
        Returns:
            매칭된 개념 ID (매칭 실패시 None)
        """
        # TODO: LLM 호출 로직
        pass

