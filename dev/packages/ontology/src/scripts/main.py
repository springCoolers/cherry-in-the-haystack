#!/usr/bin/env python3
"""Main processing script for ontology mapping."""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_query_engine import GraphQueryEngine
from storage.vector_store import VectorStore
from storage.new_concept_manager import NewConceptManager
from pipeline.concept_matcher import ConceptMatcher
from pipeline.ontology_updater import OntologyUpdater
from pipeline.document_ontology_mapper import DocumentOntologyMapper
from pipeline.ontology_graph_manager import OntologyGraphManager
from pipeline.staging_manager import StagingManager
from pipeline.relation_builder import add_relations_by_source


def load_jsonl(file_path: str) -> List[Dict[str, Any]]:
    """JSONL 파일 로드.
    
    Args:
        file_path: JSONL 파일 경로
        
    Returns:
        개념 정보 리스트
    """
    concepts = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                data = json.loads(line)
                
                required_fields = ["concept", "section_id", "section_title", "chunk_text"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    print(f"Warning: Line {line_num} missing required fields: {missing_fields}, skipping")
                    continue
                
                concepts.append(data)
            
            except json.JSONDecodeError as e:
                print(f"Warning: Line {line_num} invalid JSON: {e}")
                continue
    
    return concepts


def process_jsonl(
    input_file: str,
    graph_endpoint: str,
    vector_db_path: str,
    new_concept_db_path: str,
    debug: bool = False
) -> None:
    """JSONL 입력을 처리하여 개념 매핑 및 관계 추가.
    
    Args:
        input_file: JSONL 입력 파일 경로
        graph_endpoint: Graph DB SPARQL endpoint
        vector_db_path: Vector DB 경로
        new_concept_db_path: 신규 개념 DB 경로
    """
    print(f"\n{'='*60}")
    print(f"Ontology Mapping 시작")
    print(f"{'='*60}\n")
    
    print(f"입력 파일: {input_file}")
    
    concepts = load_jsonl(input_file)
    print(f"로드된 개념 수: {len(concepts)}\n")
    
    if not concepts:
        print("처리할 개념이 없습니다.")
        return
    
    print("컴포넌트 초기화 중...")
    print(f"Vector DB 경로: {vector_db_path}")
    graph_engine = GraphQueryEngine(graph_endpoint)
    vector_store = VectorStore(vector_db_path)
    print(f"VectorStore 초기화 완료")
    print(f"  - DB 경로: {vector_store.db_path}")
    print(f"  - 컬렉션 이름: {vector_store.collection_name}")
    try:
        collections = vector_store.client.list_collections()
        print(f"  - 사용 가능한 컬렉션: {[c.name for c in collections]}")
    except Exception as e:
        print(f"  - 컬렉션 목록 조회 실패: {e}")
    print(f"  - ChromaDB 총 개념 수: {vector_store.count()}")
    concept_matcher = ConceptMatcher(vector_store)
    new_concept_manager = NewConceptManager(new_concept_db_path, vector_store=vector_store)
    
    # 온톨로지 그래프 매니저 초기화 (NetworkX 그래프 로드)
    print("온톨로지 그래프 로드 중...")
    
    graph_manager = OntologyGraphManager(
        graph_engine=graph_engine,
        vector_store=vector_store,
        root_concept="LLMConcept"
    )
    print(f"그래프 로드 완료: {len(graph_manager.real_graph.nodes())}개 노드, {len(graph_manager.real_graph.edges())}개 엣지")
    
    # 스테이징 매니저 초기화
    staging_manager = StagingManager(
        graph_manager=graph_manager,
        graph_engine=graph_engine,
        vector_store=vector_store
    )
    
    ontology_updater = OntologyUpdater(
        graph_engine=graph_engine,
        vector_store=vector_store,
        graph_manager=graph_manager,
        staging_manager=staging_manager
    )
    
    mapper = DocumentOntologyMapper(
        graph_engine=graph_engine,
        vector_store=vector_store,
        concept_matcher=concept_matcher,
        new_concept_manager=new_concept_manager,
        ontology_updater=ontology_updater,
        debug=debug
    )
    
    print("초기화 완료\n")
    
    print(f"{'='*60}")
    print(f"개념 매핑 시작 ({len(concepts)}개)")
    print(f"{'='*60}\n")
    
    results = []
    
    for idx, concept_data in enumerate(concepts, 1):
        concept = concept_data["concept"]
        chunk_text = concept_data["chunk_text"]
        section_id = concept_data["section_id"]
        section_title = concept_data["section_title"]
        
        source = concept_data.get("source", f"section_{section_id}")
        metadata = {k: v for k, v in concept_data.items() 
                   if k not in ["concept", "chunk_text", "section_id", "section_title"]}
        
        print(f"[{idx}/{len(concepts)}] 처리 중: {concept}")
        
        try:
            result = mapper.map_concept(
                concept=concept,
                chunk_text=chunk_text,
                source=source,
                section_title=section_title,
                metadata=metadata
            )
            
            results.append({
                "concept": concept,
                "section_id": section_id,
                "section_title": section_title,
                "source": source,
                "matched_concept_id": result.get("matched_concept_id"),
                "is_new": result.get("is_new", False)
            })
            
            if result.get("matched_concept_id"):
                print(f"  ✓ 매칭됨: {result['matched_concept_id']}")
            else:
                print(f"  • 신규 개념으로 저장됨")
        
        except Exception as e:
            print(f"  ✗ 오류: {e}")
            continue
    
    # 스테이징된 변경사항 확인 및 최종 반영
    print(f"\n{'='*60}")
    print(f"스테이징된 변경사항 확인")
    print(f"{'='*60}\n")
    
    staging_manager.print_staging_summary()
    
    # 사용자 확인 (자동 승인 또는 수동 확인)
    print(f"\n{'='*60}")
    print(f"실제 DB 반영 여부 확인")
    print(f"{'='*60}")
    
    # 자동 승인 모드 (나중에 수동 확인으로 변경 가능)
    import sys
    if "--auto-commit" in sys.argv:
        print("자동 승인 모드: 스테이징된 변경사항을 실제 DB에 반영합니다.")
        staging_manager.commit_to_real_db()
    else:
        print("\n스테이징된 변경사항을 실제 DB에 반영하시겠습니까?")
        print("반영하려면: --auto-commit 플래그를 추가하거나")
        print("수동으로 staging_manager.commit_to_real_db()를 호출하세요.")
        print("\n롤백하려면: staging_manager.rollback_staging()을 호출하세요.")
    
    # print(f"\n{'='*60}")
    # print(f"관계 추가 시작")
    # print(f"{'='*60}\n")
    
    # add_relations_by_source(results, graph_engine)
    
    # print(f"\n{'='*60}")
    # print(f"처리 완료")
    # print(f"{'='*60}\n")
    
    # matched_count = sum(1 for r in results if r.get("matched_concept_id"))
    # new_count = sum(1 for r in results if r.get("is_new"))
    
    # print(f"총 처리: {len(results)}개")
    # print(f"  - 매칭됨: {matched_count}개")
    # print(f"  - 신규: {new_count}개")


def main():
    """메인 함수."""
    parser = argparse.ArgumentParser(
        description="Process JSONL file to map concepts to ontology"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input JSONL file path"
    )
    parser.add_argument(
        "--graph-endpoint",
        default="http://localhost:7200/repositories/llm-ontology",
        help="Graph DB SPARQL endpoint"
    )
    parser.add_argument(
        "--vector-db",
        default="db/vector_store",
        help="Vector DB path"
    )
    parser.add_argument(
        "--new-concept-db",
        default="db/new_concepts.db",
        help="New concept database path"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (show intermediate states)"
    )
    
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent.parent
    
    vector_db_path = args.vector_db
    if not Path(vector_db_path).is_absolute():
        vector_db_path = str(project_root / vector_db_path)
    
    new_concept_db_path = args.new_concept_db
    if not Path(new_concept_db_path).is_absolute():
        new_concept_db_path = str(project_root / new_concept_db_path)
    
    try:
        process_jsonl(
            input_file=args.input,
            graph_endpoint=args.graph_endpoint,
            vector_db_path=vector_db_path,
            new_concept_db_path=new_concept_db_path,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\n\n중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

