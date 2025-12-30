"""Document ontology mapper using LangGraph workflow."""

import json
import os
import re
from typing import Dict, List, Any, TypedDict, Optional

from pydantic import BaseModel, Field

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from storage.graph_query_engine import GraphQueryEngine
from storage.vector_store import VectorStore
from storage.new_concept_manager import NewConceptManager
from pipeline.concept_matcher import ConceptMatcher
from pipeline.ontology_updater import OntologyUpdater


class KoreanDescriptionResult(BaseModel):
    """한글 설명 결과 모델."""
    
    description: str = Field(..., description="생성된 한글 설명 (3-5문장)")


class ClusterValidationResult(BaseModel):
    """클러스터 검증 결과 모델."""
    
    selected_noun_phrase: str = Field(..., description="선택된 대표 noun_phrase_summary")
    can_merge: bool = Field(..., description="모든 개념을 합칠 수 있는지 여부")
    reason: str = Field(..., description="합칠 수 있는지 여부에 대한 이유")


class MappingState(TypedDict):
    """LangGraph State 정의."""

    concept: str
    chunk_text: str
    source: str
    metadata: Dict[str, Any]
    matched_concept_id: Optional[str]
    is_new: bool
    candidates: List[Dict[str, Any]]
    korean_description: Optional[str]
    reason: Optional[str]
    noun_phrase_summary: Optional[str]
    should_add_to_ontology: Optional[bool]
    cluster: Optional[Dict[str, Any]]


