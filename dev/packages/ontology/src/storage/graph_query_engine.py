"""SPARQL query engine for graph database."""

from typing import Dict, Any, List
from SPARQLWrapper import SPARQLWrapper, JSON


class GraphQueryEngine:
    """SPARQL 쿼리 엔진."""

    def __init__(self, endpoint_url: str) -> None:
        """GraphDB 엔드포인트 URL로 초기화.
        
        Args:
            endpoint_url: GraphDB SPARQL 엔드포인트 URL
        """
        self.endpoint_url = endpoint_url
        self.sparql = SPARQLWrapper(endpoint_url)
        self.sparql.setReturnFormat(JSON)

    def query(self, sparql_query: str) -> List[Dict[str, Any]]:
        """SPARQL 쿼리 실행.
        
        Args:
            sparql_query: 실행할 SPARQL 쿼리 문자열
            
        Returns:
            쿼리 결과 리스트
        """
        self.sparql.setQuery(sparql_query)
        results = self.sparql.query().convert()
        
        if "results" in results and "bindings" in results["results"]:
            return results["results"]["bindings"]
        return []

    def update(self, sparql_update: str) -> None:
        """SPARQL UPDATE 실행.
        
        Args:
            sparql_update: 실행할 SPARQL UPDATE 문자열
        """
        update_endpoint = self.endpoint_url.replace("/sparql", "/statements")
        sparql = SPARQLWrapper(update_endpoint)
        sparql.setMethod("POST")
        sparql.setQuery(sparql_update)
        sparql.query()

    def add_triple(
        self, 
        subject: str, 
        predicate: str, 
        obj: str,
        is_literal: bool = False
    ) -> None:
        """Triple을 그래프 DB에 추가.
        
        Args:
            subject: 주어 (URI 형식)
            predicate: 서술어 (URI 형식)
            obj: 목적어 (URI 또는 리터럴)
            is_literal: obj가 리터럴인지 여부
        """
        if is_literal:
            obj_str = f'"{obj}"'
        else:
            obj_str = f"<{obj}>"
        
        query = f"""
        PREFIX llm: <http://example.org/llm-ontology#>
        INSERT DATA {{
            <{subject}> <{predicate}> {obj_str} .
        }}
        """
        self.update(query)

    def add_concept(
        self,
        concept_id: str,
        label: str,
        parent: str,
        description: str
    ) -> None:
        """새 개념을 그래프 DB에 추가.
        
        Args:
            concept_id: 개념 ID
            label: 개념 레이블
            parent: 부모 개념 ID
            description: 개념 설명
        """
        query = f"""
        PREFIX llm: <http://example.org/llm-ontology#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        INSERT DATA {{
            llm:{concept_id} a owl:Class ;
                rdfs:label "{label}"@en ;
                rdfs:subClassOf llm:{parent} ;
                llm:description "{description}" .
        }}
        """
        self.update(query)

    def concept_exists(self, concept_id: str) -> bool:
        """개념이 GraphDB에 존재하는지 확인.
        
        Args:
            concept_id: 개념 ID
            
        Returns:
            존재 여부
        """
        query = f"""
        PREFIX llm: <http://example.org/llm-ontology#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        
        ASK {{
            llm:{concept_id} a owl:Class .
        }}
        """
        self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        return results.get("boolean", False)

    def update_description(self, concept_id: str, description: str) -> None:
        """개념의 description 업데이트.
        
        Args:
            concept_id: 개념 ID
            description: 새 설명
        """
        query = f"""
        PREFIX llm: <http://example.org/llm-ontology#>
        
        DELETE {{
            llm:{concept_id} llm:description ?old .
        }}
        INSERT {{
            llm:{concept_id} llm:description "{description}" .
        }}
        WHERE {{
            OPTIONAL {{ llm:{concept_id} llm:description ?old . }}
        }}
        """
        self.update(query)

    def add_relation(
        self, 
        concept1: str, 
        concept2: str,
        weight: float = 1.0
    ) -> None:
        """두 개념 간 관계 추가 (양방향).
        
        Args:
            concept1: 첫 번째 개념 ID
            concept2: 두 번째 개념 ID
            weight: 관계 가중치
        """
        query = f"""
        PREFIX llm: <http://example.org/llm-ontology#>
        
        INSERT DATA {{
            llm:{concept1} llm:related llm:{concept2} .
            llm:{concept2} llm:related llm:{concept1} .
        }}
        """
        self.update(query)

    def update_relation_weight(
        self, 
        subject: str, 
        predicate: str, 
        obj: str, 
        weight: float
    ) -> None:
        """Relation의 weight를 업데이트.
        
        Args:
            subject: 주어
            predicate: 서술어
            obj: 목적어
            weight: 업데이트할 weight 값
        """
        query = f"""
        PREFIX llm: <http://example.org/llm-ontology#>
        
        DELETE {{
            llm:{subject} llm:{predicate} llm:{obj} .
        }}
        INSERT {{
            llm:{subject} llm:{predicate} llm:{obj} .
        }}
        WHERE {{
            llm:{subject} llm:{predicate} llm:{obj} .
        }}
        """
        self.update(query)

