"""Graph reorganizer for suggesting intermediate concepts and relocations."""

import os
from typing import Dict, List, Any, Optional, Set, Tuple
from pydantic import BaseModel, Field

import networkx as nx
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from storage.graph_query_engine import GraphQueryEngine
from storage.vector_store import VectorStore
from pipeline.ontology_graph_manager import OntologyGraphManager
from pipeline.staging_manager import StagingManager


class IntermediateConceptSuggestion(BaseModel):
    """중간 개념 추가 제안 (자식이 2개 이상인 경우만)"""
    concept_id: str
    label: str
    description: str
    parent_concept_id: str
    children_concept_ids: List[str] = Field(..., min_length=2)
    reason: str


class ConceptRelocationSuggestion(BaseModel):
    """개념 재배치 제안"""
    concept_id: str
    current_parent_id: str
    suggested_parent_id: str
    reason: str


class ReorganizationSuggestion(BaseModel):
    """통합 재구성 제안"""
    intermediate_concepts: List[IntermediateConceptSuggestion]
    relocations: List[ConceptRelocationSuggestion]


class SuggestionEvaluation(BaseModel):
    """제안 평가 결과"""
    suggestion_id: str
    suggestion_type: str
    is_needed: bool
    appropriateness_score: float = Field(..., ge=0.0, le=1.0)
    improvement_suggestions: str
    final_decision: str


class EvaluationsResult(BaseModel):
    """평가 결과 통합"""
    evaluations: List[SuggestionEvaluation]


class TreeComparison:
    """트리 비교 결과"""
    def __init__(self):
        self.new_concepts: Set[str] = set()
        self.new_edges: List[Tuple[str, str]] = []
        self.modified_subtrees: List[str] = []
        self.parents_with_many_children: Dict[str, List[str]] = {}


