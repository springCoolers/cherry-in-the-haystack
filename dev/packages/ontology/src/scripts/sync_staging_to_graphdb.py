"""스테이징된 개념들을 GraphDB에 반영하는 스크립트."""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.graph_query_engine import GraphQueryEngine
from storage.vector_store import VectorStore
from pipeline.ontology_graph_manager import OntologyGraphManager


def sync_from_file(json_path: str, graph_endpoint: str) -> None:
    """JSON 파일에서 읽어서 GraphDB에 반영.
    
    Args:
        json_path: 스테이징 JSON 파일 경로
        graph_endpoint: GraphDB SPARQL 엔드포인트 URL
    """
    print(f"\n{'='*80}")
    print(f"JSON 파일에서 GraphDB로 싱크 시작")
    print(f"{'='*80}\n")
    
    if not os.path.exists(json_path):
        print(f"오류: 파일이 없습니다: {json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    staged_concepts = data.get('staged_concepts', [])
    
    if not staged_concepts:
        print("스테이징된 개념이 없습니다.")
        return
    
    print(f"스테이징된 개념 수: {len(staged_concepts)}개\n")
    
    graph_engine = GraphQueryEngine(graph_endpoint)
    
    for idx, concept in enumerate(staged_concepts, 1):
        print(f"[{idx}/{len(staged_concepts)}] {concept['concept_id']} → {concept['parent_concept']}")
        
        try:
            graph_engine.add_concept(
                concept_id=concept["concept_id"],
                label=concept["label"],
                parent=concept["parent_concept"],
                description=concept["description"]
            )
            print(f"  ✓ GraphDB에 추가 완료")
        except Exception as e:
            print(f"  ✗ 오류: {e}")
    
    print(f"\n✓ GraphDB 반영 완료: {len(staged_concepts)}개 개념 추가됨")


def sync_from_vectordb(vector_db_path: str, graph_endpoint: str) -> None:
    """VectorDB 스테이징 컬렉션에서 읽어서 GraphDB에 반영.
    
    add_to_ontology에서 추가된 개념만 싱크합니다.
    
    Args:
        vector_db_path: VectorDB 저장 경로
        graph_endpoint: GraphDB SPARQL 엔드포인트 URL
    """
    print(f"\n{'='*80}")
    print(f"VectorDB에서 GraphDB로 싱크 시작")
    print(f"{'='*80}\n")
    
    vector_store = VectorStore(vector_db_path)
    graph_engine = GraphQueryEngine(graph_endpoint)
    
    print("OntologyGraphManager 초기화 중...")
    graph_manager = OntologyGraphManager(
        graph_engine=graph_engine,
        vector_store=vector_store,
        root_concept="LLMConcept",
        debug=False
    )
    
    staging_changes = graph_manager.get_staging_changes()
    added_concept_ids = set(staging_changes.get("added", []))
    
    if not added_concept_ids:
        print("add_to_ontology에서 추가된 개념이 없습니다.")
        return
    
    print(f"add_to_ontology에서 추가된 개념 수: {len(added_concept_ids)}개\n")
    
    staging_data = vector_store.staging_collection.get()
    
    if not staging_data["ids"]:
        print("스테이징 컬렉션에 개념이 없습니다.")
        return
    
    concepts_to_sync = []
    for i, concept_id in enumerate(staging_data["ids"]):
        if concept_id in added_concept_ids:
            metadata = staging_data["metadatas"][i]
            description = staging_data["documents"][i]
            label = metadata.get("label", concept_id)
            parent = metadata.get("parent", "LLMConcept")
            
            concepts_to_sync.append({
                "concept_id": concept_id,
                "label": label,
                "parent": parent,
                "description": description
            })
    
    if not concepts_to_sync:
        print("싱크할 개념이 없습니다.")
        return
    
    print(f"싱크할 개념 수: {len(concepts_to_sync)}개\n")
    
    synced_concept_ids = []
    
    for idx, concept in enumerate(concepts_to_sync, 1):
        concept_id = concept["concept_id"]
        print(f"[{idx}/{len(concepts_to_sync)}] {concept_id} → {concept['parent']}")
        
        try:
            if graph_engine.concept_exists(concept_id):
                graph_engine.update_description(concept_id, concept["description"])
                vector_store.update_concept(concept_id, concept["description"])
                print(f"  ✓ GraphDB 및 VectorDB 업데이트 완료")
            else:
                graph_engine.add_concept(
                    concept_id=concept_id,
                    label=concept["label"],
                    parent=concept["parent"],
                    description=concept["description"]
                )
                synced_concept_ids.append(concept_id)
                print(f"  ✓ GraphDB에 추가 완료")
        except Exception as e:
            print(f"  ✗ 오류: {e}")
    
    print(f"\n✓ GraphDB 반영 완료: {len(concepts_to_sync)}개 개념 처리됨")
    
    if synced_concept_ids:
        print(f"\nVectorDB 스테이징 컬렉션의 {len(synced_concept_ids)}개 개념을 실제 컬렉션으로 커밋 중...")
        vector_store.commit_staging_concepts(synced_concept_ids)
        print(f"✓ VectorDB 커밋 완료")
    else:
        print(f"\nVectorDB에 새로 추가할 개념이 없습니다 (모두 업데이트됨).")


def main():
    """메인 함수."""
    parser = argparse.ArgumentParser(
        description="스테이징된 개념들을 GraphDB에 반영"
    )
    parser.add_argument(
        "--json",
        type=str,
        help="스테이징 JSON 파일 경로"
    )
    parser.add_argument(
        "--vectordb",
        type=str,
        help="VectorDB 저장 경로"
    )
    parser.add_argument(
        "--graph-endpoint",
        type=str,
        required=True,
        help="GraphDB SPARQL 엔드포인트 URL"
    )
    
    args = parser.parse_args()
    
    if args.json:
        sync_from_file(args.json, args.graph_endpoint)
    elif args.vectordb:
        sync_from_vectordb(args.vectordb, args.graph_endpoint)
    else:
        parser.print_help()
        print("\n오류: --json 또는 --vectordb 중 하나를 지정해야 합니다.")


if __name__ == "__main__":
    main()

