"""
아이디어 추출 노드.

LLM을 사용하여 문단에서 핵심 아이디어를 추출.
"""

from langchain_core.prompts import ChatPromptTemplate

from src.workflow.state import PipelineState
from src.model.model import get_default_llm
from src.model.schemas import ExtractedIdea, ParagraphChunk
from src.prompts.extraction import EXTRACTION_PROMPT, HUMAN_PROMPT


def extract_idea(state: PipelineState) -> PipelineState:
    """
    현재 청크에서 핵심 아이디어 추출.

    LLM을 사용하여 구조화된 아이디어를 추출.

    Args:
        state: PipelineState (current_chunk 필수)

    Returns:
        업데이트된 PipelineState (extracted_idea 추가)
    """
    current_chunk = state.get("current_chunk")

    if not current_chunk:
        return {**state, "error": "current_chunk is required for idea extraction"}

    # 청크 텍스트 추출
    if hasattr(current_chunk, "text"):
        chunk_text = current_chunk.text
    elif hasattr(current_chunk, "body_text"):
        chunk_text = current_chunk.body_text
    elif isinstance(current_chunk, dict):
        chunk_text = current_chunk.get("text") or current_chunk.get("body_text", "")
    else:
        chunk_text = str(current_chunk)

    if not chunk_text or len(chunk_text.strip()) < 50:
        return {**state, "extracted_idea": None}

    try:
        llm = get_default_llm()
        structured_llm = llm.with_structured_output(ExtractedIdea, method="json_mode")

        prompt = ChatPromptTemplate.from_messages([
            ("system", EXTRACTION_PROMPT),
            ("human", HUMAN_PROMPT),
        ])

        chain = prompt | structured_llm
        extracted = chain.invoke({"text": chunk_text})

        # 통계 업데이트
        stats = state.get("stats", {})
        stats["total_ideas"] = stats.get("total_ideas", 0) + 1

        return {
            **state,
            "extracted_idea": extracted,
            "stats": stats,
        }

    except Exception as e:
        return {**state, "error": f"Idea extraction failed: {str(e)}"}