class GraphReorganizer:
    """그래프 재구성 제안 및 평가."""
    
    def __init__(
        self,
        graph_manager: OntologyGraphManager,
        graph_engine: GraphQueryEngine,
        vector_store: VectorStore,
        staging_manager: Optional[StagingManager] = None,
        debug: bool = False
    ) -> None:
        """GraphReorganizer 초기화.
        
        Args:
            graph_manager: OntologyGraphManager 인스턴스
            graph_engine: GraphQueryEngine 인스턴스
            vector_store: VectorStore 인스턴스
            staging_manager: StagingManager 인스턴스 (선택)
            debug: 디버그 모드 여부
        """
        self.graph_manager = graph_manager
        self.graph_engine = graph_engine
        self.vector_store = vector_store
        self.staging_manager = staging_manager
        self.debug = debug
        
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.structured_llm_suggestion = self.llm.with_structured_output(ReorganizationSuggestion)
        self.structured_llm_evaluation = self.llm.with_structured_output(EvaluationsResult)
    
    def compare_trees(self) -> TreeComparison:
        """원래 그래프와 현재 그래프 비교.
        
        Returns:
            TreeComparison 객체
        """
        comparison = TreeComparison()
        
        real_graph = self.graph_manager.real_graph
        staging_graph = self.graph_manager.staging_graph
        
        comparison.new_concepts = self.graph_manager.staging_concepts.copy()
        
        for parent, child in staging_graph.edges():
            if not real_graph.has_edge(parent, child):
                comparison.new_edges.append((parent, child))
        
        for concept_id in comparison.new_concepts:
            if concept_id in staging_graph:
                parent = None
                for p in staging_graph.predecessors(concept_id):
                    parent = p
                    break
                
                if parent:
                    if parent not in comparison.modified_subtrees:
                        comparison.modified_subtrees.append(parent)
        
        for node in staging_graph.nodes():
            if node == self.graph_manager.root_concept:
                continue
            
            children = list(staging_graph.successors(node))
            if len(children) >= 2:
                comparison.parents_with_many_children[node] = children
        
        return comparison
    
    def suggest_reorganization(self, comparison: TreeComparison) -> ReorganizationSuggestion:
        """그래프 재구성 제안 (중간 개념 + 재배치).
        
        Args:
            comparison: 트리 비교 결과
            
        Returns:
            재구성 제안
        """
        if self.debug:
            print(f"\n[그래프 재구성 제안]", flush=True)
            print(f"신규 개념: {len(comparison.new_concepts)}개", flush=True)
            print(f"자식이 2개 이상인 부모: {len(comparison.parents_with_many_children)}개", flush=True)
        
        graph_info = self._build_graph_info(comparison)
        
        messages = [
            SystemMessage(content="""당신은 온톨로지 구조 전문가입니다.
새로 추가된 개념들을 분석하여 그래프 구조를 개선할 수 있는 방법을 제안해주세요.

**제안 유형:**

1. **중간 개념 추가** (선택적, 자식이 2개 이상인 경우만 고려):
   - 여러 자식 개념들이 공통된 특성을 가지고 있을 때
   - 의미적으로 묶을 수 있는 개념들이 있을 때
   - 중간 개념을 만들면 구조가 더 명확해질 때
   - **중요**: 자식이 2개 이상이어도 반드시 만들 필요는 없음. 필요할 때만 제안

2. **개념 재배치**:
   - 현재 부모가 적절하지 않은 경우
   - 더 적합한 부모가 있는 경우
   - 의미적으로 더 잘 맞는 위치로 이동할 수 있는 경우

**제안 시 고려사항:**
- 온톨로지의 계층 구조가 명확해지는가?
- 개념들이 의미적으로 잘 묶이는가?
- 불필요한 중간 개념을 만들지 않는가?
- 재배치가 구조를 개선하는가?

제안할 것이 없으면 빈 리스트를 반환하세요."""),
            HumanMessage(content=f"""다음 그래프 구조를 분석하여 재구성 제안을 해주세요:

{graph_info}

**신규 추가된 개념들:**
{', '.join(sorted(comparison.new_concepts))}

**자식이 2개 이상인 부모 노드들:**
{self._format_parents_with_children(comparison.parents_with_many_children)}

위 정보를 바탕으로:
1. 중간 개념 추가가 필요한 경우 제안 (자식이 2개 이상인 경우만, 필수 아님)
2. 재배치가 필요한 개념 제안

제안할 것이 없으면 빈 리스트를 반환하세요.""")
        ]
        
        try:
            result = self.structured_llm_suggestion.invoke(messages)
            
            if self.debug:
                print(f"  중간 개념 제안: {len(result.intermediate_concepts)}개", flush=True)
                print(f"  재배치 제안: {len(result.relocations)}개", flush=True)
            
            return result
        except Exception as e:
            if self.debug:
                print(f"  제안 생성 오류: {e}", flush=True)
            return ReorganizationSuggestion(intermediate_concepts=[], relocations=[])
    
    def evaluate_suggestions(self, suggestions: ReorganizationSuggestion) -> List[SuggestionEvaluation]:
        """제안 평가.
        
        Args:
            suggestions: 재구성 제안
            
        Returns:
            평가 결과 리스트
        """
        if not suggestions.intermediate_concepts and not suggestions.relocations:
            return []
        
        if self.debug:
            print(f"\n[제안 평가]", flush=True)
        
        graph_info = self._build_graph_info(None)
        
        suggestions_text = self._format_suggestions(suggestions)
        
        messages = [
            SystemMessage(content="""당신은 온톨로지 구조 평가 전문가입니다.
제안된 재구성 사항들을 평가하여 최종 결정을 내려주세요.

**평가 기준:**

1. **중간 개념 제안 평가:**
   - 자식 개념들이 의미적으로 묶일 수 있는가?
   - 중간 개념이 구조를 명확하게 만드는가?
   - 불필요한 복잡성을 추가하지 않는가?
   - 자식이 2개 이상이어도 반드시 만들 필요는 없음

2. **재배치 제안 평가:**
   - 현재 위치가 부적절한가?
   - 제안된 위치가 더 적합한가?
   - 재배치가 구조를 개선하는가?

**최종 결정:**
- "accept": 제안을 그대로 수락
- "reject": 제안을 거부
- "modify": 제안을 수정 필요 (개선 제안 포함)

각 제안에 대해 appropriateness_score (0.0-1.0)를 부여하세요.
각 제안의 suggestion_id는 반드시 제공된 형식(intermediate_0, relocation_0 등)을 그대로 사용하세요.
suggestion_type은 "intermediate_concept" 또는 "relocation"으로 설정하세요."""),
            HumanMessage(content=f"""다음 그래프 구조와 제안을 평가해주세요:

{graph_info}

**제안 사항:**

{suggestions_text}

각 제안에 대해 평가하고 최종 결정을 내려주세요. suggestion_id는 위에 표시된 형식을 정확히 사용하세요.""")
        ]
        
        try:
            result = self.structured_llm_evaluation.invoke(messages)
            
            if self.debug:
                accepted = sum(1 for e in result.evaluations if e.final_decision == "accept")
                print(f"  수락: {accepted}개", flush=True)
                print(f"  거부: {len(result.evaluations) - accepted}개", flush=True)
            
            return result.evaluations
        except Exception as e:
            if self.debug:
                print(f"  평가 오류: {e}", flush=True)
            return []
    
    def finalize_reorganization(
        self,
        suggestions: ReorganizationSuggestion,
        evaluations: List[SuggestionEvaluation]
    ) -> nx.DiGraph:
        """평가 결과를 반영하여 최종 그래프 구조 확정.
        
        Args:
            suggestions: 재구성 제안
            evaluations: 평가 결과
            
        Returns:
            최종 그래프
        """
        final_graph = self.graph_manager.staging_graph.copy()
        
        eval_dict = {e.suggestion_id: e for e in evaluations}
        
        intermediate_idx = 0
        relocation_idx = 0
        
        for suggestion in suggestions.intermediate_concepts:
            suggestion_id = f"intermediate_{intermediate_idx}"
            intermediate_idx += 1
            
            if suggestion_id not in eval_dict:
                continue
            
            evaluation = eval_dict[suggestion_id]
            
            if evaluation.final_decision == "accept":
                if self.debug:
                    print(f"  ✓ 중간 개념 추가: {suggestion.concept_id}", flush=True)
                
                final_graph.add_node(suggestion.concept_id)
                final_graph.add_edge(suggestion.parent_concept_id, suggestion.concept_id)
                
                for child_id in suggestion.children_concept_ids:
                    if final_graph.has_edge(suggestion.parent_concept_id, child_id):
                        final_graph.remove_edge(suggestion.parent_concept_id, child_id)
                    final_graph.add_edge(suggestion.concept_id, child_id)
                
                self.vector_store.add_concept(
                    concept_id=suggestion.concept_id,
                    description=suggestion.description,
                    label=suggestion.label,
                    parent=suggestion.parent_concept_id,
                    staging=True
                )
                
                if self.staging_manager:
                    self.staging_manager.add_staged_concept(
                        concept_id=suggestion.concept_id,
                        label=suggestion.label,
                        description=suggestion.description,
                        parent_concept=suggestion.parent_concept_id
                    )
        
        for relocation in suggestions.relocations:
            suggestion_id = f"relocation_{relocation_idx}"
            relocation_idx += 1
            
            if suggestion_id not in eval_dict:
                continue
            
            evaluation = eval_dict[suggestion_id]
            
            if evaluation.final_decision == "accept":
                if self.debug:
                    print(f"  ✓ 개념 재배치: {relocation.concept_id} ({relocation.current_parent_id} → {relocation.suggested_parent_id})", flush=True)
                
                if final_graph.has_edge(relocation.current_parent_id, relocation.concept_id):
                    final_graph.remove_edge(relocation.current_parent_id, relocation.concept_id)
                
                if relocation.suggested_parent_id not in final_graph:
                    final_graph.add_node(relocation.suggested_parent_id)
                
                final_graph.add_edge(relocation.suggested_parent_id, relocation.concept_id)
        
        return final_graph
    
    def _build_graph_info(self, comparison: Optional[TreeComparison]) -> str:
        """그래프 정보를 텍스트로 변환.
        
        Args:
            comparison: 트리 비교 결과 (선택)
            
        Returns:
            그래프 정보 문자열
        """
        graph = self.graph_manager.staging_graph
        root = self.graph_manager.root_concept
        
        lines = [f"루트 개념: {root}"]
        lines.append(f"총 노드 수: {len(graph.nodes())}")
        lines.append(f"총 엣지 수: {len(graph.edges())}")
        lines.append("\n주요 서브트리:")
        
        root_children = list(graph.successors(root))
        for child in sorted(root_children)[:10]:
            subtree_info = self._get_subtree_info(graph, child, max_depth=2)
            lines.append(f"  {subtree_info}")
        
        return "\n".join(lines)
    
    def _get_subtree_info(self, graph: nx.DiGraph, root: str, max_depth: int = 2) -> str:
        """서브트리 정보를 문자열로 반환.
        
        Args:
            graph: 그래프
            root: 루트 노드
            max_depth: 최대 깊이
            
        Returns:
            서브트리 정보 문자열
        """
        if root not in graph:
            return f"{root} (없음)"
        
        def _format_node(node: str, prefix: str = "", depth: int = 0) -> List[str]:
            if depth > max_depth:
                return []
            
            lines = [f"{prefix}{node}"]
            children = sorted(graph.successors(node))
            
            for idx, child in enumerate(children[:5]):
                is_last = idx == len(children[:5]) - 1
                child_prefix = prefix + ("    " if is_last else "│   ")
                lines.extend(_format_node(child, child_prefix, depth + 1))
            
            if len(children) > 5:
                lines.append(f"{prefix}    ... ({len(children) - 5}개 더)")
            
            return lines
        
        return "\n".join(_format_node(root))
    
    def _format_parents_with_children(self, parents_with_children: Dict[str, List[str]]) -> str:
        """자식이 많은 부모 노드들을 포맷팅.
        
        Args:
            parents_with_children: 부모 -> 자식 리스트 딕셔너리
            
        Returns:
            포맷팅된 문자열
        """
        if not parents_with_children:
            return "없음"
        
        lines = []
        for parent, children in sorted(parents_with_children.items()):
            lines.append(f"  - {parent}: {len(children)}개 자식 ({', '.join(children[:5])}{'...' if len(children) > 5 else ''})")
        
        return "\n".join(lines)
    
    def _format_suggestions(self, suggestions: ReorganizationSuggestion) -> str:
        """제안을 포맷팅.
        
        Args:
            suggestions: 재구성 제안
            
        Returns:
            포맷팅된 문자열
        """
        lines = []
        
        if suggestions.intermediate_concepts:
            lines.append("**중간 개념 제안:**")
            for idx, suggestion in enumerate(suggestions.intermediate_concepts):
                suggestion_id = f"intermediate_{idx}"
                lines.append(f"  suggestion_id: {suggestion_id}")
                lines.append(f"  개념: {suggestion.concept_id} (부모: {suggestion.parent_concept_id})")
                lines.append(f"  자식: {', '.join(suggestion.children_concept_ids)}")
                lines.append(f"  이유: {suggestion.reason}")
                lines.append("")
        
        if suggestions.relocations:
            lines.append("**재배치 제안:**")
            for idx, relocation in enumerate(suggestions.relocations):
                suggestion_id = f"relocation_{idx}"
                lines.append(f"  suggestion_id: {suggestion_id}")
                lines.append(f"  개념: {relocation.concept_id}")
                lines.append(f"  현재: {relocation.current_parent_id} → 제안: {relocation.suggested_parent_id}")
                lines.append(f"  이유: {relocation.reason}")
                lines.append("")
        
        return "\n".join(lines) if lines else "제안 없음"

