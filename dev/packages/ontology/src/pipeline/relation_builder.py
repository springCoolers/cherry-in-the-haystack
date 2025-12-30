"""Source-based relation building utilities."""

from typing import List, Dict, Any
from collections import defaultdict

from storage.graph_query_engine import GraphQueryEngine


def group_by_section_id(concepts: List[Dict[str, Any]]) -> Dict[Any, List[str]]:
    """Section ID별로 개념 그룹화.
    
    Args:
        concepts: 개념 정보 리스트 (concept_id, section_id 포함)
        
    Returns:
        Section ID별 개념 ID 리스트 딕셔너리
    """
    grouped = defaultdict(list)
    
    for concept in concepts:
        section_id = concept.get("section_id")
        concept_id = concept.get("matched_concept_id") or concept.get("concept_id")
        
        if section_id is not None and concept_id:
            grouped[section_id].append(concept_id)
    
    return dict(grouped)


def add_relations_by_source(
    concepts: List[Dict[str, Any]],
    graph_engine: GraphQueryEngine
) -> int:
    """Section ID별로 그룹화하여 개념 간 관계 추가.
    
    같은 section_id를 가진 개념들 간에 llm:related 관계를 추가합니다.
    
    Args:
        concepts: 개념 정보 리스트 (section_id, matched_concept_id 포함)
        graph_engine: GraphQueryEngine 인스턴스
        
    Returns:
        추가된 관계 수
    """
    print("Section ID별 개념 관계 추가 시작...")
    
    grouped = group_by_section_id(concepts)
    
    total_relations = 0
    
    for section_id, concept_ids in grouped.items():
        if len(concept_ids) < 2:
            print(f"  Section {section_id}: 개념 1개만 있어 건너뜀")
            continue
        
        unique_ids = list(set(concept_ids))
        
        print(f"  Section {section_id}: {len(unique_ids)}개 개념 간 관계 추가 중...")
        
        relations_added = 0
        for i in range(len(unique_ids)):
            for j in range(i + 1, len(unique_ids)):
                concept1 = unique_ids[i]
                concept2 = unique_ids[j]
                
                try:
                    graph_engine.add_relation(concept1, concept2)
                    relations_added += 1
                except Exception as e:
                    print(f"    관계 추가 실패 ({concept1} - {concept2}): {e}")
                    continue
        
        print(f"    {relations_added}개 관계 추가됨")
        total_relations += relations_added
    
    print(f"관계 추가 완료: 총 {total_relations}개")
    return total_relations


def get_existing_relations(
    concept1: str,
    concept2: str,
    graph_engine: GraphQueryEngine
) -> List[Dict[str, Any]]:
    """두 개념 간 기존 관계 조회.
    
    Args:
        concept1: 첫 번째 개념 ID
        concept2: 두 번째 개념 ID
        graph_engine: GraphQueryEngine 인스턴스
        
    Returns:
        관계 정보 리스트
    """
    query = f"""
    PREFIX llm: <http://example.org/llm-ontology#>
    
    SELECT ?predicate ?weight
    WHERE {{
        {{
            llm:{concept1} ?predicate llm:{concept2} .
            OPTIONAL {{ ?predicate llm:weight ?weight . }}
        }}
        UNION
        {{
            llm:{concept2} ?predicate llm:{concept1} .
            OPTIONAL {{ ?predicate llm:weight ?weight . }}
        }}
    }}
    """
    
    results = graph_engine.query(query)
    
    relations = []
    for row in results:
        predicate = row.get("predicate", {}).get("value", "")
        weight = row.get("weight", {}).get("value", "1")
        
        relations.append({
            "predicate": predicate,
            "weight": float(weight) if weight else 1.0
        })
    
    return relations


def analyze_relations_by_section(
    concepts: List[Dict[str, Any]],
    graph_engine: GraphQueryEngine
) -> Dict[str, Any]:
    """Section ID별 관계 통계 분석.
    
    Args:
        concepts: 개념 정보 리스트
        graph_engine: GraphQueryEngine 인스턴스
        
    Returns:
        통계 정보 딕셔너리
    """
    grouped = group_by_section_id(concepts)
    
    stats = {
        "total_sections": len(grouped),
        "sections": {}
    }
    
    for section_id, concept_ids in grouped.items():
        unique_ids = list(set(concept_ids))
        
        potential_relations = len(unique_ids) * (len(unique_ids) - 1) // 2
        
        stats["sections"][str(section_id)] = {
            "concept_count": len(unique_ids),
            "potential_relations": potential_relations
        }
    
    return stats

