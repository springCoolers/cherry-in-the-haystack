# 중복제거 파이프라인 (Deduplication Pipeline)

## 개요

기존 LangGraph 워크플로우에 해시 기반 중복제거를 **노드 패턴으로 자연스럽게 통합**합니다.

### 핵심 결정사항

- **LangGraph 노드로 통합**: 별도 서비스가 아닌 `workflow/nodes/` 패턴 유지
- **2단계 중복제거**: 청크 해시/임베딩 체크 → 아이디어 추출 → concept 정확 매칭
- **실시간 처리**: SHA256 + SimHash 기반 (빠름)
- **배치 처리**: OpenAI 임베딩 (별도 스크립트)

---

## 파이프라인 구조

### 기존 LangGraph 구조

```
extract_idea → check_duplicate → save/skip → END
```

### 새로운 LangGraph 구조

```
check_chunk_duplicate → extract_idea → check_idea_duplicate → save/skip → END
     ↓ (중복)                                    ↓ (중복)
    skip ──────────────────────────────────────→ END
```

**왜 extract_idea 전인가?**

- 청크가 이전에 저장된 청크와 중복이면 **LLM 호출 자체를 스킵** → 비용 절감
- 첫 번째 청크는 비교 대상이 없으므로 항상 통과
- 두 번째 청크부터 DB에 저장된 해시와 비교

---

## 파일 구조

### src/dedup/ (별도 모듈로 분리)

```
src/dedup/
    __init__.py
    hash_utils.py         # SHA256, SimHash 해시 계산
    embedding_utils.py    # OpenAI 임베딩 생성
    dedup_service.py      # DeduplicationService 클래스

scripts/
    generate_embeddings.py   # 배치 임베딩 생성 CLI
```

**왜 src/dedup/ 분리인가?**

- `dedup_service.py`는 DB 세션을 받아 쿼리를 실행하는 **서비스 클래스** → `utils/`(순수 함수)와 성격이 다름
- 중복제거 도메인이 명확히 분리됨 (해시, 임베딩, 서비스가 한 곳에)
- 향후 임베딩 배치 처리, 유사도 검색 등 확장 시 관리 용이
- `workflow/nodes/check_duplicate.py`는 이 모듈을 **import해서 사용**하는 LangGraph 노드 역할만 담당

### 수정된 파일

| 파일 | 변경 내용 |
|------|-----------|
| `src/db/models.py` | paragraph_hash, simhash64 필드 + ParagraphEmbedding 모델 |
| `src/model/schemas.py` | HierarchicalChunk에 해시 필드 추가 |
| `src/workflow/nodes/__init__.py` | 새 노드 export 추가 |
| `src/workflow/nodes/chunk_paragraphs.py` | 청킹 시 해시 계산 |
| `src/workflow/nodes/check_duplicate.py` | 2개 노드로 분리 (chunk/idea) |
| `src/workflow/nodes/save_to_db.py` | 해시 필드 저장 |
| `src/workflow/workflow.py` | 그래프 구조 수정 |
| `src/workflow/state.py` | `enable_semantic_dedup`, `semantic_threshold` 필드 추가 |

---

## 현재 구현 상태

| 구성요소 | 상태 | 파일 |
|---------|------|------|
| SHA256 해시 | ✅ 완료 | `src/dedup/hash_utils.py` |
| SimHash 퍼지 매칭 | ✅ 완료 | `src/dedup/hash_utils.py` |
| DeduplicationService | ✅ 완료 | `src/dedup/dedup_service.py` |
| 청크 해시 저장 | ✅ 완료 | `chunk_paragraphs.py`, `save_to_db.py` |
| LangGraph 노드 통합 | ✅ 완료 | `check_duplicate.py`, `workflow.py` |
| 배치 임베딩 생성 | ✅ 완료 | `scripts/generate_embeddings.py` |
| 임베딩 기반 중복제거 | ✅ 완료 | `check_duplicate.py` (하이브리드) |

