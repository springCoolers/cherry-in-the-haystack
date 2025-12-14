"""
LangGraph 워크플로우 상태 정의.

PipelineState: 전체 PDF 처리 파이프라인용 (TypedDict)
State: 개별 아이디어 추출용 (Pydantic)
"""
from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

from src.model.schemas import (
    ParagraphChunk,
    ExtractedIdea,
    HierarchicalChunk,
    DetectedChapter,
    DetectedSection,
)


# ============================================================
# PipelineState: 전체 PDF 처리 파이프라인용 (TypedDict)
# ============================================================

class PipelineState(TypedDict, total=False):
    """
    PDF 처리 파이프라인 전체 상태.

    LangGraph에서 TypedDict 사용 권장.
    total=False로 모든 필드를 optional로 설정.
    """
    # ─── 입력 ───
    pdf_path: str
    book_id: Optional[int]
    resume: bool

    # ─── PDF 메타데이터 ───
    metadata: Optional[dict]  # title, author, total_pages

    # ─── Plain Text (Option A 파이프라인) ───
    plain_text: Optional[str]  # pymupdf로 추출한 순수 텍스트

    # ─── 챕터/섹션 (LLM 감지 기반) ───
    chapters: List[DetectedChapter]  # LLM이 감지한 챕터 리스트
    current_chapter: Optional[DetectedChapter]  # 현재 처리 중인 챕터
    current_chapter_id: Optional[int]  # 현재 챕터 DB ID
    current_section: Optional[DetectedSection]  # 현재 처리 중인 섹션
    current_section_text: Optional[str]  # 현재 섹션 텍스트
    hierarchy_path: Optional[str]  # 현재 계층 경로 (예: "Chapter 1 > Section 1.1")

    # ─── 문단 처리 ───
    chunks: List[HierarchicalChunk]  # 분할된 문단 리스트
    current_chunk_index: int  # 현재 처리 중인 청크 인덱스
    current_chunk: Optional[HierarchicalChunk]  # 현재 처리 중인 청크
    extracted_concepts: Optional[dict]  # 추출된 개념 캐시 {paragraph_index: concept}

    # ─── 아이디어 추출 ───
    extracted_idea: Optional[ExtractedIdea]
    is_duplicate: bool  # 중복 여부
    saved_chunk_id: Optional[int]  # 저장된 청크 ID

    # ─── 결과/통계 ───
    stats: dict  # 처리 통계
    error: Optional[str]  # 에러 메시지

    # ─── 설정 ───
    model_version: str


def create_initial_state(
    pdf_path: str,
    book_id: Optional[int] = None,
    resume: bool = False,
    model_version: str = "gemini-2.5-flash",
) -> PipelineState:
    """초기 PipelineState 생성."""
    return PipelineState(
        pdf_path=pdf_path,
        book_id=book_id,
        resume=resume,
        model_version=model_version,
        # 기본값 설정
        chapters=[],
        chunks=[],
        current_chunk_index=0,
        is_duplicate=False,
        stats={
            "total_chapters": 0,
            "completed_chapters": 0,
            "failed_chapters": 0,
            "total_paragraphs": 0,
            "total_ideas": 0,
            "duplicates_skipped": 0,
        },
    )


# ============================================================
# State: 개별 아이디어 추출용 (Pydantic)
# ============================================================

class State(BaseModel):
    """개별 청크의 아이디어 추출 상태."""
    chunk: ParagraphChunk = Field(description="입력 문단 청크")
    result: ExtractedIdea | None = Field(default=None, description="추출된 핵심 아이디어")
    error: str | None = Field(default=None, description="에러 메시지")

    # 메타데이터 (DB 저장용)
    book_id: int | None = Field(default=None, description="책 ID")
    chunk_id: int | None = Field(default=None, description="저장된 청크 ID")
    model_version: str = Field(default="gemini-2.5-flash", description="LLM 모델 버전")
