"""Staging manager for batch concept addition with review."""

from typing import Dict, List, Any, Optional
from pipeline.ontology_graph_manager import OntologyGraphManager
from storage.graph_query_engine import GraphQueryEngine
from storage.vector_store import VectorStore


class StagingManager:
    """스테이징된 개념들을 관리하고 최종 확인 후 실제 DB에 반영."""
    
    def __init__(
        self,
        graph_manager: OntologyGraphManager,
        graph_engine: GraphQueryEngine,
        vector_store: VectorStore
    ) -> None:
        """StagingManager 초기화.
        
        Args:
            graph_manager: OntologyGraphManager 인스턴스
            graph_engine: GraphQueryEngine 인스턴스
            vector_store: VectorStore 인스턴스
        """
        self.graph_manager = graph_manager
        self.graph_engine = graph_engine
        self.vector_store = vector_store
        
        # 스테이징된 개념들 저장 (확인용)
        self.staged_concepts: List[Dict[str, Any]] = []
    
    def add_staged_concept(
        self,
        concept_id: str,
        label: str,
        description: str,
        parent_concept: str
    ) -> None:
        """스테이징된 개념 추가 (메타데이터 저장).
        
        Args:
            concept_id: 개념 ID
            label: 개념 레이블
            description: 개념 설명
            parent_concept: 부모 개념 ID
        """
        self.staged_concepts.append({
            "concept_id": concept_id,
            "label": label,
            "description": description,
            "parent_concept": parent_concept
        })
    
    def get_staging_summary(self) -> Dict[str, Any]:
        """스테이징된 변경사항 요약.
        
        Returns:
            변경사항 요약 딕셔너리
        """
        changes = self.graph_manager.get_staging_changes()
        
        # 부모 개념별로 그룹화
        by_parent = {}
        for concept in self.staged_concepts:
            parent = concept["parent_concept"]
            if parent not in by_parent:
                by_parent[parent] = []
            by_parent[parent].append(concept)
        
        return {
            "total_concepts": len(self.staged_concepts),
            "added_concepts": changes.get("added", []),
            "by_parent": by_parent,
            "graph_stats": {
                "total_nodes": len(self.graph_manager.staging_graph.nodes()),
                "total_edges": len(self.graph_manager.staging_graph.edges()),
                "staging_nodes": len(self.graph_manager.staging_concepts)
            }
        }
    
    def print_staging_summary(self) -> None:
        """스테이징된 변경사항을 출력."""
        summary = self.get_staging_summary()
        
        print(f"\n{'='*80}")
        print(f"스테이징된 변경사항 요약")
        print(f"{'='*80}")
        print(f"\n총 추가될 개념 수: {summary['total_concepts']}개")
        print(f"그래프 노드 수: {summary['graph_stats']['total_nodes']}개")
        print(f"그래프 엣지 수: {summary['graph_stats']['total_edges']}개")
        
        print(f"\n부모 개념별 분류:")
        for parent, concepts in summary['by_parent'].items():
            print(f"\n  [{parent}] ({len(concepts)}개)")
            for concept in concepts:
                path = self.graph_manager.get_path_to_root(concept["concept_id"])
                print(f"    - {concept['concept_id']}")
                print(f"      경로: {' → '.join(path)}")
                if concept.get("description"):
                    print(f"      설명: {concept['description'][:80]}...")
    
    def commit_to_real_db(self) -> None:
        """스테이징된 변경사항을 실제 DB에 반영."""
        print(f"\n{'='*80}")
        print(f"실제 DB에 반영 시작")
        print(f"{'='*80}\n")
        
        # Graph DB에 추가
        print(f"Graph DB에 추가 중...")
        for idx, concept in enumerate(self.staged_concepts, 1):
            print(f"  [{idx}/{len(self.staged_concepts)}] {concept['concept_id']} → {concept['parent_concept']}")
            
            self.graph_engine.add_concept(
                concept_id=concept["concept_id"],
                label=concept["label"],
                parent=concept["parent_concept"],
                description=concept["description"]
            )
        
        # Vector DB: 스테이징 컬렉션을 실제 컬렉션으로 복사
        print(f"\nVector DB에 반영 중...")
        self.vector_store.commit_staging()
        
        # 그래프 매니저 커밋
        self.graph_manager.commit_staging()
        
        # 스테이징 매니저 초기화
        self.staged_concepts.clear()
        
        print(f"\n✓ 실제 DB 반영 완료")
        print(f"  - Graph DB: {len(self.staged_concepts)}개 개념 추가")
        print(f"  - Vector DB: 스테이징 컬렉션 → 실제 컬렉션 커밋")
        print(f"  - 그래프 매니저: 스테이징 커밋 완료")
    
    def rollback_staging(self) -> None:
        """스테이징된 변경사항을 취소."""
        print(f"\n스테이징 롤백 중...")
        self.graph_manager.rollback_staging()
        self.vector_store.rollback_staging()
        self.staged_concepts.clear()
        print(f"✓ 스테이징 롤백 완료")
        print(f"  - 그래프 매니저: 롤백 완료")
        print(f"  - Vector DB: 스테이징 컬렉션 초기화")