---

## 파이프라인 흐름

```
check_chunk_duplicate
    │
    ├── 1단계: 해시 체크 (SHA256 + SimHash)
    │       ├── 중복 → skip → END
    │       └── 통과 ↓
    │
    ├── 2단계: 임베딩 체크 (enable_semantic_dedup=True 시)
    │       ├── 유사 (>=0.95) → skip → END
    │       └── 통과 ↓
    │
    └── extract_idea
            │
            ▼
        check_idea_duplicate (concept 정확 매칭)
            │
            ├── 중복 → skip → END
            │
            └── 신규 → save_to_db → END
```

### 각 단계 설명

| 단계 | 체크 대상 | 방식 | 비용 |
|-----|----------|------|------|
| 1단계 | 청크 텍스트 | SHA256 정확 + SimHash 퍼지 | 무료 |
| 2단계 | 청크 텍스트 | OpenAI 임베딩 유사도 | API 호출 |
| 3단계 | 추출된 concept | DB 정확 매칭 | 무료 |

### 상세 동작

#### check_chunk_duplicate (청크 레벨)

```python
# src/workflow/nodes/check_duplicate.py

def check_chunk_duplicate(state: PipelineState) -> PipelineState:
    # 1단계: 해시 체크 (빠름)
    dedup_service = DeduplicationService(session, fuzzy_threshold=6)
    result = dedup_service.check_duplicate(text, book_id)

    if result.is_duplicate:
        return {..., "is_chunk_duplicate": True}

    # 2단계: 임베딩 체크 (활성화 시에만)
    if enable_semantic:
        semantic_result = dedup_service.find_semantic_duplicate(text, book_id)
        if semantic_result:
            return {..., "is_chunk_duplicate": True, "chunk_duplicate_type": "semantic"}
```

- **1단계**: `DeduplicationService.check_duplicate()` → SHA256 + SimHash 해시 비교
- **2단계**: `DeduplicationService.find_semantic_duplicate()` → 임베딩 코사인 유사도

#### check_idea_duplicate (아이디어 레벨)

```python
# src/workflow/nodes/check_duplicate.py

def check_idea_duplicate(state: PipelineState) -> PipelineState:
    concept = extracted_idea.concept  # LLM이 추출한 concept

    # DB에서 동일 concept 검색 (문자열 정확 매칭)
    existing = session.query(KeyIdea).filter(
        KeyIdea.core_idea_text == concept
    ).first()

    if existing:
        return {..., "is_idea_duplicate": True}
```

- LLM이 추출한 `concept` 값을 가져옴
- `KeyIdea.core_idea_text == concept` 쿼리로 DB 검색
- 동일한 문자열이 있으면 중복 → 스킵

#### KeyIdea 저장 로직

```python
# src/workflow/nodes/save_to_db.py

def save_to_db(state: PipelineState) -> PipelineState:
    # concept 추출
    concept = extracted_idea.concept

    # KeyIdea 저장
    db_idea = KeyIdea(
        chunk_id=db_chunk.id,
        book_id=book_id,
        core_idea_text=concept,  # LLM이 추출한 concept 저장
    )
```

#### 왜 concept은 문자열 매칭인가?

| 특성 | 설명 |
|------|------|
| **concept의 성격** | LLM이 정제한 짧은 핵심 개념 (예: `"Self-attention mechanism"`) |
| **중복 발생 시나리오** | 같은 책에서 같은 concept이 여러 번 나올 수 있음 |
| **원하는 동작** | **정확히 같은 개념**만 스킵하고 싶음 |
| **왜 문자열 매칭?** | 의미적으로 비슷하지만 다른 개념은 저장해야 함 |

**예시:**
```
concept1: "Transformer"
concept2: "Transformer architecture"
→ 다른 문자열 → 둘 다 저장 ✅

concept1: "Self-attention"
concept2: "Self-attention"
→ 동일 문자열 → 첫 번째만 저장, 두 번째는 스킵
```

