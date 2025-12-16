"""Common utilities for ontology package."""

from typing import Dict, List


def load_ontology_descriptions(ttl_path: str) -> Dict[str, str]:
    """온톨로지에서 개념 description 추출.
    
    Args:
        ttl_path: TTL 파일 경로
        
    Returns:
        개념 ID와 description의 딕셔너리
    """
    # TODO: RDF 파싱하여 description 추출
    pass


def extract_keywords_from_document(document: str) -> List[str]:
    """문서에서 키워드 추출.
    
    Args:
        document: 문서 텍스트
        
    Returns:
        추출된 키워드 리스트
    """
    # TODO: 키워드 추출 로직
    pass

