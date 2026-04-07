-- ============================================================
-- Stage 4 Extra — FRAMEWORKS 50개 agent_json_raw UPDATE
-- Prerequisites: stage-1-frameworks-extra.sql applied
--                + ingest-bulk + pregen-ai-state API 실행 후
-- seq 201 ~ 250
-- ============================================================

BEGIN;

DO $$
DECLARE
    v_user_id   UUID := '00000000-0000-0000-0000-000000000000'::UUID;
    v_art_id    UUID;
    v_uas_id    UUID;
    v_aai_id    UUID;
    v_pub_at    TIMESTAMPTZ;
    rec         RECORD;
    i           INT := 0;
BEGIN

FOR rec IN (
    SELECT * FROM (VALUES
    -- (seq, entity_id, cat_id, cat_name, entity_name, score, summary, why_matters)
    -- Agent — LangChain
    (201, '0195f300-1001-7000-b000-000000000010', '0195f300-2001-7000-a000-000000000010', 'Agent', 'LangChain', 4, 'LangChain v0.3 simplifies the chain API with new declarative LCEL syntax, reducing boilerplate by 40%.', 'Major ergonomics improvement for production LLM application developers.'),
    (202, '0195f300-1001-7000-b000-000000000010', '0195f300-2001-7000-a000-000000000010', 'Agent', 'LangChain', 3, 'LangChain now supports native tool calling without manual JSON schema definitions.', 'Reduces friction for building tool-augmented agents.'),
    (203, '0195f300-1001-7000-b000-000000000010', '0195f300-2001-7000-a000-000000000010', 'Agent', 'LangChain', 3, 'LCEL performance improvements reduce chain execution latency by up to 25%.', 'Critical for latency-sensitive production deployments.'),
    -- Agent — LangGraph
    (204, '0195f300-1001-7000-b000-000000000011', '0195f300-2001-7000-a000-000000000010', 'Agent', 'LangGraph', 5, 'LangGraph 0.3 introduces persistent state and human-in-the-loop checkpointing for long-running agents.', 'Game-changer for production agent reliability and auditability.'),
    (205, '0195f300-1001-7000-b000-000000000011', '0195f300-2001-7000-a000-000000000010', 'Agent', 'LangGraph', 4, 'LangGraph human-in-the-loop patterns enable agents to pause and await user approval at critical steps.', 'Essential for enterprise deployments requiring human oversight.'),
    (206, '0195f300-1001-7000-b000-000000000011', '0195f300-2001-7000-a000-000000000010', 'Agent', 'LangGraph', 4, 'LangGraph multi-agent supervisor pattern enables hierarchical agent coordination at scale.', 'Foundational architecture for complex multi-step automated workflows.'),
    -- Agent — CrewAI
    (207, '0195f300-1001-7000-b000-000000000012', '0195f300-2001-7000-a000-000000000010', 'Agent', 'CrewAI', 4, 'CrewAI 0.86 introduces task dependency graphs and async agent execution, doubling throughput.', 'Major performance leap for parallel multi-agent pipelines.'),
    (208, '0195f300-1001-7000-b000-000000000012', '0195f300-2001-7000-a000-000000000010', 'Agent', 'CrewAI', 3, 'CrewAI enterprise adds long-term memory and shared knowledge base across agent crews.', 'Enables persistent organizational knowledge for recurring tasks.'),
    -- Agent — AutoGPT
    (209, '0195f300-1001-7000-b000-000000000013', '0195f300-2001-7000-a000-000000000010', 'Agent', 'AutoGPT', 5, 'AutoGPT Platform v0.4 launches no-code visual workflow builder for autonomous agent design.', 'Lowers barrier to entry for non-engineers building autonomous agents.'),
    (210, '0195f300-1001-7000-b000-000000000013', '0195f300-2001-7000-a000-000000000010', 'Agent', 'AutoGPT', 3, 'AutoGPT crosses 168k GitHub stars, remaining the most-starred AI agent repository.', 'Reflects continued community momentum in autonomous agent development.'),
    (211, '0195f300-1001-7000-b000-000000000013', '0195f300-2001-7000-a000-000000000010', 'Agent', 'AutoGPT', 3, 'AutoGPT Forge SDK provides a standardized interface for building custom agent backends.', 'Enables rapid prototyping of specialized autonomous agent systems.'),
    -- Fine-Tuning — Unsloth
    (212, '0195f300-1001-7000-b000-000000000015', '0195f300-2001-7000-a000-000000000011', 'Fine-Tuning', 'Unsloth', 4, 'Unsloth v2026.3 adds Llama 4 Scout support with optimized 4-bit quantized training.', 'Enables consumer GPU fine-tuning of the latest Llama 4 family models.'),
    (213, '0195f300-1001-7000-b000-000000000015', '0195f300-2001-7000-a000-000000000011', 'Fine-Tuning', 'Unsloth', 5, 'Unsloth achieves 2x faster fine-tuning and 60% VRAM reduction vs standard LoRA.', 'Best-in-class efficiency makes fine-tuning accessible on limited hardware.'),
    (214, '0195f300-1001-7000-b000-000000000015', '0195f300-2001-7000-a000-000000000011', 'Fine-Tuning', 'Unsloth', 3, 'Unsloth GGUFification enables direct export to GGUF format for Ollama deployment.', 'Closes the fine-tune-to-deploy loop without manual conversion steps.'),
    (215, '0195f300-1001-7000-b000-000000000015', '0195f300-2001-7000-a000-000000000011', 'Fine-Tuning', 'Unsloth', 4, 'Unsloth outperforms standard LoRA by 1.8x on speed with equivalent model quality benchmarks.', 'Validates Unsloth as the go-to library for efficient parameter-efficient fine-tuning.'),
    -- Fine-Tuning — LLaMA-Factory
    (216, '0195f300-1001-7000-b000-000000000016', '0195f300-2001-7000-a000-000000000011', 'Fine-Tuning', 'LLaMA-Factory', 4, 'LLaMA-Factory v0.9 unifies SFT, DPO, KTO, and RLHF in a single training pipeline.', 'One-stop solution simplifies the choice and comparison of alignment methods.'),
    (217, '0195f300-1001-7000-b000-000000000016', '0195f300-2001-7000-a000-000000000011', 'Fine-Tuning', 'LLaMA-Factory', 3, 'LLaMA-Factory web UI adds multi-GPU distributed training orchestration.', 'Makes large-scale fine-tuning accessible without custom training scripts.'),
    (218, '0195f300-1001-7000-b000-000000000016', '0195f300-2001-7000-a000-000000000011', 'Fine-Tuning', 'LLaMA-Factory', 4, 'LLaMA-Factory adds first-class support for Qwen3 and Gemma 3 model families.', 'Keeps LLaMA-Factory compatible with the latest open-source model releases.'),
    (219, '0195f300-1001-7000-b000-000000000016', '0195f300-2001-7000-a000-000000000011', 'Fine-Tuning', 'LLaMA-Factory', 3, 'LLaMA-Factory integrates ORPO training, enabling alignment without a reference model.', 'ORPO reduces training compute cost while maintaining alignment effectiveness.'),
    -- RAG — RAGFlow
    (220, '0195f300-1001-7000-b000-00000000001c', '0195f300-2001-7000-a000-000000000012', 'RAG', 'RAGFlow', 5, 'RAGFlow v0.14 introduces GraphRAG for entity-relationship aware retrieval alongside hybrid search.', 'GraphRAG dramatically improves multi-hop reasoning over structured knowledge.'),
    (221, '0195f300-1001-7000-b000-00000000001c', '0195f300-2001-7000-a000-000000000012', 'RAG', 'RAGFlow', 3, 'RAGFlow DeepDoc chunking outperforms naive text splitting on complex PDF documents.', 'Document-structure-aware chunking reduces retrieval noise in enterprise RAG.'),
    (222, '0195f300-1001-7000-b000-00000000001c', '0195f300-2001-7000-a000-000000000012', 'RAG', 'RAGFlow', 3, 'RAGFlow enterprise multi-tenant mode enables isolated knowledge bases per organization.', 'Critical feature for SaaS companies building white-label RAG products.'),
    -- RAG — Haystack
    (223, '0195f300-1001-7000-b000-00000000001d', '0195f300-2001-7000-a000-000000000012', 'RAG', 'Haystack', 4, 'Haystack 2.0 introduces YAML-based declarative pipeline configuration for reproducible NLP workflows.', 'Version-controlled pipelines improve team collaboration and deployment consistency.'),
    (224, '0195f300-1001-7000-b000-00000000001d', '0195f300-2001-7000-a000-000000000012', 'RAG', 'Haystack', 3, 'Haystack adds native Cohere Rerank and Mistral Embed integrations.', 'Expands retrieval quality options without custom integration code.'),
    -- RAG — RAGAS
    (225, '0195f300-1001-7000-b000-00000000001f', '0195f300-2001-7000-a000-000000000012', 'RAG', 'RAGAS', 4, 'RAGAS v0.2 introduces automated test set generation directly from source documents.', 'Eliminates manual labeling effort for RAG evaluation dataset creation.'),
    (226, '0195f300-1001-7000-b000-00000000001f', '0195f300-2001-7000-a000-000000000012', 'RAG', 'RAGAS', 3, 'RAGAS context precision and recall metrics provide fine-grained retrieval quality assessment.', 'Enables systematic diagnosis of retrieval vs generation failure modes.'),
    (227, '0195f300-1001-7000-b000-00000000001f', '0195f300-2001-7000-a000-000000000012', 'RAG', 'RAGAS', 3, 'RAGAS integrates natively with both LangChain and LlamaIndex evaluation pipelines.', 'Reduces integration friction for teams already using major RAG frameworks.'),
    -- Serving — vLLM
    (228, '0195f300-1001-7000-b000-000000000017', '0195f300-2001-7000-a000-000000000014', 'Serving', 'vLLM', 5, 'vLLM v0.8 speculative decoding and chunked prefill improve throughput by up to 2.4x.', 'Significant serving efficiency gain reduces GPU cost for high-traffic LLM APIs.'),
    (229, '0195f300-1001-7000-b000-000000000017', '0195f300-2001-7000-a000-000000000014', 'Serving', 'vLLM', 3, 'vLLM Kubernetes deployment guide covers autoscaling and rolling updates for production.', 'Fills the operational gap between model serving and cloud-native infrastructure.'),
    (230, '0195f300-1001-7000-b000-000000000017', '0195f300-2001-7000-a000-000000000014', 'Serving', 'vLLM', 4, 'vLLM OpenAI-compatible server adds multi-modal input support for vision models.', 'Enables drop-in replacement for GPT-4V deployments with open-source models.'),
    (231, '0195f300-1001-7000-b000-000000000017', '0195f300-2001-7000-a000-000000000014', 'Serving', 'vLLM', 4, 'vLLM outperforms TensorRT-LLM on throughput benchmarks for most open-source models in 2026.', 'Positions vLLM as the default choice for production open-source model serving.'),
    -- Serving — Ollama
    (232, '0195f300-1001-7000-b000-000000000018', '0195f300-2001-7000-a000-000000000014', 'Serving', 'Ollama', 4, 'Ollama v0.6 introduces model context caching, reducing repeated prompt processing overhead.', 'Dramatically speeds up multi-turn conversations for long system prompts.'),
    (233, '0195f300-1001-7000-b000-000000000018', '0195f300-2001-7000-a000-000000000014', 'Serving', 'Ollama', 3, 'Ollama multimodal streaming stability improvements fix image input handling edge cases.', 'Resolves reliability issues blocking production multimodal use cases.'),
    (234, '0195f300-1001-7000-b000-000000000018', '0195f300-2001-7000-a000-000000000014', 'Serving', 'Ollama', 3, 'Ollama REST API adds batch completion endpoint for high-throughput offline processing.', 'Enables efficient document processing and bulk inference without streaming overhead.'),
    (235, '0195f300-1001-7000-b000-000000000018', '0195f300-2001-7000-a000-000000000014', 'Serving', 'Ollama', 2, 'Ollama Docker Compose setup enables isolated local LLM lab environments in minutes.', 'Simplifies onboarding for developers new to local LLM experimentation.'),
    -- Data & Storage — LlamaIndex
    (236, '0195f300-1001-7000-b000-000000000019', '0195f300-2001-7000-a000-000000000015', 'Data & Storage', 'LlamaIndex', 4, 'LlamaIndex v0.12 hybrid search combines dense and sparse retrieval for improved recall.', 'Addresses the classic precision-recall tradeoff in production RAG systems.'),
    (237, '0195f300-1001-7000-b000-000000000019', '0195f300-2001-7000-a000-000000000015', 'Data & Storage', 'LlamaIndex', 4, 'LlamaIndex PropertyGraphIndex enables knowledge graph construction and traversal for RAG.', 'GraphRAG capability now available natively in the LlamaIndex ecosystem.'),
    (238, '0195f300-1001-7000-b000-000000000019', '0195f300-2001-7000-a000-000000000015', 'Data & Storage', 'LlamaIndex', 3, 'LlamaIndex Workflow API introduces event-driven orchestration for complex agent pipelines.', 'Replaces imperative agent loops with reactive, composable workflow graphs.'),
    -- Data & Storage — ChromaDB
    (239, '0195f300-1001-7000-b000-00000000001a', '0195f300-2001-7000-a000-000000000015', 'Data & Storage', 'ChromaDB', 3, 'ChromaDB 0.6 persistent client improves stability and adds multi-collection support.', 'Resolves data persistence issues that limited ChromaDB in long-running services.'),
    (240, '0195f300-1001-7000-b000-00000000001a', '0195f300-2001-7000-a000-000000000015', 'Data & Storage', 'ChromaDB', 3, 'ChromaDB advanced metadata filtering enables complex boolean queries over vector stores.', 'Brings SQL-like filtering expressiveness to vector database queries.'),
    (241, '0195f300-1001-7000-b000-00000000001a', '0195f300-2001-7000-a000-000000000015', 'Data & Storage', 'ChromaDB', 4, 'ChromaDB leads on ease-of-use in 2026 vector database benchmark vs Pinecone and Weaviate.', 'Strong positioning for developer-first RAG prototyping use cases.'),
    -- LLMOps — MLflow
    (242, '0195f300-1001-7000-b000-00000000001e', '0195f300-2001-7000-a000-000000000016', 'LLMOps', 'MLflow', 5, 'MLflow 3.0 AI Gateway unifies model routing, rate limiting, and prompt versioning in one service.', 'Enterprise-grade LLM governance layer now available in open source.'),
    (243, '0195f300-1001-7000-b000-00000000001e', '0195f300-2001-7000-a000-000000000016', 'LLMOps', 'MLflow', 4, 'MLflow LLM Evaluate automates side-by-side model comparison with custom metric plugins.', 'Accelerates model selection and regression detection in CI/CD pipelines.'),
    (244, '0195f300-1001-7000-b000-00000000001e', '0195f300-2001-7000-a000-000000000016', 'LLMOps', 'MLflow', 3, 'MLflow Tracing API provides OpenTelemetry-compatible instrumentation for LLM call chains.', 'Enables distributed tracing across complex multi-model inference pipelines.'),
    (245, '0195f300-1001-7000-b000-00000000001e', '0195f300-2001-7000-a000-000000000016', 'LLMOps', 'MLflow', 3, 'MLflow matches W&B on feature parity while offering self-hosted deployment flexibility.', 'Compelling alternative for teams with data residency or cost requirements.'),
    -- Observability — Langfuse
    (246, '0195f300-1001-7000-b000-00000000001b', '0195f300-2001-7000-a000-000000000017', 'Observability', 'Langfuse', 4, 'Langfuse v3 introduces real-time LLM observability with sub-second trace ingestion.', 'Production-grade observability now matches speed of modern APM tools.'),
    (247, '0195f300-1001-7000-b000-00000000001b', '0195f300-2001-7000-a000-000000000017', 'Observability', 'Langfuse', 4, 'Langfuse token cost tracking with budget alerts prevents runaway inference spending.', 'Essential cost governance feature for teams running high-volume LLM applications.'),
    (248, '0195f300-1001-7000-b000-00000000001b', '0195f300-2001-7000-a000-000000000017', 'Observability', 'Langfuse', 3, 'Langfuse Scores API enables custom evaluation metrics attached to any trace.', 'Closes the loop between production monitoring and offline evaluation workflows.'),
    -- Prompt Engineering — DSPy
    (249, '0195f300-1001-7000-b000-000000000014', '0195f300-2001-7000-a000-000000000013', 'Prompt Engineering', 'DSPy', 5, 'DSPy 2.5 MIPROv2 optimizer automatically tunes prompts and few-shot examples for maximum accuracy.', 'Automated prompt optimization outperforms hand-crafted prompts on most benchmarks.'),
    (250, '0195f300-1001-7000-b000-000000000014', '0195f300-2001-7000-a000-000000000013', 'Prompt Engineering', 'DSPy', 4, 'DSPy programmatic prompting consistently outperforms manual prompting on GPT-5 across 12 tasks.', 'Validates DSPy as the new standard for optimized prompt engineering workflows.')
    ) AS t(seq, entity_id, cat_id, cat_name, entity_name, score, summary, why_matters)
) LOOP
    i := i + 1;

    -- article_raw id from seq
    v_art_id := format('0195f300-b%s-7000-8000-000000000001', lpad(rec.seq::text, 3, '0'))::UUID;

    -- published_at from article_raw
    SELECT published_at INTO v_pub_at
    FROM content.article_raw
    WHERE id = v_art_id;

    IF v_pub_at IS NULL THEN
        RAISE NOTICE 'Skipping seq %: article_raw not found', rec.seq;
        CONTINUE;
    END IF;

    -- user_article_state id
    SELECT id INTO v_uas_id
    FROM content.user_article_state
    WHERE article_raw_id = v_art_id
      AND user_id = v_user_id
      AND revoked_at IS NULL
    LIMIT 1;

    IF v_uas_id IS NULL THEN
        RAISE NOTICE 'Skipping seq %: user_article_state not found (run ingest-bulk first)', rec.seq;
        CONTINUE;
    END IF;

    -- user_article_ai_state id
    SELECT id INTO v_aai_id
    FROM content.user_article_ai_state
    WHERE user_article_state_id = v_uas_id
    LIMIT 1;

    IF v_aai_id IS NULL THEN
        RAISE NOTICE 'Skipping seq %: user_article_ai_state not found (run pregen-ai-state first)', rec.seq;
        CONTINUE;
    END IF;

    -- Update agent_json_raw and set SUCCESS
    UPDATE content.user_article_ai_state
    SET
        agent_json_raw = jsonb_build_object(
            'representative_entity_id',            rec.entity_id,
            'representative_entity_name',          rec.entity_name,
            'representative_entity_page',          'FRAMEWORKS',
            'representative_entity_category_id',   rec.cat_id,
            'representative_entity_category_name', rec.cat_name,
            'ai_score',                            rec.score,
            'ai_summary',                          rec.summary,
            'ai_why_it_matters',                   rec.why_matters
        ),
        ai_status  = 'SUCCESS',
        updated_at = NOW()
    WHERE id = v_aai_id;

END LOOP;

RAISE NOTICE 'Done: processed % records', i;
END $$;

COMMIT;