**왜 임베딩이 아닌가?**
- 임베딩으로 비교하면 `"Transformer"`와 `"Transformer architecture"`가 유사하다고 판단될 수 있음
- 하지만 이 두 개념은 서로 다른 관점을 담고 있을 수 있으므로 **둘 다 저장**하는 것이 적절

---

## 왜 해시와 임베딩을 함께 사용하는가?

### Q: 임베딩이 있으면 해시가 필요 없지 않나?

A: 임베딩만으로도 중복 탐지가 가능하지만, **비용과 속도** 문제가 있습니다.

| 방식 | 속도 | 비용 | 탐지 범위 |
|-----|------|------|----------|
| SHA256 | 즉시 (μs) | 무료 | 완전 동일 |
| SimHash | 즉시 (μs) | 무료 | 글자 변형 |
| 임베딩 | 느림 (~200ms) | $0.00002/1K tokens | 의미적 유사 |

**100개 청크 처리 시:**
- 임베딩만: 100 API 호출 → ~20초, ~$0.004
- 해시+임베딩: 해시에서 80개 스킵 → 20 API 호출 → ~4초, ~$0.0008

→ **해시 = 빠른 1차 필터, 임베딩 = 정밀 2차 필터**

### Q: 해시로 중복이라 판단된 것을 임베딩으로 재확인하면 안 되나?

A: 그것도 가능하지만, **목적이 다릅니다.**

| 방향 | 흐름 | 목적 | 결과 |
|-----|------|------|------|
| **현재 기획** | 해시 통과 → 임베딩 체크 | 해시가 놓친 중복 잡기 | 더 많이 스킵 (엄격) |
| 대안 | 해시 중복 → 임베딩 재확인 | 해시 오탐 방지 | 더 많이 저장 (관대) |

**현재 기획을 선택한 이유:**
- 해시(SHA256)는 정확함 → 오탐(false positive)이 거의 없음
- SimHash는 오탐 가능성 있지만, threshold=6이면 상당히 유사한 경우만 탐지
- 따라서 **해시 오탐 방지보다 해시가 놓친 의미적 중복 잡기**가 더 유용

### Q: SimHash도 유사도를 보는데 임베딩이 왜 필요한가?

A: SimHash는 **글자 수준** 유사도, 임베딩은 **의미 수준** 유사도입니다.

```
예시 1: SimHash가 잡는 경우
  "Transformer는 attention을 사용한다"
  "Transformer는 attention을 활용한다"
  → 글자 대부분 동일 → SimHash 거리 작음 ✅

예시 2: 임베딩만 잡는 경우
  "Transformer는 attention 메커니즘을 사용한다"
  "Attention mechanism이 Transformer의 핵심이다"
  → 글자 순서 다름 → SimHash 거리 큼 ❌
  → 의미 동일 → 임베딩 유사도 높음 (0.92+) ✅
```

---

## 사용 방법

### 기본 사용 (해시만)

```python
from src.workflow.workflow import run_pdf_pipeline

# 해시만 사용 (기본, 빠름)
run_pdf_pipeline("book.pdf")
```

### 임베딩 기반 중복제거 활성화

```python
# 해시 + 임베딩 사용 (정밀, API 비용 발생)
run_pdf_pipeline("book.pdf", enable_semantic_dedup=True)

# 임계값 조정 (더 관대한 중복 탐지)
run_pdf_pipeline("book.pdf", enable_semantic_dedup=True, semantic_threshold=0.90)
```

### 배치 임베딩 생성

```bash
python scripts/generate_embeddings.py --book-id 1 --batch-size 100
```

---

## 통계 필드

```python
stats = {
    # 기존
    "chunk_duplicates_skipped": 0,   # 해시 기반
    "idea_duplicates_skipped": 0,    # concept 기반

    # 신규 (임베딩 활성화 시)
    "semantic_duplicates_skipped": 0,  # 임베딩 기반
}
```

