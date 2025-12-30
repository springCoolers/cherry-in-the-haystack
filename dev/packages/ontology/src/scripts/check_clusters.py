#!/usr/bin/env python3
"""클러스터 DB 확인 스크립트."""

import sys
import sqlite3
from pathlib import Path
import argparse

def check_clusters(db_path: str):
    """클러스터 DB 확인."""
    if not Path(db_path).exists():
        print(f"❌ DB 파일이 없습니다: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"\n{'='*80}")
    print(f"클러스터 DB 확인: {db_path}")
    print(f"{'='*80}\n")
    
    # 1. new_concepts 테이블 확인
    print("📋 신규 개념 (new_concepts):")
    print("-" * 80)
    cursor.execute("SELECT COUNT(*) FROM new_concepts")
    concept_count = cursor.fetchone()[0]
    print(f"총 개념 수: {concept_count}개\n")
    
    if concept_count > 0:
        cursor.execute("SELECT id, concept, source, created_at FROM new_concepts ORDER BY id DESC LIMIT 10")
        print("최근 10개 개념:")
        for row in cursor.fetchall():
            print(f"  [{row[0]}] {row[1][:50]:50} | source: {row[2]:20} | {row[3]}")
    
    print()
    
    # 2. concept_clusters 테이블 확인
    print("🔗 클러스터 (concept_clusters):")
    print("-" * 80)
    cursor.execute("SELECT COUNT(*) FROM concept_clusters")
    cluster_count = cursor.fetchone()[0]
    print(f"총 클러스터 수: {cluster_count}개\n")
    
    if cluster_count > 0:
        cursor.execute("SELECT id, cluster_name, concept_ids, created_at FROM concept_clusters ORDER BY id")
        for row in cursor.fetchall():
            cluster_id, cluster_name, concept_ids_str, created_at = row
            concept_ids = concept_ids_str.split(",") if concept_ids_str else []
            
            print(f"클러스터 ID: {cluster_id}")
            print(f"  이름: {cluster_name}")
            print(f"  개념 수: {len(concept_ids)}개")
            print(f"  개념 목록: {', '.join(concept_ids[:5])}{'...' if len(concept_ids) > 5 else ''}")
            print(f"  생성 시간: {created_at}")
            print()
    else:
        print("  클러스터가 없습니다.")
    
    print()
    
    # 3. clustering_metadata 테이블 확인
    print("📊 클러스터링 메타데이터 (clustering_metadata):")
    print("-" * 80)
    cursor.execute("SELECT key, value FROM clustering_metadata")
    metadata = cursor.fetchall()
    
    if metadata:
        for key, value in metadata:
            print(f"  {key}: {value}")
    else:
        print("  메타데이터가 없습니다.")
    
    print()
    
    # 4. 통계
    print("📈 통계:")
    print("-" * 80)
    
    # 클러스터별 개념 수 분포
    cursor.execute("SELECT concept_ids FROM concept_clusters")
    cluster_sizes = []
    for row in cursor.fetchall():
        concept_ids = row[0].split(",") if row[0] else []
        cluster_sizes.append(len(concept_ids))
    
    if cluster_sizes:
        print(f"클러스터 크기 분포:")
        print(f"  평균: {sum(cluster_sizes) / len(cluster_sizes):.1f}개")
        print(f"  최소: {min(cluster_sizes)}개")
        print(f"  최대: {max(cluster_sizes)}개")
        print(f"  5개 이상: {sum(1 for s in cluster_sizes if s >= 5)}개")
    
    conn.close()
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="클러스터 DB 확인")
    parser.add_argument(
        "--db",
        default="db/new_concepts.db",
        help="DB 파일 경로"
    )
    
    args = parser.parse_args()
    
    # 상대 경로를 절대 경로로 변환
    db_path = Path(__file__).parent.parent.parent / args.db
    
    check_clusters(str(db_path))

