"""ChromaDB synchronization utilities."""

from typing import List, Dict, Any

from storage.graph_query_engine import GraphQueryEngine
from storage.vector_store import VectorStore


def get_graphdb_concepts(graph_engine: GraphQueryEngine) -> List[Dict[str, str]]:
    """Graph DB에서 모든 개념과 description 조회.
    
    Args:
        graph_engine: GraphQueryEngine 인스턴스
        
    Returns:
        개념 정보 리스트 (concept_id, label, description, parent)
    """
    query = """
    PREFIX llm: <http://example.org/llm-ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    
    SELECT ?concept ?label ?description ?parent
    WHERE {
        ?conceptUri a owl:Class .
        ?conceptUri rdfs:label ?label .
        OPTIONAL { ?conceptUri llm:description ?description . }
        OPTIONAL { ?conceptUri rdfs:subClassOf ?parentUri . }
        
        BIND(REPLACE(STR(?conceptUri), "http://example.org/llm-ontology#", "") AS ?concept)
        BIND(IF(BOUND(?parentUri), REPLACE(STR(?parentUri), "http://example.org/llm-ontology#", ""), "") AS ?parent)
    }
    """
    
    results = graph_engine.query(query)
    
    concepts = []
    for row in results:
        concept_id = row.get("concept", {}).get("value", "")
        label = row.get("label", {}).get("value", "")
        description = row.get("description", {}).get("value", "")
        parent = row.get("parent", {}).get("value", "")
        
        if concept_id and description:
            concepts.append({
                "concept_id": concept_id,
                "label": label,
                "description": description,
                "parent": parent
            })
    
    return concepts


def get_chromadb_concept_ids(vector_store: VectorStore) -> set:
    """ChromaDB에 있는 모든 개념 ID 조회.
    
    Args:
        vector_store: VectorStore 인스턴스
        
    Returns:
        개념 ID 집합
    """
    try:
        all_data = vector_store.collection.get()
        return set(all_data["ids"])
    except Exception:
        return set()


def sync_graphdb_to_chromadb(
    graph_engine: GraphQueryEngine,
    vector_store: VectorStore
) -> int:
    """Graph DB의 개념 중 ChromaDB에 없는 것을 추가.
    
    Args:
        graph_engine: GraphQueryEngine 인스턴스
        vector_store: VectorStore 인스턴스
        
    Returns:
        추가된 개념 수
    """
    print("Graph DB와 ChromaDB 동기화 시작...")
    
    graphdb_concepts = get_graphdb_concepts(graph_engine)
    chromadb_ids = get_chromadb_concept_ids(vector_store)
    
    print(f"Graph DB 개념 수: {len(graphdb_concepts)}")
    print(f"ChromaDB 개념 수: {len(chromadb_ids)}")
    
    missing_concepts = [
        c for c in graphdb_concepts
        if c["concept_id"] not in chromadb_ids
    ]
    
    if not missing_concepts:
        print("동기화 완료: 추가할 개념 없음")
        return 0
    
    print(f"ChromaDB에 {len(missing_concepts)}개 개념 추가 중...")
    
    added_count = 0
    for concept in missing_concepts:
        try:
            vector_store.add_concept(
                concept_id=concept["concept_id"],
                description=concept["description"],
                label=concept["label"],
                parent=concept["parent"]
            )
            added_count += 1
            
            if added_count % 10 == 0:
                print(f"  진행: {added_count}/{len(missing_concepts)}")
        
        except Exception as e:
            print(f"  개념 추가 실패 ({concept['concept_id']}): {e}")
            continue
    
    print(f"동기화 완료: {added_count}개 개념 추가됨")
    return added_count


def verify_sync(
    graph_engine: GraphQueryEngine,
    vector_store: VectorStore
) -> Dict[str, Any]:
    """동기화 상태 확인.
    
    Args:
        graph_engine: GraphQueryEngine 인스턴스
        vector_store: VectorStore 인스턴스
        
    Returns:
        동기화 상태 정보
    """
    graphdb_concepts = get_graphdb_concepts(graph_engine)
    chromadb_ids = get_chromadb_concept_ids(vector_store)
    
    graphdb_ids = set(c["concept_id"] for c in graphdb_concepts)
    
    missing_in_chromadb = graphdb_ids - chromadb_ids
    extra_in_chromadb = chromadb_ids - graphdb_ids
    
    return {
        "graphdb_count": len(graphdb_ids),
        "chromadb_count": len(chromadb_ids),
        "missing_in_chromadb": list(missing_in_chromadb),
        "extra_in_chromadb": list(extra_in_chromadb),
        "is_synced": len(missing_in_chromadb) == 0
    }