### 출력 예시

```
============================================================
📊 처리 요약
============================================================
감지 방법: toc
총 챕터: 10
총 섹션: 45
완료: 10
실패: 0
총 문단: 320
추출된 아이디어: 280
────────────────────────────────────────
중복 스킵 상세:
  해시 기반: 15
  임베딩 기반: 8
  아이디어 기반: 17
  총 스킵: 40
============================================================
```

---

## DB 인프라

### 필요한 테이블

```sql
-- paragraph_chunks 테이블 (해시 필드 추가됨)
ALTER TABLE paragraph_chunks ADD COLUMN paragraph_hash VARCHAR(64);
ALTER TABLE paragraph_chunks ADD COLUMN simhash64 BIGINT;

-- paragraph_embeddings 테이블 (pgvector 필요)
CREATE TABLE paragraph_embeddings (
    id SERIAL PRIMARY KEY,
    chunk_id INTEGER REFERENCES paragraph_chunks(id) UNIQUE,
    book_id INTEGER REFERENCES books(id),
    embedding vector(1536),
    model_name VARCHAR(100) DEFAULT 'text-embedding-3-small'
);

-- pgvector 인덱스
CREATE INDEX ON paragraph_embeddings
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

### 왜 PostgreSQL + pgvector가 필요한가?

| 기능 | SQLite | PostgreSQL + pgvector |
|------|--------|----------------------|
| 해시 중복체크 | ✅ 가능 | ✅ 가능 |
| 임베딩 저장 | ❌ 불가 (vector 타입 없음) | ✅ `vector(1536)` 타입 |
| 코사인 유사도 검색 | ❌ 불가 | ✅ `<=>` 연산자 |
| 성능 인덱스 | ❌ | ✅ IVFFlat 인덱스 |

---

## 비용 분석

### OpenAI text-embedding-3-small

| 항목 | 값 |
|-----|---|
| 가격 | $0.00002 / 1K tokens |
| 평균 청크 | ~200 tokens |
| 1000 청크 | ~$0.004 |
| 책 1권 (500청크) | ~$0.002 |

**결론:** 배치 임베딩 생성 비용은 무시할 수준

---

## 개발 환경 설정

### 1. 가상환경 설정

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경변수 설정 (.env)

```
DATABASE_URL=postgresql://user:password@localhost:5433/pdf_extractor
OPENAI_API_KEY=sk-...
```

### 3. PostgreSQL 서버 실행

#### Docker 사용 (권장)

```bash
docker run -d \
  --name pdf-extractor-db \
  -e POSTGRES_PASSWORD=yourpassword \
  -e POSTGRES_DB=pdf_extractor \
  -p 5433:5432 \
  pgvector/pgvector:pg16
```

#### macOS 로컬 설치

```bash
brew install postgresql@16
brew services start postgresql@16
brew install pgvector
```

#### 클라우드 DB

- Supabase, Neon, Railway 등에서 무료 PostgreSQL 제공
- pgvector 지원되는 서비스 선택

### 4. 테스트 실행

```bash
source venv/bin/activate
python3 tests/test_deduplication.py
```

---

## 테스트 결과

| 테스트 | 서버 없이 | 서버 있을 때 |
|--------|----------|-------------|
| hash_utils | ✅ 통과 | ✅ 통과 |
| embedding_utils | ✅ 통과 | ✅ 통과 |
| pipeline_state | ✅ 통과 | ✅ 통과 |
| workflow_options | ✅ 통과 | ✅ 통과 |
| dedup_service | ⏭️ 스킵 | 테스트 가능 |
| workflow_integration | ⏭️ 스킵 | 테스트 가능 |

서버 없이도 **핵심 로직(해시, 임베딩, 파이프라인 구조)**은 모두 테스트 통과합니다.

---

## 테스트 체크리스트

- [x] hash_utils: SHA256 결정론적 확인
- [x] hash_utils: SimHash 해밍 거리 계산
- [x] check_chunk_duplicate 노드: 정확/퍼지 중복 탐지
- [x] check_idea_duplicate 노드: concept 정확 매칭
- [x] PipelineState: 새 필드 존재 확인
- [x] run_pdf_pipeline: 옵션 파라미터 확인
- [ ] generate_embeddings.py: 특정 book_id 임베딩 생성 (DB 필요)
- [ ] pgvector 쿼리: 코사인 유사도 계산 정확성 (DB 필요)
- [ ] dedup_service: enable_semantic=True 동작 확인 (DB 필요)

---

## 버그 수정 이력

### hamming_distance() 함수 버그 (2024-12-27)

**수정 전 (버그):**
```python
def hamming_distance(hash1: int, hash2: int) -> int:
    xor = xor & 0xFFFFFFFFFFFFFFFF  # xor 정의 안됨!
    return bin(xor).count('1')
