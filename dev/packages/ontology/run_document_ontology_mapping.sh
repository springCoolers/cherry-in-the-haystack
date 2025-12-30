#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

GRAPH_ENDPOINT="${GRAPH_ENDPOINT:-http://localhost:7200/repositories/llm-ontology}"
VECTOR_DB_PATH="${VECTOR_DB_PATH:-$PROJECT_ROOT/db/vector_store}"
NEW_CONCEPT_DB="${NEW_CONCEPT_DB:-$PROJECT_ROOT/db/new_concepts.db}"
BACKUP_DIR="${BACKUP_DIR:-$PROJECT_ROOT/backups}"
SNAPSHOT_DIR="${SNAPSHOT_DIR:-$PROJECT_ROOT/snapshots}"

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    --input FILE        JSONL 입력 파일 경로 (필수)
    --sync-only         동기화만 실행 (처리 생략)
    --skip-backup       백업 생략 (Graph DB + ChromaDB)
    --skip-sync         ChromaDB 동기화 생략
    -h, --help          도움말 표시

Environment Variables:
    GRAPH_ENDPOINT      Graph DB endpoint (기본: http://localhost:7200/repositories/llm-ontology)
    VECTOR_DB_PATH      Vector DB 경로 (기본: db/vector_store)
    NEW_CONCEPT_DB      신규 개념 DB 경로 (기본: db/new_concepts.db)
    BACKUP_DIR          백업 디렉토리 (기본: backups)
    SNAPSHOT_DIR        스냅샷 디렉토리 (기본: snapshots)

Examples:
    # 기본 실행 (백업 + 동기화 + 처리)
    $0 --input concepts.jsonl

    # 백업 생략
    $0 --input concepts.jsonl --skip-backup

    # 동기화만 실행
    $0 --sync-only

EOF
}

INPUT_FILE=""
SYNC_ONLY=false
SKIP_BACKUP=false
SKIP_SYNC=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --input)
            INPUT_FILE="$2"
            shift 2
            ;;
        --sync-only)
            SYNC_ONLY=true
            shift
            ;;
        --skip-backup)
            SKIP_BACKUP=true
            shift
            ;;
        --skip-sync)
            SKIP_SYNC=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

if [ "$SYNC_ONLY" = false ] && [ -z "$INPUT_FILE" ]; then
    echo "Error: --input is required"
    show_usage
    exit 1
fi

cd "$PROJECT_ROOT"

echo "======================================"
echo "Ontology Processing Pipeline"
echo "======================================"
echo ""

if [ "$SKIP_BACKUP" = false ]; then
    echo "Step 1: 백업 (Graph DB + ChromaDB)"
    echo "--------------------------------------"
    uv run python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('$PROJECT_ROOT') / 'src'))

from backup.graph_backup import create_backup
from backup.chromadb_snapshot import create_snapshot

print('Graph DB 백업 중...')
create_backup('$GRAPH_ENDPOINT', '$BACKUP_DIR')

print('\\nChromaDB 스냅샷 생성 중...')
create_snapshot('$VECTOR_DB_PATH', '$SNAPSHOT_DIR')
"
    echo ""
fi

if [ "$SKIP_SYNC" = false ]; then
    echo "Step 2: Graph DB ↔ ChromaDB 동기화"
    echo "--------------------------------------"
    uv run python -c "
import sys
from pathlib import Path
sys.path.insert(0, str(Path('$PROJECT_ROOT') / 'src'))

from storage.graph_query_engine import GraphQueryEngine
from storage.vector_store import VectorStore
from backup.chromadb_sync import sync_graphdb_to_chromadb

graph_engine = GraphQueryEngine('$GRAPH_ENDPOINT')
vector_store = VectorStore('$VECTOR_DB_PATH')

added = sync_graphdb_to_chromadb(graph_engine, vector_store)
print(f'동기화 완료: {added}개 개념 추가됨')
"
    echo ""
fi

if [ "$SYNC_ONLY" = true ]; then
    echo "======================================"
    echo "동기화 완료"
    echo "======================================"
    exit 0
fi

echo "Step 3: JSONL 처리 (개념 매핑)"
echo "--------------------------------------"
uv run python src/scripts/main.py \
    --input "$INPUT_FILE" \
    --graph-endpoint "$GRAPH_ENDPOINT" \
    --vector-db "$VECTOR_DB_PATH" \
    --new-concept-db "$NEW_CONCEPT_DB"

echo ""

echo "======================================"
echo "모든 작업 완료"
echo "======================================"

