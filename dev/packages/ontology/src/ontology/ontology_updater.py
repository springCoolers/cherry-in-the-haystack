"""Ontology updater for adding new concepts and relations."""

from typing import Dict, List, Any, Optional

from ontology.graph_query_engine import GraphQueryEngine


class OntologyUpdater:
    """온톨로지 업데이트 (신규 개념 추가, relation 추가)."""

    def __init__(self, graph_engine: GraphQueryEngine) -> None:
        """OntologyUpdater 초기화.
        
        Args:
            graph_engine: GraphQueryEngine 인스턴스
        """
        self.graph_engine = graph_engine
        # TODO: LLM 초기화 (부모 개념 결정용)

    def add_new_concepts(
        self, concepts: List[Dict[str, Any]], parent_concept: Optional[str] = None
    ) -> None:
        """신규 개념 온톨로지에 추가.
        
        Args:
            concepts: 추가할 개념 리스트 (각각 concept_id, description 포함)
            parent_concept: 부모 개념 ID (옵션)
        """
        # TODO: 신규 개념 온톨로지에 추가 로직
        pass

    def add_relations(self, concepts: List[str], chunk_id: str) -> None:
        """동일 청크 개념 간 relation 추가.
        
        Args:
            concepts: 개념 ID 리스트
            chunk_id: 청크 ID
        """
        # TODO: 개념 간 relation 추가 로직 (A - related - B, B - related - A)
        # TODO: 이미 있는 triple이면 weight 증가
        pass

    def _decide_parent_concept(
        self, concepts: List[Dict[str, Any]]
    ) -> Optional[str]:
        """LLM으로 부모 개념 결정.
        
        Args:
            concepts: 개념 리스트
            
        Returns:
            부모 개념 ID (결정 실패시 None)
        """
        # TODO: LLM으로 부모 개념 결정 로직
        pass