```

**수정 후:**
```python
def hamming_distance(hash1: int, hash2: int) -> int:
    xor = hash1 ^ hash2  # 추가됨
    xor = xor & 0xFFFFFFFFFFFFFFFF
    return bin(xor).count('1')
```

---

## 코드 이해를 위한 Python 문법

이 프로젝트에서 자주 사용되는 Python 패턴들을 정리합니다.

### 딕셔너리 언패킹 (`{**state, ...}`)

```python
state = {"a": 1, "b": 2, "book_id": 123}

# 새 딕셔너리 생성 (원본 유지 + 새 키 추가)
result = {**state, "is_chunk_duplicate": False}
# → {"a": 1, "b": 2, "book_id": 123, "is_chunk_duplicate": False}
```

**왜 이렇게 하나?**

LangGraph 노드는 **불변성(Immutability)**을 유지해야 합니다:

```python
# ❌ 원본 수정 (side effect 발생)
state["is_chunk_duplicate"] = False
return state

# ✅ 새 딕셔너리 생성 (원본 유지)
return {**state, "is_chunk_duplicate": False}
```

---

### 객체 vs 딕셔너리

```python
# 딕셔너리 (dict) - 키-값 쌍의 자료구조
chunk_dict = {"text": "Transformer는...", "chapter_id": 1}
chunk_dict["text"]      # 키로 접근
chunk_dict.get("text")  # 키로 접근 (없으면 None 반환)

# 객체 (class) - 속성을 가진 인스턴스
class HierarchicalChunk:
    def __init__(self, text, chapter_id):
        self.text = text
        self.chapter_id = chapter_id

chunk_obj = HierarchicalChunk(text="Transformer는...", chapter_id=1)
chunk_obj.text  # 속성으로 접근 (점 표기법)
```

| 구분 | 딕셔너리 | 객체 |
|------|----------|------|
| 생성 | `{"key": value}` | `ClassName(...)` |
| 접근 | `d["key"]` 또는 `d.get("key")` | `obj.attribute` |
| 타입 | `dict` | 클래스명 (예: `HierarchicalChunk`) |

---

### hasattr 함수

```python
hasattr(객체, "속성명")  # 해당 속성이 있으면 True, 없으면 False
```

```python
chunk_obj = HierarchicalChunk(text="...", chapter_id=1)
hasattr(chunk_obj, "text")       # True - text 속성 있음
hasattr(chunk_obj, "author")     # False - author 속성 없음

chunk_dict = {"text": "...", "chapter_id": 1}
hasattr(chunk_dict, "text")      # False - 딕셔너리는 .text 속성이 없음
```

---

### get 함수 (딕셔너리)

```python
딕셔너리.get("키", 기본값)  # 키가 있으면 값 반환, 없으면 기본값 반환
```

```python
chunk_dict = {"text": "Transformer는...", "chapter_id": 1}