class DocumentOntologyMapper:
    """LangGraph 플로우 오케스트레이터."""

    def __init__(
        self,
        graph_engine: GraphQueryEngine,
        vector_store: VectorStore,
        concept_matcher: ConceptMatcher,
        new_concept_manager: NewConceptManager,
        ontology_updater: OntologyUpdater,
        debug: bool = False,
    ) -> None:
        """DocumentOntologyMapper 초기화.
        
        Args:
            graph_engine: GraphQueryEngine 인스턴스
            vector_store: VectorStore 인스턴스
            concept_matcher: ConceptMatcher 인스턴스
            new_concept_manager: NewConceptManager 인스턴스
            ontology_updater: OntologyUpdater 인스턴스
            debug: 디버그 모드 활성화 여부
        """
        self.graph_engine = graph_engine
        self.vector_store = vector_store
        self.concept_matcher = concept_matcher
        self.new_concept_manager = new_concept_manager
        self.ontology_updater = ontology_updater
        self.debug = debug
        
        # 한글 description 생성을 위한 LLM 초기화
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.llm = ChatOpenAI(model=model, temperature=0)
        self.structured_llm_description = self.llm.with_structured_output(KoreanDescriptionResult)
        self.structured_llm_cluster_validation = self.llm.with_structured_output(ClusterValidationResult)
        
        self.workflow = self.create_mapping_workflow()

    def map_concept(
        self,
        concept: str,
        chunk_text: str,
        source: str,
        section_title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """단일 개념 매핑 함수 (LangGraph 실행).
        
        Args:
            concept: 매핑할 개념
            chunk_text: 개념이 추출된 원본 텍스트
            source: 출처
            section_title: 섹션 제목 (매칭 시 활용)
            metadata: 추가 메타데이터
            
        Returns:
            매핑 결과 딕셔너리
        """
        metadata_dict = metadata or {}
        if section_title:
            metadata_dict["section_title"] = section_title
        
        initial_state: MappingState = {
            "concept": concept,
            "chunk_text": chunk_text,
            "source": source,
            "metadata": metadata_dict,
            "matched_concept_id": None,
            "is_new": False,
            "candidates": [],
            "korean_description": None,
            "reason": None,
            "noun_phrase_summary": None,
            "should_add_to_ontology": None,
            "cluster": None,
        }
        
        # stream 사용하여 각 노드 실행 확인 (디버그 모드에서)
        if self.debug:
            final_state = initial_state
            for step in self.workflow.stream(initial_state):
                # 각 step은 {node_name: state} 형태
                if step:
                    final_state = list(step.values())[0]
            result = final_state
        else:
            # 일반 모드에서는 invoke 사용
            result = self.workflow.invoke(initial_state)
        
        return result

    def create_mapping_workflow(self) -> Any:
        """LangGraph StateGraph 생성 및 노드 연결.
        
        Returns:
            구성된 StateGraph
        """
        workflow = StateGraph(MappingState)

        workflow.add_node("search_similar_concepts", self.search_similar_concepts)
        workflow.add_node("match_with_llm", self.match_with_llm)
        workflow.add_node("save_new_concept", self.save_new_concept)
        workflow.add_node("check_new_concept_clusters", self.check_new_concept_clusters)
        workflow.add_node("add_to_ontology", self.add_to_ontology)

        workflow.set_entry_point("search_similar_concepts")
        workflow.add_edge("search_similar_concepts", "match_with_llm")
        
        def should_save_new(state: MappingState) -> str:
            return "save_new_concept" if state["is_new"] else END
        
        workflow.add_conditional_edges("match_with_llm", should_save_new)
        workflow.add_edge("save_new_concept", "check_new_concept_clusters")

        workflow.add_edge("check_new_concept_clusters", END)
        
        # def should_add_to_ontology(state: MappingState) -> str:
        #     return "add_to_ontology" if state.get("should_add_to_ontology", False) else END
        
        # workflow.add_conditional_edges("check_new_concept_clusters", should_add_to_ontology)
        # workflow.add_edge("add_to_ontology", END)

        return workflow.compile()

    def _generate_korean_description(self, concept: str, chunk_text: str = None) -> str:
        """개념을 한글 설명으로 변환 (상세 버전).
        
        Args:
            concept: 개념 이름
            chunk_text: 개념이 추출된 원본 텍스트 (선택)
            
        Returns:
            한글 설명 (3-5문장)
        """
        chunk_info = ""
        if chunk_text:
            chunk_info = f"\n\n원본 텍스트 맥락:\n{chunk_text[:500]}"
        
        messages = [
            SystemMessage(content="""당신은 LLM 및 AI 분야 전문가입니다.
주어진 개념에 대한 상세하고 정확한 한글 설명을 작성해주세요.

다음 내용을 3-5문장으로 포함하세요:
1. 개념의 핵심 정의 (무엇인가?)
2. 주요 특징이나 작동 원리 (어떻게 동작하는가?)
3. 대표적인 사용 사례나 적용 분야 (어디에 쓰이는가?)
4. 관련된 다른 개념들이나 대비되는 특징

원본 텍스트가 제공된 경우, 그 맥락을 고려하여 설명을 작성하세요.
벡터 검색에 유리하도록 다양한 표현과 키워드를 자연스럽게 포함하세요.
전문적이면서도 명확하게 작성하세요."""),
            HumanMessage(content=f"""다음 개념에 대한 상세 한글 설명을 작성해주세요:

개념: {concept}{chunk_info}

3-5문장으로 한글 설명을 작성하세요.""")
        ]
        
        try:
            result = self.structured_llm_description.invoke(messages)
            return result.description
        except Exception as e:
            if self.debug:
                print(f"한글 설명 생성 실패: {e}")
            # 실패 시 원본 개념 반환
            return concept
    
    def search_similar_concepts(self, state: MappingState) -> MappingState:
        """벡터 검색 노드 (vector_store 사용).
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        concept = state["concept"]
        chunk_text = state.get("chunk_text", "")
        
        if self.debug:
            print(f"\n{'='*60}", flush=True)
            print(f"[search_similar_concepts] 개념: {concept}", flush=True)
            print(f"{'='*60}", flush=True)
            total_concepts = self.vector_store.count()
            print(f"ChromaDB 총 개념 수: {total_concepts}", flush=True)
        
        # 1. 한글 description 생성
        korean_description = self._generate_korean_description(concept, chunk_text)
        
        if self.debug:
            print(f"생성된 한글 설명: {korean_description}", flush=True)
        
        # 2. 한글 설명으로 벡터 검색
        candidates = self.vector_store.find_similar(korean_description, k=5)
        
        # LLMConcept은 매칭 대상에서 제외
        candidates = [c for c in candidates if c.get('concept_id') != 'LLMConcept']
        
        state["candidates"] = candidates
        state["korean_description"] = korean_description
        
        if self.debug:
            print(f"\n후보 개념 수: {len(candidates)}", flush=True)
            if candidates:
                print(f"후보 개념 목록:", flush=True)
                for idx, c in enumerate(candidates, 1):
                    concept_id = c.get('concept_id', 'N/A')
                    description = c.get('description', '')
                    distance = c.get('distance', 'N/A')
                    print(f"  {idx}. {concept_id} (거리: {distance})", flush=True)
                    print(f"     설명: {description[:100]}...", flush=True)
            else:
                print("  ⚠️ 후보 개념이 없습니다. ChromaDB가 초기화되었는지 확인하세요.", flush=True)
            print(f"\nState after search_similar_concepts:", flush=True)
            print(f"  - candidates: {len(state['candidates'])}개", flush=True)
        
        return state


    def match_with_llm(self, state: MappingState) -> MappingState:
        """LLM 매칭 노드 (concept_matcher 사용).
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        concept = state["concept"]
        chunk_text = state["chunk_text"]
        candidates = state["candidates"]
        section_title = state.get("metadata", {}).get("section_title")
            
        if not candidates:
            state["is_new"] = True
            if self.debug:
                print("후보 없음 → 신규 개념으로 분류", flush=True)
            return state
        
        match_result = self.concept_matcher.match(
            keyword=concept,
            context=chunk_text,
            candidates=candidates,
            section_title=section_title,

        )
        
        matched_concept = match_result.get("matched")
        reason = match_result.get("reason", "이유 없음")
        noun_phrase_summary = match_result.get("noun_phrase_summary", "")
        most_similar_concept_id = match_result.get("most_similar_concept_id")
        
        state["reason"] = reason
        state["noun_phrase_summary"] = noun_phrase_summary
        
        if matched_concept:
            state["matched_concept_id"] = matched_concept
            state["is_new"] = False
            if self.debug:
                print(f"\n[MatchingResult]", flush=True)
                print(f"  - noun_phrase_summary: {noun_phrase_summary}", flush=True)
                print(f"  - most_similar_concept_id: {most_similar_concept_id}", flush=True)
                print(f"  - matched_concept_id: {matched_concept}", flush=True)
                print(f"  - reason: {reason}", flush=True)
                print(f"✓ 매칭 성공: {matched_concept}", flush=True)
                print(f"  → is_new: False", flush=True)
        else:
            state["is_new"] = True
            if self.debug:
                print(f"\n[MatchingResult]", flush=True)
                print(f"  - noun_phrase_summary: {noun_phrase_summary}", flush=True)
                print(f"  - most_similar_concept_id: {most_similar_concept_id}", flush=True)
                print(f"  - matched_concept_id: None", flush=True)
                print(f"  - reason: {reason}", flush=True)
                print("✗ 매칭 실패 → 신규 개념으로 분류", flush=True)
                print(f"  → is_new: True", flush=True)
        
        if self.debug:
            print(f"\nState after match_with_llm:", flush=True)
            print(f"  - matched_concept_id: {state.get('matched_concept_id')}", flush=True)
            print(f"  - is_new: {state['is_new']}", flush=True)
        
        return state

    def save_new_concept(self, state: MappingState) -> MappingState:
        """신규 개념 저장 노드 (new_concept_manager 사용).
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        concept = state["concept"]
        korean_description = state.get("korean_description") or state["chunk_text"][:500]
        source = state["source"]
        original_keyword = state["concept"]
        noun_phrase_summary = state.get("noun_phrase_summary")
        reason = state.get("reason")
        
        if self.debug:
            print(f"\n{'='*60}", flush=True)
            print(f"[save_new_concept] 개념: {concept}", flush=True)
            print(f"{'='*60}", flush=True)
            print(f"출처: {source}", flush=True)
            print(f"원본 키워드: {original_keyword}", flush=True)
            print(f"명사구 요약: {noun_phrase_summary}", flush=True)
            print(f"판단 이유: {reason[:200] if reason else 'None'}...", flush=True)
        
        self.new_concept_manager.save_concept(
            concept=concept,
            description=korean_description,
            source=source,
            original_keyword=original_keyword,
            noun_phrase_summary=noun_phrase_summary,
            reason=reason
        )
        
        if self.debug:
            print("✓ 신규 개념 저장 완료", flush=True)
        
        return state

    def check_new_concept_clusters(self, state: MappingState) -> MappingState:
        """클러스터 체크 노드 (new_concept_manager 사용).
        
        LLM을 사용하여 클러스터의 개념들을 하나로 합칠 수 있는지 검증합니다.
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        concept = state["concept"]
        
        if self.debug:
            print(f"\n{'='*60}", flush=True)
            print(f"[check_new_concept_clusters] 개념: {concept}", flush=True)
            print(f"{'='*60}", flush=True)
        
        clusters = self.new_concept_manager.get_clusters(min_size=5, concept=concept)
        
        if self.debug:
            print(f"현재 개념이 포함된 클러스터 수: {len(clusters)}", flush=True)
        
        for cluster in clusters:
                if self.debug:
                    print(f"\n[클러스터 검증 시작]", flush=True)
                    print(f"클러스터 개념 수: {len(cluster.get('concepts', []))}개", flush=True)
                
                # LLM으로 클러스터 검증
                validation_result = self._validate_cluster_with_llm(cluster)
                
                if validation_result and validation_result.can_merge:
                    # 대표 개념 설정
                    representative_concept = self._select_representative_by_noun_phrase(
                        cluster.get("concept_details", []),
                        validation_result.selected_noun_phrase
                    )
                    
                    if representative_concept:
                        # 클러스터에 대표 개념 정보 추가
                        cluster["representative_concept"] = representative_concept
                        cluster["selected_noun_phrase"] = validation_result.selected_noun_phrase
                        
                        state["should_add_to_ontology"] = True
                        state["cluster"] = cluster
                        
                        if self.debug:
                            print(f"✓ 클러스터 검증 통과", flush=True)
                            print(f"  - 선택된 대표 noun_phrase: {validation_result.selected_noun_phrase}", flush=True)
                            print(f"  - 합치기 가능 이유: {validation_result.reason}", flush=True)
                            print(f"  - 대표 개념: {representative_concept.get('concept', 'N/A')}", flush=True)
                    else:
                        state["should_add_to_ontology"] = False
                        if self.debug:
                            print(f"✗ 대표 개념 선택 실패", flush=True)
                else:
                    state["should_add_to_ontology"] = False
                    if self.debug:
                        if validation_result:
                            print(f"✗ 클러스터 검증 실패", flush=True)
                            print(f"  - 선택된 noun_phrase: {validation_result.selected_noun_phrase}", flush=True)
                            print(f"  - 합치기 불가 이유: {validation_result.reason}", flush=True)
                        else:
                            print(f"✗ LLM 검증 실패", flush=True)
                
                return state
        
        state["should_add_to_ontology"] = False
        if self.debug:
            print("✗ 클러스터 없음 (5개 미만 또는 현재 개념이 포함된 클러스터 없음)", flush=True)
        
        return state
    
    def _validate_cluster_with_llm(self, cluster: Dict[str, Any]) -> Optional[ClusterValidationResult]:
        """LLM을 사용하여 클러스터의 개념들을 합칠 수 있는지 검증.
        
        Args:
            cluster: 클러스터 정보 (concept_details 포함)
            
        Returns:
            ClusterValidationResult 또는 None (실패 시)
        """
        if self.debug:
            print(f"\n{'='*60}", flush=True)
            print(f"[클러스터 검증]", flush=True)
            print(f"{'='*60}", flush=True)
            print(f"클러스터 개념 수: {len(cluster.get('concepts', []))}", flush=True)
        
        concept_details = cluster.get("concept_details", [])
        
        if not concept_details:
            return None
        
        if self.debug:
            print(f"\n[클러스터 개념 상세 정보]", flush=True)
            print(f"클러스터의 개념 수: {len(concept_details)}개", flush=True)
            for idx, c in enumerate(concept_details, 1):
                print(f"  {idx}. {c.get('concept', 'N/A')}", flush=True)
                print(f"     원본 키워드: {c.get('original_keyword', 'N/A')}", flush=True)
                print(f"     명사구 요약: {c.get('noun_phrase_summary', 'N/A')}", flush=True)
        
        # 클러스터 정보를 텍스트로 구성
        cluster_info = []
        for idx, c in enumerate(concept_details, 1):
            original_keyword = c.get("original_keyword", "N/A")
            noun_phrase_summary = c.get("noun_phrase_summary", "N/A")
            description = c.get("description", "N/A")
            
            cluster_info.append(
                f"{idx}. 원본 키워드: {original_keyword}\n"
                f"   noun_phrase_summary: {noun_phrase_summary}\n"
                f"   설명: {description[:200]}..."
            )
        
        cluster_text = "\n\n".join(cluster_info)
        
        messages = [
            SystemMessage(content="""당신은 온톨로지 전문가입니다.
주어진 클러스터의 개념들을 분석하여 하나의 통합된 개념으로 합칠 수 있는지 판단해주세요.

**작업 순서:**
1. 클러스터 내 모든 개념의 noun_phrase_summary를 검토
2. 가장 적절한 대표 noun_phrase_summary 하나를 선택
3. 클러스터의 모든 개념이 선택한 대표 개념과 합쳐질 수 있는지 판단
   - 모든 개념이 동일하거나 매우 유사한 의미를 나타내는가?
   - 개념들 간의 차이가 단순히 표현 방식의 차이인가, 아니면 본질적으로 다른 개념인가?
4. 합칠 수 있다면 can_merge=True, 그렇지 않다면 can_merge=False
5. 판단 이유를 명확하게 설명

**주의사항:**
- 각각 독립적으로 구분이 필요한 (각각 학습이 필요한) 개념을 합치면 안됩니다.
- 완전히 동일하지 않더라도 세부적이어서 구분이 필요하지 않은 개념이라면 상위 개념으로 합칠 수 있습니다. 
- 선택한 noun_phrase_summary는 모든 개념을 대표할 수 있어야 합니다"""),
            HumanMessage(content=f"""다음 클러스터의 개념들을 분석해주세요:

{cluster_text}

1. 가장 적절한 대표 noun_phrase_summary를 선택하세요
2. 클러스터의 모든 개념이 선택한 대표 개념과 합쳐질 수 있는지 판단하세요
3. 판단 이유를 명확하게 설명하세요""")
        ]
        
        try:
            result = self.structured_llm_cluster_validation.invoke(messages)
            return result
        except Exception as e:
            if self.debug:
                print(f"LLM 검증 실패: {e}", flush=True)
            return None
    
    def _select_representative_by_noun_phrase(
        self,
        concept_details: List[Dict[str, Any]],
        selected_noun_phrase: str
    ) -> Optional[Dict[str, Any]]:
        """선택된 noun_phrase_summary를 가진 대표 개념 선택.
        
        Args:
            concept_details: 개념 상세 정보 리스트
            selected_noun_phrase: LLM이 선택한 noun_phrase_summary
            
        Returns:
            대표 개념 딕셔너리 또는 None
        """
        if not concept_details:
            return None
        
        # 선택된 noun_phrase_summary와 일치하는 개념 찾기
        for concept in concept_details:
            noun_phrase = concept.get("noun_phrase_summary", "").strip()
            if noun_phrase == selected_noun_phrase:
                return concept
        
        # 정확히 일치하는 것이 없으면 첫 번째 개념 반환
        return concept_details[0]

    def add_to_ontology(self, state: MappingState) -> MappingState:
        """온톨로지 추가 노드 (ontology_updater 사용).
        
        Args:
            state: 현재 상태
            
        Returns:
            업데이트된 상태
        """
        cluster = state.get("cluster", {})
        
        if not cluster:
            return state
        
        # LLM이 선택한 대표 개념 사용
        representative_concept = cluster.get("representative_concept")
        
        if not representative_concept:
            if self.debug:
                print("✗ 대표 개념 선택 실패", flush=True)
            return state
        
        if self.debug:
            print(f"\n[대표 개념 선택]", flush=True)
            print(f"  선택된 대표 개념: {representative_concept.get('noun_phrase_summary', representative_concept.get('concept', 'N/A'))}", flush=True)
            print(f"  원본 키워드: {representative_concept.get('original_keyword', 'N/A')}", flush=True)
        
        # 대표 개념을 온톨로지에 추가
        concept_id = representative_concept.get('noun_phrase_summary') or representative_concept.get('concept', '')
        concepts_to_add = [
            {
                "concept_id": concept_id,
                "label": concept_id,
                "description": representative_concept.get('description', '')
            }
        ]
        
        if self.debug:
            print(f"\n[온톨로지에 추가할 개념들]", flush=True)
            for c in concepts_to_add:
                print(f"  - {c['concept_id']}", flush=True)
        
        # 부모 개념 결정 과정 디버깅
        if self.debug:
            print(f"\n[부모 개념 결정 시작]", flush=True)
            print(f"클러스터의 모든 개념:", flush=True)
            for c in concepts_to_add:
                print(f"  - {c['concept_id']}: {c['description'][:100]}...", flush=True)
        
        # 부모 개념 결정 (LLM 사용)
        parent_concept = self.ontology_updater._decide_parent_concept(concepts_to_add)
        
        if self.debug:
            if parent_concept:
                print(f"✓ LLM이 결정한 부모 개념: {parent_concept}", flush=True)
            else:
                print(f"✗ LLM이 부모 개념을 결정하지 못함 → 기본값 'LLMConcept' 사용", flush=True)
                parent_concept = "LLMConcept"
        
        if not parent_concept:
            parent_concept = "LLMConcept"
        
        if self.debug:
            print(f"\n[온톨로지에 추가 중]", flush=True)
            print(f"부모 개념: {parent_concept}", flush=True)
            print(f"추가할 개념 수: {len(concepts_to_add)}개", flush=True)
        
        # 스테이징 모드로 먼저 추가 (임시)
        self.ontology_updater.add_new_concepts(
            concepts=concepts_to_add,
            parent_concept=parent_concept,
            debug=self.debug,
            staging=True  # 임시 추가만
        )
        
        # 스테이징된 변경사항 확인 및 표시
        if self.debug and self.ontology_updater.graph_manager:
            changes = self.ontology_updater.graph_manager.get_staging_changes()
            if changes.get("added"):
                print(f"\n[스테이징 확인] 추가될 개념들:", flush=True)
                for concept_id in changes["added"]:
                    path = self.ontology_updater.graph_manager.get_path_to_root(concept_id)
                    print(f"  - {concept_id} (경로: {' → '.join(path)})", flush=True)
                
                # 선택된 부모의 서브트리 시각화
                subtree_viz = self.ontology_updater.graph_manager.visualize_subtree(
                    parent_concept, 
                    max_depth=3
                )
                print(f"\n[부모 개념 '{parent_concept}'의 서브트리]", flush=True)
                print(subtree_viz, flush=True)
        
        # 스테이징만 수행 (실제 DB 반영은 main.py 끝에서 일괄 처리)
        # 스테이징된 변경사항은 graph_manager에 저장됨
        
        self.new_concept_manager.remove_cluster(cluster["id"])
        
        if self.debug:
            print(f"\n✓ 온톨로지 추가 완료", flush=True)
            print(f"  - 부모 개념: {parent_concept}", flush=True)
            print(f"  - 추가된 개념 수: {len(concepts_to_add)}개", flush=True)
            print(f"  - 클러스터 ID {cluster['id']} 삭제됨", flush=True)
        
        return state

