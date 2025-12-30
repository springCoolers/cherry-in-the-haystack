"""Graph DB export and backup utilities."""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional

from SPARQLWrapper import SPARQLWrapper


def export_graphdb(endpoint: str, output_path: str) -> None:
    """Graph DB를 TTL 형식으로 export.
    
    Args:
        endpoint: SPARQL endpoint URL
        output_path: 저장할 파일 경로
    """
    sparql = SPARQLWrapper(endpoint)
    
    construct_query = """
    PREFIX llm: <http://example.org/llm-ontology#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    CONSTRUCT {
        ?s ?p ?o .
    }
    WHERE {
        ?s ?p ?o .
    }
    """
    
    sparql.setQuery(construct_query)
    sparql.setReturnFormat("turtle")
    
    results = sparql.query().convert()
    
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'wb') as f:
        f.write(results)


def create_backup(endpoint: str, backup_dir: str = "backups") -> str:
    """Graph DB 백업 생성.
    
    Args:
        endpoint: SPARQL endpoint URL
        backup_dir: 백업 디렉토리 경로
        
    Returns:
        생성된 백업 파일 경로
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"graphdb_{timestamp}.ttl"
    
    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)
    
    output_path = backup_path / filename
    
    print(f"Graph DB 백업 중: {output_path}")
    export_graphdb(endpoint, str(output_path))
    print(f"백업 완료: {output_path}")
    
    cleanup_old_backups(backup_dir, keep=10)
    
    return str(output_path)


def cleanup_old_backups(backup_dir: str, keep: int = 10) -> None:
    """오래된 백업 파일 정리.
    
    Args:
        backup_dir: 백업 디렉토리 경로
        keep: 유지할 백업 개수
    """
    backup_path = Path(backup_dir)
    
    if not backup_path.exists():
        return
    
    backup_files = sorted(
        backup_path.glob("graphdb_*.ttl"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )
    
    for old_file in backup_files[keep:]:
        print(f"오래된 백업 삭제: {old_file}")
        old_file.unlink()


def restore_from_backup(backup_file: str, endpoint: str) -> None:
    """백업에서 Graph DB 복원.
    
    Args:
        backup_file: 백업 파일 경로
        endpoint: SPARQL endpoint URL (statements endpoint)
    """
    with open(backup_file, 'r', encoding='utf-8') as f:
        ttl_data = f.read()
    
    update_endpoint = endpoint.replace("/sparql", "/statements")
    sparql = SPARQLWrapper(update_endpoint)
    sparql.setMethod("POST")
    
    sparql.setQuery(f"""
    PREFIX llm: <http://example.org/llm-ontology#>
    
    INSERT DATA {{
        {ttl_data}
    }}
    """)
    
    sparql.query()
    print(f"복원 완료: {backup_file}")

