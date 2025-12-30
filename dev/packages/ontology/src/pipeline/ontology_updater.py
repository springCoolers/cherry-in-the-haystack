"""Ontology updater for adding new concepts and relations."""

import os
from typing import Dict, List, Any, Optional

from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from storage.graph_query_engine import GraphQueryEngine
from storage.vector_store import VectorStore
from pipeline.ontology_graph_manager import OntologyGraphManager
from pipeline.staging_manager import StagingManager


class ParentConceptResult(BaseModel):
    """부모 개념 결정 결과 모델."""
    
    parent_concept_id: Optional[str] = Field(
        None,
        description="부모 개념 ID. 적절한 부모가 없으면 None"
    )


class DescriptionResult(BaseModel):
    """설명 생성 결과 모델."""
    
    description: str = Field(..., description="생성된 설명 (3-5문장)")


class OntologyUpdater:
    """온톨로지 업데이트 (신규 개념 추가, relation 추가)."""

    def __init__(
        self,
        graph_engine: GraphQueryEngine,
        vector_store: VectorStore,
        llm: ChatOpenAI = None,
        graph_manager: Optional[OntologyGraphManager] = None,
        staging_manager: Optional[StagingManager] = None
    ) -> None:
        """OntologyUpdater 초기화.
        
        Args:
            graph_engine: GraphQueryEngine 인스턴스
            vector_store: VectorStore 인스턴스
            llm: LLM 인스턴스 (부모 개념 결정용)
            graph_manager: OntologyGraphManager 인스턴스 (선택)
            staging_manager: StagingManager 인스턴스 (선택)
        """
        self.graph_engine = graph_engine
        self.vector_store = vector_store
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.llm = llm or ChatOpenAI(model=model, temperature=0)
        self.structured_llm_parent = self.llm.with_structured_output(ParentConceptResult)
        self.structured_llm_description = self.llm.with_structured_output(DescriptionResult)
        self.graph_manager = graph_manager
        self.staging_manager = staging_manager

    def add_new_concept(
        self,
        concept_id: str,
        label: str,
        description: str,
        parent_concept: str,
        staging: bool = False
    ) -> None:
        """신규 개념을 Graph DB와 Vector DB에 추가.
        
        Args:
            concept_id: 개념 ID
            label: 개념 레이블
            description: 개념 설명
            parent_concept: 부모 개념 ID
            staging: 스테이징 모드 (임시 추가만, 실제 DB에는 반영 안 함)
        """
        if staging:
            # 스테이징 모드: 그래프 매니저와 스테이징 컬렉션에만 추가
            if self.graph_manager:
                self.graph_manager.stage_add_concept(
                    concept_id=concept_id,
                    parent_id=parent_concept,
                    label=label,
                    description=description
                )
            
            # 스테이징 컬렉션에 추가 (유사도 검색을 위해)
            self.vector_store.add_concept(
                concept_id=concept_id,
                description=description,
                label=label,
                parent=parent_concept,
                staging=True  # 스테이징 컬렉션에 추가
            )
        else:
            # 실제 DB에 추가
            self.graph_engine.add_concept(concept_id, label, parent_concept, description)
            
            self.vector_store.add_concept(
                concept_id=concept_id,
                description=description,
                label=label,
                parent=parent_concept,
                staging=False  # 실제 컬렉션에 추가
            )
            
            # 그래프 매니저가 있으면 실제 그래프도 업데이트
            if self.graph_manager:
                self.graph_manager.stage_add_concept(
                    concept_id=concept_id,
                    parent_id=parent_concept,
                    label=label,
                    description=description
                )
                self.graph_manager.commit_staging()

    def add_new_concepts(
        self,
        concepts: List[Dict[str, Any]],
        parent_concept: Optional[str] = None,
        debug: bool = False,
        staging: bool = False
    ) -> None:
        """신규 개념들을 온톨로지에 추가.
        
        Args:
            concepts: 추가할 개념 리스트 (concept_id, label, description 포함)
            parent_concept: 부모 개념 ID (없으면 LLM이 결정)
            debug: 디버그 모드 여부
            staging: 스테이징 모드 (임시 추가만, 실제 DB에는 반영 안 함)
        """
        if not parent_concept:
            parent_concept = self._decide_parent_concept(concepts, debug=debug)
        
        if not parent_concept:
            parent_concept = "LLMConcept"
            if debug:
                print(f"[기본값 사용] 부모 개념: {parent_concept}", flush=True)
        
        if debug:
            mode_str = "[스테이징 모드]" if staging else "[실제 DB 추가]"
            print(f"{mode_str} 부모: {parent_concept}, 개념 수: {len(concepts)}개", flush=True)
        
        for idx, concept in enumerate(concepts, 1):
            if debug:
                print(f"  [{idx}/{len(concepts)}] {concept['concept_id']} → {parent_concept}의 subclass로 추가", flush=True)
            
            self.add_new_concept(
                concept_id=concept["concept_id"],
                label=concept.get("label", concept["concept_id"]),
                description=concept["description"],
                parent_concept=parent_concept,
                staging=staging
            )
            
            # 스테이징 매니저에 메타데이터 저장
            if staging and self.staging_manager:
                self.staging_manager.add_staged_concept(
                    concept_id=concept["concept_id"],
                    label=concept.get("label", concept["concept_id"]),
                    description=concept["description"],
                    parent_concept=parent_concept
                )
        
        if debug:
            mode_str = "[스테이징 완료]" if staging else "[실제 DB 추가 완료]"
            print(f"{mode_str} 총 {len(concepts)}개 개념이 {parent_concept}의 subclass로 추가됨", flush=True)

    def update_description(self, concept_id: str, description: str) -> None:
        """개념의 description을 Graph DB와 Vector DB에서 업데이트.
        
        Args:
            concept_id: 개념 ID
            description: 새 설명
        """
        self.graph_engine.update_description(concept_id, description)
        self.vector_store.update_concept(concept_id, description)

    def add_relations(self, concepts: List[str]) -> None:
        """동일 청크 개념 간 relation 추가.
        
        Args:
            concepts: 개념 ID 리스트
        """
        for i, concept1 in enumerate(concepts):
            for concept2 in concepts[i + 1:]:
                self.graph_engine.add_relation(concept1, concept2)

    def _decide_parent_concept(
        self,
        concepts: List[Dict[str, Any]],
        debug: bool = False
    ) -> Optional[str]:
        """LLM으로 부모 개념 결정 (고도화된 버전).
        
        1. 루트 바로 아래 개념 중 선택
        2. Vector DB에서 유사 개념 검색
        3. 트리 구조 시각화 후 최종 결정
        
        Args:
            concepts: 개념 리스트
            debug: 디버그 모드 여부
            
        Returns:
            부모 개념 ID (결정 실패시 None)
        """
        if not self.graph_manager:
            # 그래프 매니저가 없으면 기본 로직 사용
            return self._decide_parent_concept_simple(concepts, debug)
        
        if debug:
            print(f"\n[부모 개념 결정 - 고도화 버전]", flush=True)
            print(f"입력 개념 수: {len(concepts)}개", flush=True)
        
        # 1. 루트 바로 아래 개념들 가져오기
        root_children = self.graph_manager.get_root_children()
        
        if debug:
            print(f"\n[1단계] 루트 바로 아래 개념들:", flush=True)
            for child in root_children[:10]:  # 최대 10개만 표시
                print(f"  - {child}", flush=True)
            if len(root_children) > 10:
                print(f"  ... 외 {len(root_children) - 10}개", flush=True)
        
        # 2. 새 개념들의 설명을 합쳐서 유사 개념 검색
        combined_description = " ".join([
            c.get("description", c.get("concept_id", ""))
            for c in concepts
        ])
        
        similar_concepts = self.graph_manager.find_similar_concepts_in_graph(
            combined_description,
            k=5
        )
        
        if debug:
            print(f"\n[2단계] Vector DB에서 찾은 유사 개념:", flush=True)
            for idx, sim in enumerate(similar_concepts, 1):
                concept_id = sim.get("concept_id", "")
                path = sim.get("path_to_root", [])
                print(f"  {idx}. {concept_id}", flush=True)
                if path:
                    print(f"     경로: {' → '.join(path)}", flush=True)
        
        # 3. LLM으로 최종 부모 개념 결정
        concept_descriptions = "\n".join([
            f"- {c['concept_id']}: {c['description']}"
            for c in concepts
        ])
        
        root_children_str = ", ".join(root_children[:20])  # 최대 20개만
        similar_concepts_str = "\n".join([
            f"  - {s['concept_id']} (경로: {' → '.join(s.get('path_to_root', []))})"
            for s in similar_concepts[:5]
        ])
        
        messages = [
            SystemMessage(content="""당신은 온톨로지 전문가입니다.
주어진 새 개념들을 온톨로지의 적절한 위치에 배치해야 합니다.

**단계별 결정:**
1. 먼저 루트 바로 아래 개념들 중에서 가장 적절한 것을 선택하세요.
2. 유사 개념들의 위치를 참고하여 결정하세요.
3. 트리 구조를 고려하여 논리적인 위치를 선택하세요.

**중요:**
- 반드시 제공된 루트 자식 개념 중 하나를 선택하거나, 유사 개념의 부모를 선택하세요.
- 기존 온톨로지에 있는 개념 ID만 반환하세요.
- 적절한 부모 개념이 없으면 parent_concept_id를 None으로 설정하세요."""),
            HumanMessage(content=f"""다음 새 개념들의 부모 개념을 결정해주세요:

**새 개념들:**
{concept_descriptions}

**루트 바로 아래 개념들 (직접 선택 가능):**
{root_children_str}

**유사 개념들 (참고용):**
{similar_concepts_str}

이 새 개념들의 공통 부모 개념 ID를 반환하세요.""")
        ]
        
        try:
            if debug:
                print(f"\n[3단계] LLM으로 최종 부모 개념 결정 중...", flush=True)
            
            result = self.structured_llm_parent.invoke(messages)
            parent_id = result.parent_concept_id
            
            if not parent_id:
                if debug:
                    print(f"[LLM 응답] 부모 개념을 찾지 못함", flush=True)
                return None
            
            # 선택된 부모의 서브트리 시각화
            if debug and parent_id in self.graph_manager.staging_graph:
                subtree_viz = self.graph_manager.visualize_subtree(parent_id, max_depth=2)
                print(f"\n[선택된 부모 개념의 서브트리]", flush=True)
                print(subtree_viz, flush=True)
            
            if debug:
                path = self.graph_manager.get_path_to_root(parent_id)
                print(f"\n[최종 결정] 부모 개념: {parent_id}", flush=True)
                if path:
                    print(f"  경로: {' → '.join(path)}", flush=True)
            
            return parent_id
        except Exception as e:
            if debug:
                print(f"[LLM 오류] 부모 개념 결정 실패: {e}", flush=True)
            return None
    
    def _decide_parent_concept_simple(
        self,
        concepts: List[Dict[str, Any]],
        debug: bool = False
    ) -> Optional[str]:
        """간단한 부모 개념 결정 (그래프 매니저 없을 때 사용).
        
        Args:
            concepts: 개념 리스트
            debug: 디버그 모드 여부
            
        Returns:
            부모 개념 ID (결정 실패시 None)
        """
        concept_descriptions = "\n".join([
            f"- {c['concept_id']}: {c['description']}"
            for c in concepts
        ])
        
        messages = [
            SystemMessage(content="""당신은 온톨로지 전문가입니다. 
주어진 개념들의 공통 부모 개념을 결정해주세요.
부모 개념은 반드시 기존 온톨로지에 있는 개념이어야 합니다.

**중요:**
- 기존 온톨로지에 있는 개념 ID만 반환하세요.
- 여러 개념의 공통 상위 개념을 찾아주세요.
- 적절한 부모 개념이 없으면 parent_concept_id를 None으로 설정하세요."""),
            HumanMessage(content=f"""다음 개념들의 공통 부모 개념을 결정해주세요:

{concept_descriptions}

이 개념들의 공통 부모 개념 ID를 반환하세요 (기존 온톨로지에 있는 개념이어야 함).""")
        ]
        
        try:
            if debug:
                print(f"[LLM 호출] 부모 개념 결정 중...", flush=True)
                print(f"입력 개념 수: {len(concepts)}개", flush=True)
            
            result = self.structured_llm_parent.invoke(messages)
            parent_id = result.parent_concept_id
            
            if not parent_id:
                if debug:
                    print(f"[LLM 응답] 부모 개념을 찾지 못함", flush=True)
                return None
            
            if debug:
                print(f"[LLM 응답] 결정된 부모 개념: {parent_id}", flush=True)
            
            return parent_id
        except Exception as e:
            if debug:
                print(f"[LLM 오류] 부모 개념 결정 실패: {e}", flush=True)
            return None

    def generate_description(
        self,
        concept_id: str,
        label: str,
        parent: str = None
    ) -> str:
        """LLM으로 개념 설명 생성.
        
        Args:
            concept_id: 개념 ID
            label: 개념 레이블
            parent: 부모 개념 ID
            
        Returns:
            생성된 설명 (3-5문장)
        """
        parent_info = f"\n상위 개념: {parent}" if parent else ""
        
        messages = [
            SystemMessage(content="""당신은 LLM 및 AI 분야 전문가입니다.
주어진 개념에 대한 상세하고 정확한 설명을 작성해주세요.

다음 내용을 3-5문장으로 포함하세요:
1. 개념의 핵심 정의 (무엇인가?)
2. 주요 특징이나 작동 원리 (어떻게 동작하는가?)
3. 대표적인 사용 사례나 적용 분야 (어디에 쓰이는가?)
4. 관련된 다른 개념들이나 대비되는 특징

벡터 검색에 유리하도록 다양한 표현과 키워드를 자연스럽게 포함하세요.
전문적이면서도 명확하게 작성하세요."""),
            HumanMessage(content=f"""다음 개념에 대한 상세 설명을 작성해주세요:

개념: {label}{parent_info}

3-5문장으로 설명을 작성하세요.""")
        ]
        
        try:
            result = self.structured_llm_description.invoke(messages)
            return result.description
        except Exception as e:
            return f"{label} 관련 개념"

    def bulk_generate_descriptions(
        self,
        concepts: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """여러 개념에 대한 설명을 배치로 생성.
        
        Args:
            concepts: 개념 리스트 (concept_id, label, parent 포함)
            
        Returns:
            concept_id -> description 딕셔너리
        """
        descriptions = {}
        
        for concept in concepts:
            description = self.generate_description(
                concept_id=concept["concept_id"],
                label=concept.get("label", concept["concept_id"]),
                parent=concept.get("parent")
            )
            descriptions[concept["concept_id"]] = description
        
        return descriptions

