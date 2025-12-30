"""Common utilities for ontology package."""

from typing import Dict, List, Tuple
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, Literal
from rdflib.term import URIRef


LLM = Namespace("http://example.org/llm-ontology#")
OWL = Namespace("http://www.w3.org/2002/07/owl#")


def load_ontology_graph(ttl_path: str) -> Graph:
    """TTL 파일을 RDF 그래프로 로드.
    
    Args:
        ttl_path: TTL 파일 경로
        
    Returns:
        RDF 그래프
    """
    graph = Graph()
    graph.parse(ttl_path, format="turtle")
    return graph


def load_ontology_descriptions(ttl_path: str) -> Dict[str, str]:
    """온톨로지에서 개념 description 추출.
    
    Args:
        ttl_path: TTL 파일 경로
        
    Returns:
        개념 ID와 description의 딕셔너리
    """
    graph = load_ontology_graph(ttl_path)
    descriptions = {}
    
    for subject in graph.subjects(RDF.type, OWL.Class):
        concept_id = str(subject).replace(str(LLM), "")
        desc_obj = graph.value(subject, LLM.description)
        if desc_obj:
            descriptions[concept_id] = str(desc_obj)
    
    return descriptions


def load_all_concepts(ttl_path: str) -> List[Dict[str, str]]:
    """온톨로지에서 모든 개념 정보 추출.
    
    Args:
        ttl_path: TTL 파일 경로
        
    Returns:
        개념 정보 리스트 (concept_id, label, parent, description)
    """
    graph = load_ontology_graph(ttl_path)
    concepts = []
    
    for subject in graph.subjects(RDF.type, OWL.Class):
        concept_id = str(subject).replace(str(LLM), "")
        
        label_obj = graph.value(subject, RDFS.label)
        label = str(label_obj) if label_obj else concept_id
        
        parent_obj = graph.value(subject, RDFS.subClassOf)
        parent = str(parent_obj).replace(str(LLM), "") if parent_obj else None
        
        desc_obj = graph.value(subject, LLM.description)
        description = str(desc_obj) if desc_obj else ""
        
        concepts.append({
            "concept_id": concept_id,
            "label": label,
            "parent": parent,
            "description": description
        })
    
    return concepts


def update_ttl_descriptions(ttl_path: str, descriptions: Dict[str, str]) -> None:
    """TTL 파일의 개념 description 업데이트.
    
    Args:
        ttl_path: TTL 파일 경로
        descriptions: 개념 ID와 새 description의 딕셔너리
    """
    graph = load_ontology_graph(ttl_path)
    
    for concept_id, description in descriptions.items():
        subject = URIRef(str(LLM) + concept_id)
        
        if (subject, RDF.type, OWL.Class) in graph:
            graph.remove((subject, LLM.description, None))
            graph.add((subject, LLM.description, Literal(description)))
    
    graph.serialize(destination=ttl_path, format="turtle")


def add_concept_to_ttl(
    ttl_path: str,
    concept_id: str,
    label: str,
    parent: str,
    description: str
) -> None:
    """TTL 파일에 새 개념 추가.
    
    Args:
        ttl_path: TTL 파일 경로
        concept_id: 개념 ID
        label: 개념 레이블
        parent: 부모 개념 ID
        description: 개념 설명
    """
    graph = load_ontology_graph(ttl_path)
    
    subject = URIRef(str(LLM) + concept_id)
    parent_uri = URIRef(str(LLM) + parent)
    
    graph.add((subject, RDF.type, OWL.Class))
    graph.add((subject, RDFS.label, Literal(label, lang="en")))
    graph.add((subject, RDFS.subClassOf, parent_uri))
    graph.add((subject, LLM.description, Literal(description)))
    
    graph.serialize(destination=ttl_path, format="turtle")


def extract_keywords_from_document(document: str) -> List[str]:
    """문서에서 키워드 추출.
    
    Args:
        document: 문서 텍스트
        
    Returns:
        추출된 키워드 리스트
    """
    pass

