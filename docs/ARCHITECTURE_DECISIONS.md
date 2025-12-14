# PDF 처리 파이프라인 아키텍처 변경 이력

이 문서는 PDF 처리 파이프라인의 아키텍처 변경 과정과 각 단계에서의 의사결정을 기록합니다.

---

## 목차
1. [초기 상태 (First Commit)](#1-초기-상태-first-commit)
2. [Phase 1: 페이지 → 챕터 기반 전환](#2-phase-1-페이지--챕터-기반-전환)
3. [Phase 2: 규칙 기반 → LLM 기반 청킹](#3-phase-2-규칙-기반--llm-기반-청킹)
4. [Phase 3: 섹션 메타데이터 추가](#4-phase-3-섹션-메타데이터-추가)
5. [전체 아키텍처 변화](#5-전체-아키텍처-변화)
6. [파일 변경 요약](#6-파일-변경-요약)
7. [핵심 의사결정 요약](#7-핵심-의사결정-요약)

---

## 1. 초기 상태 (First Commit)

### 아키텍처: 페이지 기반 처리

```
PDF → 페이지별 텍스트 추출 → 규칙 기반 문단 분할 → LLM 아이디어 추출 → DB 저장
```

### 핵심 파일 구조

| 파일 | 역할 | 한계 |
|------|------|------|
| `parser.py` | 페이지별 텍스트 추출 (`extract_page_text()`) | 페이지 경계에서 문장 잘림 |
| `chunker.py` | 규칙 기반 분할 (150-1000자, 5문장) | 의미 단위 무시, 챕터 컨텍스트 없음 |
| `schemas.py` | `Book`, `ParagraphChunk`, `KeyIdea` | 챕터 메타데이터 없음 |

### 초기 코드 예시

**schemas.py**:
```python
class ParagraphChunk(BaseModel):
    book_id: int
    page_number: int        # 페이지 기반
    paragraph_index: int
    body_text: str
    # 챕터 정보 없음!
```

**chunker.py**:
```python
MIN_PARAGRAPH_LENGTH = 150
MAX_PARAGRAPH_LENGTH = 1000
TARGET_SENTENCES = 5

def split_paragraphs(page_text: str) -> List[str]:
    # 더블 뉴라인으로 분할
    # 문장 수 기반 병합/분할
    # 의미 단위 고려 없음
```

---

## 2. Phase 1: 페이지 → 챕터 기반 전환

### 문제점 인식

1. **페이지 경계 문제**: "Language"가 "anguage"로 잘림
2. **컨텍스트 부재**: 문단이 어느 챕터에 속하는지 모름
3. **의미 단위 무시**: 규칙 기반 분할이 개념 경계를 무시

### 의사결정

| 결정 | 이유 | 대안 |
|------|------|------|
| TOC 기반 챕터 감지 | PDF 내장 TOC가 가장 신뢰성 높음 | 패턴 기반만 사용 (부정확) |
| 전체 텍스트 추출 후 챕터 분할 | 페이지 경계 문제 해결 | 페이지별 처리 유지 (문제 지속) |
| 텍스트 정규화 모듈 분리 | 하이픈 연결, 테이블 제거 등 복잡한 처리 | chunker에 포함 (복잡도 증가) |

### 신규 파일

```
src/pdf/
├── chapter_detector.py  # TOC/패턴 기반 챕터 감지
├── text_normalizer.py   # PDF 아티팩트 제거, 페이지 연결
```

### 스키마 확장

```python
# schemas.py (확장)
class Chapter(BaseModel):
    book_id: int
    title: str
    start_page: int
    end_page: int
    level: int              # 1=Chapter, 2=Section
    detection_method: str   # 'toc', 'pattern', 'fallback'

class ParagraphChunk(BaseModel):
    # 기존 필드 유지
    chapter_id: int | None           # NEW: 챕터 참조
    chapter_paragraph_index: int     # NEW: 챕터 내 인덱스
    section_path: str | None         # NEW: "Chapter 1 > Section"

@dataclass
class HierarchicalChunk:
    """chunker 출력용 계층적 청크"""
    text: str
    chapter_id: int | None
    chapter_title: str | None
    section_path: str
    paragraph_index: int
    chapter_paragraph_index: int
    start_char: int
    end_char: int
```

---

## 3. Phase 2: 규칙 기반 → LLM 기반 청킹

### 문제점 인식 (테스트 결과)

```
Chapter 1 → 181 paragraphs → 181 LLM calls
중복 개념: "Foundation Models" x3, "Model as a Service" x2
```

1. **과도한 분할**: 의미적으로 연결된 텍스트가 여러 문단으로 분리
2. **중복 추출**: 동일 개념이 여러 문단에서 반복 추출
3. **비효율적 API 사용**: 문단당 1회 LLM 호출

### 의사결정

| 결정 | 이유 | 대안 |
|------|------|------|
| 하이브리드 청킹 | 규칙 기반 대략 분할 + LLM 세부 분할 | LLM만 사용 (비용 높음) |
| 청킹 + 추출 통합 | 1 API 호출로 분할과 추출 동시 수행 | 2단계 분리 (비효율) |
| 2500자 big_chunk | LLM 컨텍스트 활용 최적화 | 더 작은 청크 (의미 손실) |

### 신규 파일

```
src/pdf/semantic_chunker.py      # 하이브리드 청킹 로직
src/prompts/semantic_chunking.py # 통합 프롬프트
```

### 신규 스키마

```python
# schemas.py (추가)
class SemanticParagraph(BaseModel):
    """LLM 출력"""
    text: str      # 원문 그대로
    concept: str   # 핵심 개념

class ChunkAndExtractResult(BaseModel):
    """LLM 구조화 출력"""
    paragraphs: List[SemanticParagraph]
```

### 결과 비교

| 지표 | Before (규칙) | After (하이브리드) | 개선 |
|------|--------------|-------------------|------|
| 문단 수 | 181 | 98 | -46% |
| LLM 호출 | 181 | ~40 | -78% |
| 고유 개념 비율 | ~60% | 93% (91/98) | +33% |
| 평균 문단 길이 | ~300자 | ~1,000자 | +233% |

---

## 4. Phase 3: 섹션 메타데이터 추가

### 문제점 인식

```
현재: section_path = "Chapter 1. Introduction to..."
원하는: section_path = "Chapter 1... > What This Book Is Not"
```

챕터 내 서브섹션 ("The Rise of AI Engineering", "Language Models" 등)이 메타데이터에 누락

### 의사결정

| 결정 | 이유 | 대안 |
|------|------|------|
| LLM 기반 섹션 감지 | 다양한 섹션 스타일 인식 가능 | 규칙 기반 (패턴 제한적) |
| 섹션 상태 추적 | 연속 문단에 섹션 전파 | 매 문단마다 섹션 지정 (중복) |
| 스키마 확장 (section_title) | 기존 구조 유지하며 기능 추가 | 별도 스키마 (복잡도 증가) |

### 스키마 수정

```python
class SemanticParagraph(BaseModel):
    text: str
    concept: str
    section_title: str | None = Field(
        default=None,
        description="섹션 제목 (예: 'What This Book Is Not')"
    )
```

### 청커 로직 추가

```python
current_section = None  # 섹션 상태 추적

for para in semantic_paragraphs:
    # 새 섹션 감지 시 갱신
    if para.section_title and para.section_title.lower() != "null":
        current_section = para.section_title

    # section_path 구성
    if current_section:
        section_path = f"{chapter_title} > {current_section}"
```

### 최종 결과

```
section_path: "Chapter 1... > The Rise of AI Engineering"
section_path: "Chapter 1... > From Language Models to Large Language Models"
section_path: "Chapter 1... > Language models"
```

---

## 5. 전체 아키텍처 변화

### Before (초기)

```
PDF → 페이지별 추출 → 규칙 분할 → LLM 추출 → DB
      (page_text)     (150-1000자)  (181 calls)
```

### After (현재)

```
PDF → 전체 추출 → 챕터 감지 → 텍스트 정규화 → 하이브리드 청킹 → DB
      (full_text)   (TOC 기반)   (하이픈 연결)   (규칙+LLM, ~40 calls)
                                  (테이블 제거)   (분할+추출 통합)
                                                 (섹션 감지)
```

### 데이터 구조 예시

```
Book: "AI Engineering"
├── Chapter 1: "Introduction to LLMs"
│   ├── Paragraph 0: "Large language models have..."
│   │   └── section_path: "Chapter 1 > Introduction to LLMs"
│   │   └── KeyIdea: "Large Language Model"
│   ├── Paragraph 1: "The transformer architecture..."
│   │   └── section_path: "Chapter 1 > The Rise of AI Engineering"
│   │   └── KeyIdea: "Transformer"
│   └── ...
├── Chapter 2: "Prompt Engineering"
│   └── ...
└── ...
```

---

## 6. 파일 변경 요약

| 파일 | 상태 | 주요 변경 |
|------|------|----------|
| `parser.py` | 수정 | `extract_all_pages()`, `extract_full_text()` 추가 |
| `chunker.py` | 수정 | `split_chapter_into_paragraphs()`, `HierarchicalChunk` |
| `schemas.py` | 수정 | `Chapter`, `DetectedChapter`, `SemanticParagraph` 추가 |
| `chapter_detector.py` | **신규** | TOC/패턴 기반 챕터 감지 |
| `text_normalizer.py` | **신규** | PDF 아티팩트 제거, 테이블 필터링 |
| `semantic_chunker.py` | **신규** | 하이브리드 청킹, 섹션 상태 추적 |
| `semantic_chunking.py` | **신규** | LLM 통합 프롬프트 |
| `test_full_pipeline.py` | **신규** | 테스트 스크립트 |

---

## 7. 핵심 의사결정 요약

| # | 결정 | 근거 |
|---|------|------|
| 1 | 페이지 → 챕터 기반 | 페이지 경계 문제 해결, 컨텍스트 유지 |
| 2 | TOC 우선 감지 | PDF 내장 메타데이터가 가장 신뢰성 높음 |
| 3 | 하이브리드 청킹 | 규칙(효율) + LLM(정확도) 장점 결합 |
| 4 | 청킹+추출 통합 | API 호출 78% 감소, 의미 일관성 |
| 5 | LLM 섹션 감지 | 다양한 섹션 스타일 인식 가능 |
| 6 | 섹션 상태 추적 | 연속 문단에 섹션 정보 전파 |

---

## 버그 수정 이력

### P0: 챕터 end_page 계산 오류
- **문제**: TOC에서 다음 항목 레벨 무시 → 모든 챕터가 단일 페이지로 감지
- **수정**: 같은 레벨 이하의 다음 항목을 찾아 end_page 계산

### P1: 페이지 경계 텍스트 잘림
- **문제**: "Language"가 "anguage"로 잘림
- **수정**: `extract_chapter_text_from_pdf()` 함수로 PDF에서 직접 페이지 범위 추출

### P2: 테이블/표 데이터 필터링
- **문제**: 벤치마크 표 데이터가 문단에 포함됨
- **수정**: `_remove_table_data()` 메서드로 3줄 이상 연속 테이블 행 제거

### P3: "null" 문자열 처리
- **문제**: LLM이 JSON null 대신 `"null"` 문자열 반환
- **수정**: `para.section_title.lower() != "null"` 조건 추가
