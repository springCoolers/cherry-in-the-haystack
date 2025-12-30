#!/usr/bin/env python3
"""Main processing script for ontology mapping."""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

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
from pipeline.graph_reorganizer import GraphReorganizer
from pipeline.graph_exporter import GraphExporter


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
        root_concept="LLMConcept",
        debug=debug
    )
    print(f"그래프 로드 완료: {len(graph_manager.real_graph.nodes())}개 노드, {len(graph_manager.real_graph.edges())}개 엣지")
    
    # 스테이징 매니저 초기화
    staging_manager = StagingManager(
        graph_manager=graph_manager,
        graph_engine=graph_engine,
        vector_store=vector_store,
        db_path=vector_db_path
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
            
            concept_id = result.get("matched_concept_id")
            results.append({
                "concept": concept,
                "section_id": section_id,
                "section_title": section_title,
                "source": source,
                "matched_concept_id": concept_id,
                "concept_id": concept_id,
                "is_new": result.get("is_new", False)
            })
            
            if result.get("matched_concept_id"):
                print(f"  ✓ 매칭됨: {result['matched_concept_id']}")
            else:
                print(f"  • 신규 개념으로 저장됨")
        
        except Exception as e:
            print(f"  ✗ 오류: {e}")
            continue
    
    # # 그래프 구조 분석 및 재구성
    # print(f"\n{'='*60}")
    # print(f"그래프 구조 분석 및 재구성")
    # print(f"{'='*60}\n")
    
    # reorganizer = GraphReorganizer(
    #     graph_manager=graph_manager,
    #     graph_engine=graph_engine,
    #     vector_store=vector_store,
    #     staging_manager=staging_manager,
    #     debug=debug
    # )
    
    # comparison = reorganizer.compare_trees()
    
    # if comparison.new_concepts:
    #     print(f"신규 추가된 개념: {len(comparison.new_concepts)}개")
    #     print(f"변경된 서브트리: {len(comparison.modified_subtrees)}개")
    #     print(f"자식이 2개 이상인 부모: {len(comparison.parents_with_many_children)}개\n")
        
    #     suggestions = reorganizer.suggest_reorganization(comparison)
        
    #     if suggestions.intermediate_concepts or suggestions.relocations:
    #         evaluations = reorganizer.evaluate_suggestions(suggestions)
            
    #         final_graph = reorganizer.finalize_reorganization(suggestions, evaluations)
            
    #         graph_manager.staging_graph = final_graph
            
    #         print(f"\n그래프 재구성 완료")
    #         print(f"  최종 노드 수: {len(final_graph.nodes())}개")
    #         print(f"  최종 엣지 수: {len(final_graph.edges())}개")
    #     else:
    #         print("재구성 제안 없음\n")
        
    #     graph_exporter = GraphExporter(graph_engine, graph_manager)
    #     output_dir = Path(vector_db_path).parent / "graph_exports"
    #     files = graph_exporter.export_all(graph_manager.staging_graph, output_dir)
        
    #     print(f"\n그래프 구조 파일 저장 완료:")
    #     for file_type, file_path in files.items():
    #         print(f"  - {file_type}: {file_path}")
    # else:
    #     print("신규 추가된 개념이 없어 그래프 재구성을 건너뜁니다.\n")
    
    # 스테이징된 변경사항 확인 및 최종 반영
    print(f"\n{'='*60}")
    print(f"스테이징된 변경사항 확인")
    print(f"{'='*60}\n")
    
    staging_manager.print_staging_summary()
    
    if staging_manager.staged_concepts:
        print(f"\n✓ 스테이징 JSON 파일 저장됨: {staging_manager.staging_file_path}")
    
    # results를 JSON 파일로 저장
    results_dir = Path(vector_db_path).parent / "staged_result"
    results_dir.mkdir(parents=True, exist_ok=True)
    results_file = results_dir / "mapping_results.json"
    
    # 클러스터링으로 추가된 개념들로 results 업데이트
    # staging_manager의 staged_concepts를 직접 사용 (파일보다 메모리 데이터가 더 정확)
    if staging_manager.staged_concepts:
        # original_keywords -> concept_id 매핑 생성
        keyword_to_concept = {}
        for staged_concept in staging_manager.staged_concepts:
            concept_id = staged_concept.get("concept_id")
            original_keywords = staged_concept.get("original_keywords", [])
            if original_keywords:
                for keyword in original_keywords:
                    keyword_to_concept[keyword] = concept_id
        
        # results 업데이트
        updated_count = 0
        for result in results:
            concept = result.get("concept")
            if concept in keyword_to_concept and not result.get("matched_concept_id"):
                concept_id = keyword_to_concept[concept]
                result["matched_concept_id"] = concept_id
                result["concept_id"] = concept_id
                updated_count += 1
        
        if updated_count > 0:
            print(f"\n✓ 클러스터링으로 추가된 개념 매칭: {updated_count}개 업데이트됨")
    
    results_data = {
        "results": results,
        "total_count": len(results),
        "matched_count": sum(1 for r in results if r.get("matched_concept_id")),
        "new_count": sum(1 for r in results if r.get("is_new")),
        "last_updated": datetime.now().isoformat()
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 매핑 결과 JSON 파일 저장됨: {results_file}")
    print(f"  - 총 처리: {results_data['total_count']}개")
    print(f"  - 매칭됨: {results_data['matched_count']}개")
    print(f"  - 신규: {results_data['new_count']}개")
    
    # 사용자 확인 (자동 승인 또는 수동 확인)
    print(f"\n{'='*60}")
    print(f"실제 DB 반영 여부 확인")
    print(f"{'='*60}")
    
    
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