chunk_dict.get("text", "")       # → "Transformer는..."
chunk_dict.get("author", "없음")  # → "없음" (키가 없어서 기본값)
chunk_dict["author"]             # → KeyError 발생! (키 없음)
```

---

### 유연한 타입 처리 패턴

```python
text = current_chunk.text if hasattr(current_chunk, 'text') else current_chunk.get('text', '')
```

풀어서 쓰면:

```python
if hasattr(current_chunk, 'text'):
    # current_chunk가 객체인 경우
    text = current_chunk.text
else:
    # current_chunk가 딕셔너리인 경우
    text = current_chunk.get('text', '')
```

**왜 두 가지 타입을 모두 처리하나?**

`current_chunk`가 **두 가지 형태**로 들어올 수 있기 때문:

```python
# 객체로 전달되는 경우
state["current_chunk"] = HierarchicalChunk(text="...", chapter_id=1)

# 딕셔너리로 전달되는 경우
state["current_chunk"] = {"text": "...", "chapter_id": 1}
```

---

## 타입 구조 정리

### 노드 함수의 입출력

```python
def check_chunk_duplicate(state: PipelineState) -> PipelineState:
```

| 역할 | 타입 | 설명 |
|------|------|------|
| 입력 | `PipelineState` | 파이프라인 전체 상태 (딕셔너리) |
| 출력 | `PipelineState` | 업데이트된 상태 (딕셔너리) |

### PipelineState 구조

```python
state = {
    "current_chunk": HierarchicalChunk(...),  # 현재 처리 중인 청크
    "book_id": 123,
    "enable_semantic_dedup": False,
    "stats": {"chunk_duplicates_skipped": 0},
    "extracted_idea": ExtractedIdea(...),     # LLM 추출 결과
    ...
}
```

### 타입 흐름도

```
┌─────────────────────────────────────────────────────────┐
│ PipelineState (전체 상태 딕셔너리)                        │
│   ├── current_chunk: HierarchicalChunk (청크 객체)       │
│   ├── book_id: int                                      │
│   ├── extracted_idea: ExtractedIdea (LLM 결과)          │
│   └── stats: dict                                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ DeduplicationService (서비스 클래스)                     │
│   └── check_duplicate(text) → DeduplicationResult       │
│                                  ├── is_duplicate: bool │
│                                  └── duplicate_type: str│
└─────────────────────────────────────────────────────────┘
```

### 각 타입의 역할

| 타입 | 정의 위치 | 역할 |
|------|----------|------|
| `PipelineState` | `state.py` | 노드 간 데이터 전달 (딕셔너리) |
| `HierarchicalChunk` | `schemas.py` | 문단 청크 데이터 (dataclass) |
| `ExtractedIdea` | `schemas.py` | LLM 추출 결과 (Pydantic) |
| `DeduplicationService` | `dedup_service.py` | 중복체크 로직 (클래스) |
| `DeduplicationResult` | `dedup_service.py` | 중복체크 결과 (dataclass) |

### DeduplicationResult 구조

```python
@dataclass
class DeduplicationResult:
    """중복 체크 결과"""
    is_duplicate: bool                        # 중복인지 여부
    duplicate_type: Optional[str] = None      # 'exact', 'fuzzy', 'semantic'
    existing_chunk_id: Optional[int] = None   # 중복된 기존 청크 ID
    similarity_score: Optional[float] = None  # 유사도 점수
    hamming_distance: Optional[int] = None    # SimHash 해밍 거리
```

### 간단 요약

```
PipelineState    ← 전체 상태를 담는 큰 바구니 (dict)
  ↓
current_chunk    ← 바구니에서 꺼낸 청크 (객체)
  ↓
text             ← 청크에서 꺼낸 텍스트 (str)
  ↓
DeduplicationService.check_duplicate(text)
  ↓
DeduplicationResult ← 중복 체크 결과 (객체)
  ├── is_duplicate: True/False
  └── duplicate_type: "exact"/"fuzzy"/"semantic"
```
