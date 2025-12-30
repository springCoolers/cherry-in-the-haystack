"""Ontology graph manager using NetworkX for hierarchical structure."""

import networkx as nx
from typing import Dict, List, Optional, Set, Tuple
from storage.graph_query_engine import GraphQueryEngine
from storage.vector_store import VectorStore


class OntologyGraphManager:
    """온톨로지 그래프 관리 (NetworkX 기반).
    
    GraphDB의 subclassof 관계를 NetworkX 그래프로 로드하고 관리합니다.
    임시 업데이트를 지원하여 최종 확인 후 실제 DB에 반영할 수 있습니다.
    """
    
    def __init__(
        self,
        graph_engine: GraphQueryEngine,
        vector_store: VectorStore,
        root_concept: str = "Thing"
    ) -> None:
        """OntologyGraphManager 초기화.
        
        Args:
            graph_engine: GraphQueryEngine 인스턴스
            vector_store: VectorStore 인스턴스
            root_concept: 루트 개념 ID (기본값: "Thing")
        """
        self.graph_engine = graph_engine
        self.vector_store = vector_store
        self.root_concept = root_concept
        
        # 실제 그래프 (GraphDB에서 로드)
        self.real_graph = nx.DiGraph()
        
        # 스테이징 그래프 (임시 업데이트용)
        self.staging_graph = nx.DiGraph()
        
        # 스테이징된 개념들 (임시로 추가된 개념)
        self.staging_concepts: Set[str] = set()
        
        # 초기화: 실제 그래프 로드
        self._load_real_graph()
    
    def _load_real_graph(self) -> None:
        """GraphDB에서 subclassof 관계를 로드하여 NetworkX 그래프 생성."""
        try:
            # SPARQL 쿼리: 모든 subclassof 관계 가져오기
            query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX llm: <http://example.org/llm-ontology#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            
            SELECT ?child ?parent
            WHERE {
                ?child rdfs:subClassOf ?parent .
                ?child a owl:Class .
                ?parent a owl:Class .
            }
            """
            
            results = self.graph_engine.query(query)
            
            # 그래프 초기화
            self.real_graph.clear()
            
            # 루트 노드 추가
            self.real_graph.add_node(self.root_concept)
            
            # 엣지 추가
            for row in results:
                child_raw = row.get("child", {}).get("value", "")
                parent_raw = row.get("parent", {}).get("value", "")
                
                # URI에서 개념 ID 추출
                if "#" in child_raw:
                    child = child_raw.split("#")[-1]
                elif "/" in child_raw:
                    child = child_raw.split("/")[-1]
                else:
                    child = child_raw
                
                if "#" in parent_raw:
                    parent = parent_raw.split("#")[-1]
                elif "/" in parent_raw:
                    parent = parent_raw.split("/")[-1]
                else:
                    parent = parent_raw
                
                if child and parent:
                    # 노드가 없으면 추가
                    if child not in self.real_graph:
                        self.real_graph.add_node(child)
                    if parent not in self.real_graph:
                        self.real_graph.add_node(parent)
                    
                    self.real_graph.add_edge(parent, child)  # parent -> child 방향
            
            # 스테이징 그래프를 실제 그래프로 초기화
            self.staging_graph = self.real_graph.copy()
            self.staging_concepts.clear()
            
        except Exception as e:
            print(f"[경고] 그래프 로드 실패: {e}")
            # 빈 그래프로 시작
            self.real_graph.add_node(self.root_concept)
            self.staging_graph = self.real_graph.copy()
    
    def get_root_children(self) -> List[str]:
        """루트 개념 바로 아래 자식 개념들 반환.
        
        Returns:
            루트의 직접 자식 개념 리스트
        """
        if self.root_concept not in self.staging_graph:
            return []
        
        children = list(self.staging_graph.successors(self.root_concept))
        return sorted(children)
    
    def get_subtree(self, root_node: str, max_depth: int = 3) -> nx.DiGraph:
        """특정 노드를 루트로 하는 서브트리 반환.
        
        Args:
            root_node: 서브트리의 루트 노드
            max_depth: 최대 깊이
            
        Returns:
            서브트리 그래프
        """
        if root_node not in self.staging_graph:
            return nx.DiGraph()
        
        # BFS로 서브트리 추출
        subtree = nx.DiGraph()
        visited = set()
        queue = [(root_node, 0)]
        
        while queue:
            node, depth = queue.pop(0)
            
            if depth > max_depth or node in visited:
                continue
            
            visited.add(node)
            subtree.add_node(node)
            
            if depth < max_depth:
                for child in self.staging_graph.successors(node):
                    if child not in visited:
                        subtree.add_edge(node, child)
                        queue.append((child, depth + 1))
        
        return subtree
    
    def get_path_to_root(self, node: str) -> List[str]:
        """노드에서 루트까지의 경로 반환.
        
        Args:
            node: 시작 노드
            
        Returns:
            루트까지의 경로 (노드 리스트)
        """
        if node not in self.staging_graph:
            return []
        
        path = []
        current = node
        
        while current and current != self.root_concept:
            path.append(current)
            predecessors = list(self.staging_graph.predecessors(current))
            if predecessors:
                current = predecessors[0]  # 첫 번째 부모만 사용
            else:
                break
        
        path.append(self.root_concept)
        return list(reversed(path))
    
    def stage_add_concept(
        self,
        concept_id: str,
        parent_id: str,
        label: str = None,
        description: str = None
    ) -> None:
        """임시로 개념 추가 (스테이징).
        
        Args:
            concept_id: 개념 ID
            parent_id: 부모 개념 ID
            label: 개념 레이블
            description: 개념 설명
        """
        # 개념이 없으면 추가
        if concept_id not in self.staging_graph:
            self.staging_graph.add_node(concept_id)
        
        # 부모가 없으면 루트에 연결
        if parent_id not in self.staging_graph:
            parent_id = self.root_concept
        
        # 엣지 추가
        self.staging_graph.add_edge(parent_id, concept_id)
        
        # 스테이징된 개념으로 표시
        self.staging_concepts.add(concept_id)
    
    def stage_remove_concept(self, concept_id: str) -> None:
        """임시로 개념 제거 (스테이징).
        
        Args:
            concept_id: 개념 ID
        """
        if concept_id in self.staging_graph:
            self.staging_graph.remove_node(concept_id)
            self.staging_concepts.discard(concept_id)
    
    def commit_staging(self) -> None:
        """스테이징된 변경사항을 실제 그래프에 반영."""
        self.real_graph = self.staging_graph.copy()
        self.staging_concepts.clear()
    
    def rollback_staging(self) -> None:
        """스테이징된 변경사항을 취소."""
        self.staging_graph = self.real_graph.copy()
        self.staging_concepts.clear()
    
    def get_staging_changes(self) -> Dict[str, List[str]]:
        """스테이징된 변경사항 반환.
        
        Returns:
            추가된 개념과 제거된 개념 딕셔너리
        """
        added = list(self.staging_concepts)
        removed = []
        
        # 실제 그래프에는 있지만 스테이징 그래프에는 없는 노드 찾기
        for node in self.real_graph.nodes():
            if node not in self.staging_graph:
                removed.append(node)
        
        return {
            "added": added,
            "removed": removed
        }
    
    def visualize_subtree(self, root_node: str, max_depth: int = 3) -> str:
        """서브트리를 텍스트로 시각화.
        
        Args:
            root_node: 루트 노드
            max_depth: 최대 깊이
            
        Returns:
            시각화된 트리 문자열
        """
        subtree = self.get_subtree(root_node, max_depth)
        
        if not subtree.nodes():
            return f"[{root_node}] (노드 없음)"
        
        lines = []
        
        def _print_tree(node: str, prefix: str = "", is_last: bool = True):
            lines.append(f"{prefix}{'└── ' if is_last else '├── '}{node}")
            
            children = list(subtree.successors(node))
            for idx, child in enumerate(children):
                is_last_child = idx == len(children) - 1
                child_prefix = prefix + ("    " if is_last else "│   ")
                _print_tree(child, child_prefix, is_last_child)
        
        _print_tree(root_node)
        
        return "\n".join(lines)
    
    def find_similar_concepts_in_graph(
        self,
        query_text: str,
        k: int = 5
    ) -> List[Dict[str, any]]:
        """Vector DB에서 유사한 개념을 찾고 그래프에서의 위치 반환.
        
        Args:
            query_text: 검색 쿼리 텍스트
            k: 반환할 개념 수
            
        Returns:
            유사 개념 리스트 (concept_id, similarity, path_to_root 포함)
        """
        # Vector DB에서 유사 개념 검색
        similar = self.vector_store.find_similar(query_text, k=k)
        
        # 각 개념의 루트까지 경로 추가
        enriched = []
        for concept in similar:
            concept_id = concept.get("concept_id", "")
            if concept_id in self.staging_graph:
                path = self.get_path_to_root(concept_id)
                concept["path_to_root"] = path
                concept["depth"] = len(path) - 1
            else:
                concept["path_to_root"] = []
                concept["depth"] = -1
            
            enriched.append(concept)
        
        return enriched

