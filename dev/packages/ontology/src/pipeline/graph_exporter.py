"""Graph exporter for saving graph structure and descriptions."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

import networkx as nx
from SPARQLWrapper import SPARQLWrapper

from storage.graph_query_engine import GraphQueryEngine
from pipeline.ontology_graph_manager import OntologyGraphManager
from backup.graph_backup import export_graphdb


class GraphExporter:
    """그래프 구조 및 description 저장."""
    
    def __init__(
        self,
        graph_engine: GraphQueryEngine,
        graph_manager: OntologyGraphManager
    ) -> None:
        """GraphExporter 초기화.
        
        Args:
            graph_engine: GraphQueryEngine 인스턴스
            graph_manager: OntologyGraphManager 인스턴스
        """
        self.graph_engine = graph_engine
        self.graph_manager = graph_manager
    
    def export_all(
        self,
        graph: nx.DiGraph,
        output_dir: Path,
        timestamp: Optional[str] = None
    ) -> Dict[str, str]:
        """모든 형식으로 그래프 저장.
        
        Args:
            graph: 저장할 그래프
            output_dir: 출력 디렉토리
            timestamp: 타임스탬프 (없으면 자동 생성)
            
        Returns:
            생성된 파일 경로 딕셔너리
        """
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        files = {}
        
        json_path = output_dir / f"graph_structure_{timestamp}.json"
        self.export_graph_to_json(graph, json_path)
        files["json"] = str(json_path)
        
        descriptions_path = output_dir / f"descriptions_{timestamp}.json"
        self.export_descriptions(descriptions_path)
        files["descriptions"] = str(descriptions_path)
        
        ttl_path = output_dir / f"graph_structure_{timestamp}.ttl"
        self.export_graph_to_ttl(ttl_path)
        files["ttl"] = str(ttl_path)
        
        return files
    
    def export_graph_to_json(
        self,
        graph: nx.DiGraph,
        output_path: Path
    ) -> None:
        """그래프 구조를 JSON으로 저장.
        
        Args:
            graph: 저장할 그래프
            output_path: 출력 파일 경로
        """
        nodes = []
        edges = []
        
        for node in graph.nodes():
            node_data = {
                "concept_id": node,
                "children": list(graph.successors(node)),
                "parents": list(graph.predecessors(node))
            }
            nodes.append(node_data)
        
        for parent, child in graph.edges():
            edges.append({
                "parent": parent,
                "child": child
            })
        
        data = {
            "root_concept": self.graph_manager.root_concept,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "nodes": nodes,
            "edges": edges,
            "exported_at": datetime.now().isoformat()
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"그래프 JSON 저장 완료: {output_path}")
    
    def export_graph_to_ttl(self, output_path: Path) -> None:
        """그래프를 TTL 형식으로 저장.
        
        Args:
            output_path: 출력 파일 경로
        """
        export_graphdb(self.graph_engine.endpoint_url, str(output_path))
        print(f"그래프 TTL 저장 완료: {output_path}")
    
    def export_descriptions(self, output_path: Path) -> None:
        """각 개념의 description을 JSON으로 저장.
        
        Args:
            output_path: 출력 파일 경로
        """
        query = """
        PREFIX llm: <http://example.org/llm-ontology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        
        SELECT ?concept ?label ?description
        WHERE {
            ?conceptUri a owl:Class .
            ?conceptUri rdfs:label ?label .
            OPTIONAL { ?conceptUri llm:description ?description . }
            
            BIND(REPLACE(STR(?conceptUri), "http://example.org/llm-ontology#", "") AS ?concept)
        }
        """
        
        results = self.graph_engine.query(query)
        
        descriptions = {}
        for row in results:
            concept_id = row.get("concept", {}).get("value", "")
            label = row.get("label", {}).get("value", "")
            description = row.get("description", {}).get("value", "")
            
            if concept_id:
                descriptions[concept_id] = {
                    "label": label,
                    "description": description or ""
                }
        
        data = {
            "total_concepts": len(descriptions),
            "exported_at": datetime.now().isoformat(),
            "descriptions": descriptions
        }
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Description JSON 저장 완료: {output_path}")

