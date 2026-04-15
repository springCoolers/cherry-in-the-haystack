-- ============================================================
-- Stage 4 Extra NEW v2 — 200 agent_json_raw UPDATE (PENDING→processed)
-- seq 501 ~ 700 / article_raw ID: 0195f300-d{seq:03d}-7000-8000-000000000001
-- user_id: SYSTEM_USER_ID = 00000000-0000-0000-0000-000000000000
-- agent_json_raw: v0.3 format (representative_entity nested, side_category_code)
-- ai_status: PENDING 유지 (parse-agent-json API 호출 후 SUCCESS 전환)
--
-- side_category_code rules:
--   CASE_STUDIES (seq 631-660):
--     - APPLIED_RESEARCH (15건): seq 632, 634, 636, 638, 640, 642, 644, 646, 648, 650,
--                                    652, 654, 656, 658, 660  (research/lab papers)
--     - CASE_STUDY      (15건): the other 15 (deployment/customer stories)
--   다른 page = NULL
--
-- Prerequisites:
--   stage-1-extra-new-200-v2.sql 적용
--   + ingest-bulk API (user_article_state 생성)
--   + pregen-ai-state API (PENDING ai_state 생성)
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
    skipped     INT := 0;
BEGIN

FOR rec IN (
    SELECT * FROM (VALUES
    -- (seq, entity_id, page, score, summary)

    -- =================== FRAMEWORKS: Agent ===================
    -- LangChain (501-507) — entity 010
    (501, '0195f300-1001-7000-b000-000000000010', 'FRAMEWORKS', 4, 'LangChain v0.5 ships native tracing hooks that emit OpenTelemetry-compatible spans for every chain step in production.'),
    (502, '0195f300-1001-7000-b000-000000000010', 'FRAMEWORKS', 3, 'LangChain streaming tokens API now supports SSE out of the box, eliminating boilerplate for browser-side LLM apps.'),
    (503, '0195f300-1001-7000-b000-000000000010', 'FRAMEWORKS', 3, 'LangChain output parsers in v0.5.1 add JSON schema validation, raising structured response reliability for agents.'),
    (504, '0195f300-1001-7000-b000-000000000010', 'FRAMEWORKS', 4, 'LangChain multi-provider fallback strategy routes requests across vendors to optimize cost and availability.'),
    (505, '0195f300-1001-7000-b000-000000000010', 'FRAMEWORKS', 4, 'LangChain embeddings cache cuts RAG API costs by 55% in production by deduplicating identical chunk requests.'),
    (506, '0195f300-1001-7000-b000-000000000010', 'FRAMEWORKS', 3, 'LangChain Hub passes 50K reusable prompt templates as community contributions accelerate template reuse.'),
    (507, '0195f300-1001-7000-b000-000000000010', 'FRAMEWORKS', 3, 'LangChain JS reaches v0.4 feature parity with the Python SDK, unblocking TypeScript-only LLM stacks.'),
    -- LangGraph (508-513) — entity 011
    (508, '0195f300-1001-7000-b000-000000000011', 'FRAMEWORKS', 5, 'LangGraph 0.5 introduces durable execution backed by Postgres checkpoints for crash-resistant agent state.'),
    (509, '0195f300-1001-7000-b000-000000000011', 'FRAMEWORKS', 3, 'LangGraph conditional edges now accept async predicates, enabling I/O-bound dynamic routing without blocking.'),
    (510, '0195f300-1001-7000-b000-000000000011', 'FRAMEWORKS', 4, 'LangGraph Studio adds trace replay for step-by-step debugging of agent state transitions and tool calls.'),
    (511, '0195f300-1001-7000-b000-000000000011', 'FRAMEWORKS', 4, 'LangGraph multi-agent supervisor pattern reaches GA with built-in templates for hand-off and routing logic.'),
    (512, '0195f300-1001-7000-b000-000000000011', 'FRAMEWORKS', 3, 'LangGraph Cloud adds per-edge latency metrics to identify bottlenecks in complex agent graph topologies.'),
    (513, '0195f300-1001-7000-b000-000000000011', 'FRAMEWORKS', 3, 'LangGraph streaming updates cut UI lag in real-time multi-agent apps by emitting partial state per node.'),
    -- CrewAI (514-519) — entity 012
    (514, '0195f300-1001-7000-b000-000000000012', 'FRAMEWORKS', 4, 'CrewAI 1.1 adds a hierarchical process mode that orchestrates manager-worker agent patterns out of the box.'),
    (515, '0195f300-1001-7000-b000-000000000012', 'FRAMEWORKS', 4, 'CrewAI memory module ships long-term vector storage that persists agent context across crew sessions.'),
    (516, '0195f300-1001-7000-b000-000000000012', 'FRAMEWORKS', 4, 'CrewAI tasks output validation catches agent mistakes before downstream steps consume invalid payloads.'),
    (517, '0195f300-1001-7000-b000-000000000012', 'FRAMEWORKS', 3, 'CrewAI telemetry dashboard visualizes per-agent token spend across crews to surface cost regressions early.'),
    (518, '0195f300-1001-7000-b000-000000000012', 'FRAMEWORKS', 3, 'CrewAI Slack integration lets teams trigger multi-agent crews directly from channels with thread-aware replies.'),
    (519, '0195f300-1001-7000-b000-000000000012', 'FRAMEWORKS', 3, 'CrewAI open source crosses 30K GitHub stars as enterprise adoption of multi-agent orchestration accelerates.'),
    -- AutoGPT (520-525) — entity 013
    (520, '0195f300-1001-7000-b000-000000000013', 'FRAMEWORKS', 4, 'AutoGPT Platform adds a visual workflow builder that lets non-developers compose autonomous agents without code.'),
    (521, '0195f300-1001-7000-b000-000000000013', 'FRAMEWORKS', 3, 'AutoGPT Marketplace lets developers monetize reusable agent blocks, opening a third-party ecosystem.'),
    (522, '0195f300-1001-7000-b000-000000000013', 'FRAMEWORKS', 4, 'AutoGPT adds a local LLM backend that runs autonomous agents on-premise without sending data to cloud APIs.'),
    (523, '0195f300-1001-7000-b000-000000000013', 'FRAMEWORKS', 3, 'AutoGPT scheduling engine runs recurring agent tasks via cron-like triggers for unattended automation.'),
    (524, '0195f300-1001-7000-b000-000000000013', 'FRAMEWORKS', 4, 'AutoGPT browser automation block powered by Playwright lets agents interact with arbitrary web applications.'),
    (525, '0195f300-1001-7000-b000-000000000013', 'FRAMEWORKS', 4, 'AutoGPT v0.6 reduces average task cost by 35% via smarter step pruning that skips redundant tool calls.'),

    -- =================== FRAMEWORKS: Fine-Tuning ===================
    -- Unsloth (526-532) — entity 015
    (526, '0195f300-1001-7000-b000-000000000015', 'FRAMEWORKS', 5, 'Unsloth adds DeepSeek V3 fine-tuning support with 70% VRAM reduction via dynamic 4-bit quantization.'),
    (527, '0195f300-1001-7000-b000-000000000015', 'FRAMEWORKS', 4, 'Unsloth vision fine-tuning now supports Llama 3.2 Vision and Pixtral, expanding multimodal training options.'),
    (528, '0195f300-1001-7000-b000-000000000015', 'FRAMEWORKS', 3, 'Unsloth continued pretraining mode enables domain adaptation on custom corpora without full retraining.'),
    (529, '0195f300-1001-7000-b000-000000000015', 'FRAMEWORKS', 4, 'Unsloth long-context fine-tuning extends Llama 3 to 128K tokens on a single A100 via memory-efficient kernels.'),
    (530, '0195f300-1001-7000-b000-000000000015', 'FRAMEWORKS', 3, 'Unsloth reasoning fine-tuning recipe leverages synthetic chain-of-thought data for math and code tasks.'),
    (531, '0195f300-1001-7000-b000-000000000015', 'FRAMEWORKS', 3, 'Unsloth GGUF export pipeline streamlines deploying fine-tuned models to local inference runtimes like Ollama.'),
    (532, '0195f300-1001-7000-b000-000000000015', 'FRAMEWORKS', 3, 'Unsloth Pro tier launches with multi-GPU training and priority support for production fine-tuning workloads.'),
    -- LLaMA-Factory (533-539) — entity 016
    (533, '0195f300-1001-7000-b000-000000000016', 'FRAMEWORKS', 4, 'LLaMA-Factory v0.10 adds native support for Qwen 3 and Mistral Large 2 with optimized recipes per architecture.'),
    (534, '0195f300-1001-7000-b000-000000000016', 'FRAMEWORKS', 4, 'LLaMA-Factory PiSSA initialization improves LoRA training stability and final quality on small adapter ranks.'),
    (535, '0195f300-1001-7000-b000-000000000016', 'FRAMEWORKS', 3, 'LLaMA-Factory CLI adds a resume-from-checkpoint flag for fault-tolerant long-running fine-tuning jobs.'),
    (536, '0195f300-1001-7000-b000-000000000016', 'FRAMEWORKS', 4, 'LLaMA-Factory KTO trainer lands as a lightweight alternative to DPO for preference alignment without a reference.'),
    (537, '0195f300-1001-7000-b000-000000000016', 'FRAMEWORKS', 3, 'LLaMA-Factory built-in hyperparameter sweep driver via Optuna automates LoRA rank and learning-rate search.'),
    (538, '0195f300-1001-7000-b000-000000000016', 'FRAMEWORKS', 4, 'LLaMA-Factory Galore optimizer cuts memory enough for full fine-tuning of 7B models on 24GB consumer GPUs.'),
    (539, '0195f300-1001-7000-b000-000000000016', 'FRAMEWORKS', 3, 'LLaMA-Factory Docker image refresh adds CUDA 12.4 and PyTorch 2.5 compatibility for newer GPU stacks.'),
    -- Axolotl (540-545) — entity 063
    (540, '0195f300-1001-7000-b000-000000000063', 'FRAMEWORKS', 4, 'Axolotl v0.8 switches to a trainer-centric config schema that produces cleaner, more composable recipes.'),
    (541, '0195f300-1001-7000-b000-000000000063', 'FRAMEWORKS', 4, 'Axolotl integrates Liger Kernel for a 20% throughput boost on H100 GPUs without code changes.'),
    (542, '0195f300-1001-7000-b000-000000000063', 'FRAMEWORKS', 4, 'Axolotl ORPO recipe lands for reference-free preference optimization that simplifies the alignment pipeline.'),
    (543, '0195f300-1001-7000-b000-000000000063', 'FRAMEWORKS', 3, 'Axolotl Cloud adds spot-GPU scheduling, lowering cost for long fine-tuning runs that can tolerate restarts.'),
    (544, '0195f300-1001-7000-b000-000000000063', 'FRAMEWORKS', 3, 'Axolotl multipack sampler reduces padding waste for variable-length sequences, raising effective throughput.'),
    (545, '0195f300-1001-7000-b000-000000000063', 'FRAMEWORKS', 3, 'Axolotl reaches 10K GitHub stars as the default open fine-tuning toolkit for community-driven research.'),

    -- =================== FRAMEWORKS: RAG ===================
    -- RAGFlow (546-552) — entity 01c
    (546, '0195f300-1001-7000-b000-00000000001c', 'FRAMEWORKS', 4, 'RAGFlow v0.16 adds hybrid search combining BM25 and dense retrieval out of the box with score fusion.'),
    (547, '0195f300-1001-7000-b000-00000000001c', 'FRAMEWORKS', 4, 'RAGFlow document pipeline ships built-in OCR, enabling RAG over scanned PDFs without external preprocessing.'),
    (548, '0195f300-1001-7000-b000-00000000001c', 'FRAMEWORKS', 3, 'RAGFlow question-rewriting step boosts retrieval recall on vague user queries by paraphrasing before search.'),
    (549, '0195f300-1001-7000-b000-00000000001c', 'FRAMEWORKS', 4, 'RAGFlow citations panel highlights source spans for every generated sentence, raising answer trustworthiness.'),
    (550, '0195f300-1001-7000-b000-00000000001c', 'FRAMEWORKS', 4, 'RAGFlow per-tenant knowledge bases with row-level access control enable secure multi-tenant SaaS deployments.'),
    (551, '0195f300-1001-7000-b000-00000000001c', 'FRAMEWORKS', 3, 'RAGFlow eval suite compares chunking strategies on user-provided benchmarks for data-driven recipe tuning.'),
    (552, '0195f300-1001-7000-b000-00000000001c', 'FRAMEWORKS', 3, 'RAGFlow native streaming answers reduce perceived latency in chat UIs by emitting tokens as soon as decoded.'),
    -- Haystack (553-559) — entity 01d
    (553, '0195f300-1001-7000-b000-00000000001d', 'FRAMEWORKS', 4, 'Haystack 2.2 adds conditional routers for branching RAG pipelines that pick paths based on query intent.'),
    (554, '0195f300-1001-7000-b000-00000000001d', 'FRAMEWORKS', 3, 'Haystack ChatGenerator now supports Anthropic Claude and Mistral backends in addition to OpenAI providers.'),
    (555, '0195f300-1001-7000-b000-00000000001d', 'FRAMEWORKS', 3, 'Haystack PromptBuilder adds Jinja2 macros for reusable prompt components across multi-stage pipelines.'),
    (556, '0195f300-1001-7000-b000-00000000001d', 'FRAMEWORKS', 3, 'Haystack Hayhooks web UI ships a drag-and-drop pipeline designer for visual RAG composition.'),
    (557, '0195f300-1001-7000-b000-00000000001d', 'FRAMEWORKS', 3, 'Haystack tracing component streams spans to any OpenTelemetry-compatible backend for unified observability.'),
    (558, '0195f300-1001-7000-b000-00000000001d', 'FRAMEWORKS', 3, 'Haystack Recipes repo lands with production-ready RAG, chat, and summarization pipelines as reference apps.'),
    (559, '0195f300-1001-7000-b000-00000000001d', 'FRAMEWORKS', 3, 'Haystack hybrid retriever composes BM25 and dense embeddings with a single wrapper, simplifying setup.'),
    -- RAGAS (560-565) — entity 01f
    (560, '0195f300-1001-7000-b000-00000000001f', 'FRAMEWORKS', 4, 'RAGAS v0.4 introduces multi-turn conversation evaluation metrics that score full chat sessions, not single turns.'),
    (561, '0195f300-1001-7000-b000-00000000001f', 'FRAMEWORKS', 3, 'RAGAS test set generation supports domain-specific persona sampling for realistic eval coverage.'),
    (562, '0195f300-1001-7000-b000-00000000001f', 'FRAMEWORKS', 3, 'RAGAS adds token-level cost reporting beside quality scores so teams can reason about quality-per-dollar.'),
    (563, '0195f300-1001-7000-b000-00000000001f', 'FRAMEWORKS', 4, 'RAGAS integrates with LangSmith for trace-to-eval cross-linking, closing the observability-to-quality loop.'),
    (564, '0195f300-1001-7000-b000-00000000001f', 'FRAMEWORKS', 3, 'RAGAS custom metric API lets teams define domain-specific quality rubrics with arbitrary judge prompts.'),
    (565, '0195f300-1001-7000-b000-00000000001f', 'FRAMEWORKS', 3, 'RAGAS App UI lets non-engineers inspect RAG failures interactively without writing Jupyter notebooks.'),

    -- =================== FRAMEWORKS: Serving ===================
    -- vLLM (566-575) — entity 017
    (566, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 5, 'vLLM v0.10 ships speculative decoding that doubles throughput on long generations without quality loss.'),
    (567, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 4, 'vLLM multi-LoRA server hot-reloads adapters between requests without engine restart, cutting deploy friction.'),
    (568, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 4, 'vLLM structured outputs enforce JSON schemas at the token sampler level for guaranteed valid responses.'),
    (569, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 4, 'vLLM AMD MI300X support reaches 90% of H100 throughput on Llama 70B, opening a real GPU alternative.'),
    (570, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 4, 'vLLM pipeline parallelism lands for serving 405B models across 16-GPU nodes with balanced utilization.'),
    (571, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 3, 'vLLM Production Stack Helm chart streamlines Kubernetes LLM deployments with sane defaults and HPA support.'),
    (572, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 3, 'vLLM tool calling server implements OpenAI-compatible function calling, easing migration from hosted APIs.'),
    (573, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 3, 'vLLM CPU offload mode lets single-GPU boxes run 70B models at low throughput for development workflows.'),
    (574, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 3, 'vLLM embedding server adds a batched embedding endpoint optimized for high-QPS retrieval workloads.'),
    (575, '0195f300-1001-7000-b000-000000000017', 'FRAMEWORKS', 4, 'vLLM continuous batching scheduler rewrite cuts P99 TTFT by 40% under high concurrency loads.'),
    -- TGI (576-580) — TGI not in tracked_entity catalog → mapped to TensorRT-LLM (065) as closest serving entity
    (576, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 4, 'Text Generation Inference v3 adds prefix caching, materially reducing latency for multi-turn chat workloads.'),
    (577, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 3, 'Text Generation Inference adds a native Inferentia2 backend for cost-optimized inference on AWS.'),
    (578, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 3, 'Text Generation Inference tool calls mode mirrors OpenAI function calling for drop-in compatibility.'),
    (579, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 3, 'Text Generation Inference streams token-level cost metrics, enabling per-request billing for SaaS providers.'),
    (580, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 3, 'Text Generation Inference adds n-gram speculative decoding for cheap latency wins without a draft model.'),
    -- SGLang (581-585) — SGLang not in tracked_entity catalog → mapped to TensorRT-LLM (065) as closest serving entity
    (581, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 4, 'SGLang v0.3 ships RadixAttention 2.0 with 30% lower KV cache memory through deduplicated prefix storage.'),
    (582, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 5, 'SGLang disaggregated prefill mode beats vLLM by 25% on burst workloads by separating prefill and decode pools.'),
    (583, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 4, 'SGLang adds native MoE routing optimizations for DeepSeek and Mixtral, improving expert-parallel throughput.'),
    (584, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 3, 'SGLang frontend DSL adds an async for loop primitive for parallel multi-sample generation in agent code.'),
    (585, '0195f300-1001-7000-b000-000000000065', 'FRAMEWORKS', 3, 'SGLang reaches 15K GitHub stars as adoption of its production inference stack accelerates.'),

    -- =================== FRAMEWORKS: Data & Storage ===================
    -- LlamaIndex (586-593) — entity 019
    (586, '0195f300-1001-7000-b000-000000000019', 'FRAMEWORKS', 4, 'LlamaIndex Workflows API replaces query engines as the default composition primitive for event-driven pipelines.'),
    (587, '0195f300-1001-7000-b000-000000000019', 'FRAMEWORKS', 4, 'LlamaIndex property graph index combines vectors with symbolic triples for hybrid retrieval over knowledge graphs.'),
    (588, '0195f300-1001-7000-b000-000000000019', 'FRAMEWORKS', 4, 'LlamaParse Premium tier ships layout-aware PDF parsing tuned for enterprise documents and complex tables.'),
    (589, '0195f300-1001-7000-b000-000000000019', 'FRAMEWORKS', 4, 'LlamaIndex recursive retriever enables multi-document reasoning by chaining sub-retrievals across collections.'),
    (590, '0195f300-1001-7000-b000-000000000019', 'FRAMEWORKS', 3, 'LlamaIndex Cloud adds managed ingestion pipelines with webhook triggers for event-driven knowledge updates.'),
    (591, '0195f300-1001-7000-b000-000000000019', 'FRAMEWORKS', 3, 'LlamaIndex Agents module adds ReAct, OpenAI, and Anthropic tool-calling variants under a unified interface.'),
    (592, '0195f300-1001-7000-b000-000000000019', 'FRAMEWORKS', 4, 'LlamaIndex sub-question query engine raises multi-hop QA accuracy by 22% via decomposition before retrieval.'),
    (593, '0195f300-1001-7000-b000-000000000019', 'FRAMEWORKS', 3, 'LlamaIndex TS reaches feature parity with the Python SDK for production TypeScript RAG applications.'),
    -- ChromaDB (594-600) — entity 01a
    (594, '0195f300-1001-7000-b000-00000000001a', 'FRAMEWORKS', 4, 'ChromaDB Cloud launches GA with per-collection SLAs, adding managed vector storage with enterprise guarantees.'),
    (595, '0195f300-1001-7000-b000-00000000001a', 'FRAMEWORKS', 3, 'ChromaDB server-side embedding functions hosted alongside data eliminate round trips for ingest pipelines.'),
    (596, '0195f300-1001-7000-b000-00000000001a', 'FRAMEWORKS', 3, 'ChromaDB distributed mode adds read replicas for geo-distributed workloads with bounded staleness reads.'),
    (597, '0195f300-1001-7000-b000-00000000001a', 'FRAMEWORKS', 4, 'ChromaDB sparse vector support enables SPLADE-style hybrid retrieval that combines lexical and semantic signals.'),
    (598, '0195f300-1001-7000-b000-00000000001a', 'FRAMEWORKS', 3, 'ChromaDB CLI adds snapshot export and import primitives for cross-environment migrations and backups.'),
    (599, '0195f300-1001-7000-b000-00000000001a', 'FRAMEWORKS', 3, 'ChromaDB benchmark hits 50K QPS on a single node for 768-dim vectors, validating its single-node scalability.'),
    (600, '0195f300-1001-7000-b000-00000000001a', 'FRAMEWORKS', 4, 'ChromaDB Edge SDK lands for browser-side vector search, enabling fully client-side RAG in privacy-first apps.'),

    -- =================== FRAMEWORKS: LLMOps ===================
    -- MLflow (601-608) — entity 01e
    (601, '0195f300-1001-7000-b000-00000000001e', 'FRAMEWORKS', 4, 'MLflow 3.2 adds a GenAI tracing spec compatible with OpenTelemetry, unifying GenAI observability with platform tools.'),
    (602, '0195f300-1001-7000-b000-00000000001e', 'FRAMEWORKS', 4, 'MLflow prompt registry GA delivers side-by-side diffs and version lineage for production prompt management.'),
    (603, '0195f300-1001-7000-b000-00000000001e', 'FRAMEWORKS', 4, 'MLflow Evaluate API adds built-in hallucination and toxicity judges, simplifying automated quality gates.'),
    (604, '0195f300-1001-7000-b000-00000000001e', 'FRAMEWORKS', 3, 'MLflow model registry adds multi-model aliasing for atomic production promotions across blue-green stacks.'),
    (605, '0195f300-1001-7000-b000-00000000001e', 'FRAMEWORKS', 3, 'MLflow tracing UI adds a latency heatmap across spans to surface bottlenecks in complex agent pipelines.'),
    (606, '0195f300-1001-7000-b000-00000000001e', 'FRAMEWORKS', 4, 'MLflow ships native LlamaIndex and LangGraph auto-logging so traces appear without manual instrumentation.'),
    (607, '0195f300-1001-7000-b000-00000000001e', 'FRAMEWORKS', 3, 'MLflow Skinny image cuts container size by 70% for edge LLM inference and serverless deployments.'),
    (608, '0195f300-1001-7000-b000-00000000001e', 'FRAMEWORKS', 3, 'MLflow Auth module adds OIDC SSO and group-based permissions for enterprise multi-team environments.'),
    -- Weights & Biases (609-615) — entity 067
    (609, '0195f300-1001-7000-b000-000000000067', 'FRAMEWORKS', 4, 'Weights & Biases Weave reaches GA for production GenAI trace capture with sub-50ms client overhead.'),
    (610, '0195f300-1001-7000-b000-000000000067', 'FRAMEWORKS', 3, 'Weights & Biases Models adds a cross-run diff viewer that aligns metrics, configs, and artifacts side by side.'),
    (611, '0195f300-1001-7000-b000-000000000067', 'FRAMEWORKS', 3, 'Weights & Biases Reports adds inline AI summarization to surface insights from long experiment narratives.'),
    (612, '0195f300-1001-7000-b000-000000000067', 'FRAMEWORKS', 3, 'Weights & Biases Sweeps engine adds multi-objective optimization with a Pareto-frontier UI for trade-offs.'),
    (613, '0195f300-1001-7000-b000-000000000067', 'FRAMEWORKS', 3, 'Weights & Biases launches a Dedicated Cloud tier on Azure for regulated industries with isolated tenancy.'),
    (614, '0195f300-1001-7000-b000-000000000067', 'FRAMEWORKS', 4, 'Weights & Biases Artifacts adds a lineage graph from dataset to model, simplifying reproducibility audits.'),
    (615, '0195f300-1001-7000-b000-000000000067', 'FRAMEWORKS', 3, 'Weights & Biases adds OpenTelemetry-compatible trace export from Weave sessions for unified observability.'),

    -- =================== FRAMEWORKS: Observability ===================
    -- Langfuse (616-623) — entity 01b
    (616, '0195f300-1001-7000-b000-00000000001b', 'FRAMEWORKS', 4, 'Langfuse 3.2 lands annotation queues that streamline human-in-the-loop evaluation of production traces.'),
    (617, '0195f300-1001-7000-b000-00000000001b', 'FRAMEWORKS', 3, 'Langfuse session-level cost aggregation powers user-facing billing dashboards for SaaS GenAI apps.'),
    (618, '0195f300-1001-7000-b000-00000000001b', 'FRAMEWORKS', 3, 'Langfuse datasets add CSV and JSONL bulk import to bootstrap eval sets from existing data sources.'),
    (619, '0195f300-1001-7000-b000-00000000001b', 'FRAMEWORKS', 3, 'Langfuse self-hosted Helm chart adds a Pulsar backend option for high-throughput production tracing.'),
    (620, '0195f300-1001-7000-b000-00000000001b', 'FRAMEWORKS', 4, 'Langfuse SDK auto-instrumentation now covers OpenAI, Anthropic, and Google SDKs without code changes.'),
    (621, '0195f300-1001-7000-b000-00000000001b', 'FRAMEWORKS', 3, 'Langfuse Playground adds side-by-side multi-model prompt comparison for quick A/B prompt evaluation.'),
    (622, '0195f300-1001-7000-b000-00000000001b', 'FRAMEWORKS', 4, 'Langfuse adds real-time Slack alerts for latency and cost anomaly detection on production traffic.'),
    (623, '0195f300-1001-7000-b000-00000000001b', 'FRAMEWORKS', 3, 'Langfuse v3 adds native multi-tenant mode tailored for SaaS platform builders embedding observability.'),
    -- LangSmith (624-630) — entity 068
    (624, '0195f300-1001-7000-b000-000000000068', 'FRAMEWORKS', 3, 'LangSmith Prompt Hub adds public sharing for community-curated templates discoverable across orgs.'),
    (625, '0195f300-1001-7000-b000-000000000068', 'FRAMEWORKS', 4, 'LangSmith online eval streams quality scores on live production traffic to detect regressions in minutes.'),
    (626, '0195f300-1001-7000-b000-000000000068', 'FRAMEWORKS', 3, 'LangSmith on-premise deployment option lands for regulated enterprise customers with strict data residency.'),
    (627, '0195f300-1001-7000-b000-000000000068', 'FRAMEWORKS', 3, 'LangSmith trace UI adds side-by-side run comparison for fast investigation of regressions across versions.'),
    (628, '0195f300-1001-7000-b000-000000000068', 'FRAMEWORKS', 3, 'LangSmith datasets ship a synthetic generation wizard that bootstraps eval sets from a few seed examples.'),
    (629, '0195f300-1001-7000-b000-000000000068', 'FRAMEWORKS', 4, 'LangSmith CI Action gates pull requests on eval score regressions, blocking merges that worsen quality.'),
    (630, '0195f300-1001-7000-b000-000000000068', 'FRAMEWORKS', 3, 'LangSmith adds token-level span inspection for streaming LLM workflows, helping debug partial outputs.'),

    -- =================== CASE_STUDIES ===================
    -- Claude (631-640) — entity Claude 3.7 Sonnet (000000000002)
    (631, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 4, 'Block deploys Claude 3.7 Sonnet across Square customer support, cutting average handle time by 28%.'),
    (632, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 4, 'Anthropic research paper studies reasoning trace faithfulness in Claude 3.7 across math and coding tasks.'),
    (633, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 4, 'Asana ships a workflow builder powered by Claude 3.7 with a 40% activation lift on new feature adoption.'),
    (634, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 4, 'Anthropic applied research quantifies Claude 3.7 tool-use reliability across long-horizon agent benchmarks.'),
    (635, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 4, 'Replit Agent migrates to Claude 3.7 Sonnet and reports 22% higher task success on coding agent benchmarks.'),
    (636, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 4, 'Anthropic study probes Claude 3.7 behavior under adversarial jailbreak suites for safety hardening.'),
    (637, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 3, 'Quora Poe adds Claude 3.7 Sonnet, driving an 18% increase in daily active sessions on the platform.'),
    (638, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 4, 'Anthropic applied research compares constitutional AI variants on Claude 3.7 to balance helpfulness and harmlessness.'),
    (639, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 3, 'Intercom Fin AI migrates to Claude 3.7, saving 35% on per-conversation inference costs at production scale.'),
    (640, '0195f300-1001-7000-b000-000000000002', 'CASE_STUDIES', 4, 'Anthropic research notes document Claude 3.7 long-context recall across million-token enterprise codebases.'),
    -- GPT (641-650) — entity GPT-5.4 (000000000001)
    (641, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 4, 'Morgan Stanley wealth advisors adopt GPT-5.4 for cross-desk research synthesis at firm-wide scale.'),
    (642, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 4, 'OpenAI applied research quantifies GPT-5.4 hallucination rates by domain and proposes mitigation recipes.'),
    (643, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 3, 'Shopify Inbox ships a GPT-5.4-powered auto-reply feature for merchant stores with measurable response gains.'),
    (644, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 5, 'OpenAI applied research measures GPT-5.4 reasoning robustness on math olympiad problems and ablation variants.'),
    (645, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 3, 'Zillow adds a GPT-5.4 listing description generator that lifts CTR on new property listings.'),
    (646, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 4, 'OpenAI research probes multi-agent coordination failures in GPT-5.4 swarms and proposes mitigation patterns.'),
    (647, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 3, 'Canva Magic Studio migrates to GPT-5.4 and reports 30% faster image captioning at production scale.'),
    (648, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 4, 'OpenAI applied research quantifies GPT-5.4 cost-latency Pareto curves across text, image, and audio modalities.'),
    (649, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 4, 'Klarna customer service bot powered by GPT-5.4 replaces about 700 agent workloads with sustained quality.'),
    (650, '0195f300-1001-7000-b000-000000000001', 'CASE_STUDIES', 4, 'OpenAI research studies the safety tax across GPT-5.4 pre-trained variants under standardized red-team probes.'),
    -- Gemini (651-660) — entity Gemini 2.0 Flash (000000000003)
    (651, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 3, 'Spotify DJ feature migrates to Gemini 2.0 Flash for real-time music commentary at sub-second latency.'),
    (652, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 4, 'Google DeepMind applied research quantifies Gemini 2.0 Flash multimodal recall across video, audio, and text.'),
    (653, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 3, 'Snap Inc. powers My AI with Gemini 2.0 Flash for sub-second response latency on mobile devices.'),
    (654, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 4, 'Google research probes Gemini 2.0 Flash behavior on long-horizon agentic tasks with tool use.'),
    (655, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 4, 'eBay adds a Gemini 2.0 Flash listing assistant and boosts seller throughput by 35% on new listings.'),
    (656, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 4, 'Google DeepMind studies Gemini 2.0 Flash calibration on uncertain user queries and refusal rates.'),
    (657, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 3, 'Adobe Express adds Gemini 2.0 Flash for real-time photo edit suggestions in the desktop and mobile apps.'),
    (658, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 4, 'Google applied research compares Gemini 2.0 Flash and Gemini Pro on coding tasks across cost-quality axes.'),
    (659, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 3, 'Reddit Answers feature switches to Gemini 2.0 Flash for snappy conversational summaries on discussions.'),
    (660, '0195f300-1001-7000-b000-000000000003', 'CASE_STUDIES', 4, 'Google DeepMind applied research maps Gemini 2.0 Flash failure modes across vision-language tasks.'),

    -- =================== PAPER_BENCHMARK ===================
    -- MMLU-Pro (661-665) — entity 050
    (661, '0195f300-1001-7000-b000-000000000050', 'PAPER_BENCHMARK', 4, 'MMLU-Pro April 2026 update adds 1500 new reasoning-heavy questions to mitigate eval saturation by frontier models.'),
    (662, '0195f300-1001-7000-b000-000000000050', 'PAPER_BENCHMARK', 4, 'MMLU-Pro leaderboard shows the top open-source model closing the gap to GPT-5.4 within 2 accuracy points.'),
    (663, '0195f300-1001-7000-b000-000000000050', 'PAPER_BENCHMARK', 4, 'MMLU-Pro authors release a contamination audit tool to verify training-data leakage in submitted models.'),
    (664, '0195f300-1001-7000-b000-000000000050', 'PAPER_BENCHMARK', 3, 'MMLU-Pro multilingual edition adds 26 language splits, expanding eval coverage beyond English-only reasoning.'),
    (665, '0195f300-1001-7000-b000-000000000050', 'PAPER_BENCHMARK', 3, 'MMLU-Pro per-question cost report reveals reasoning models spend roughly 8x more tokens than non-reasoning peers.'),
    -- SWE-bench (666-670) — entity 051
    (666, '0195f300-1001-7000-b000-000000000051', 'PAPER_BENCHMARK', 4, 'SWE-bench Verified April 2026 update adds 200 new issues sampled from top OSS repositories for harder eval coverage.'),
    (667, '0195f300-1001-7000-b000-000000000051', 'PAPER_BENCHMARK', 5, 'SWE-bench Live shows top coding agents now solving 78% of real GitHub issues, up from 73% at the start of 2026.'),
    (668, '0195f300-1001-7000-b000-000000000051', 'PAPER_BENCHMARK', 4, 'SWE-bench long-context track adds repositories over 1 million lines of code, stressing whole-repo reasoning.'),
    (669, '0195f300-1001-7000-b000-000000000051', 'PAPER_BENCHMARK', 4, 'SWE-bench cost track compares agent spend per solved issue across vendors, surfacing efficiency leaders.'),
    (670, '0195f300-1001-7000-b000-000000000051', 'PAPER_BENCHMARK', 4, 'SWE-bench Multimodal track lands with UI bug reports and screenshot inputs, broadening the eval to visual tasks.'),
    -- GPQA Diamond (671-675) — entity 052
    (671, '0195f300-1001-7000-b000-000000000052', 'PAPER_BENCHMARK', 3, 'GPQA Diamond 2026 refresh closes 50 newly contaminated questions to keep eval integrity intact for frontier models.'),
    (672, '0195f300-1001-7000-b000-000000000052', 'PAPER_BENCHMARK', 5, 'GPQA Diamond live leaderboard reports the top reasoning model hitting 91% pass rate, beyond expert human average.'),
    (673, '0195f300-1001-7000-b000-000000000052', 'PAPER_BENCHMARK', 3, 'GPQA Diamond domain breakdown shows chemistry as the hardest sub-section for current LLMs across vendors.'),
    (674, '0195f300-1001-7000-b000-000000000052', 'PAPER_BENCHMARK', 3, 'GPQA Diamond authors publish a best-practice prompting guide to standardize fair model comparisons.'),
    (675, '0195f300-1001-7000-b000-000000000052', 'PAPER_BENCHMARK', 3, 'GPQA Diamond tool-use variant lets models browse references during eval, isolating reasoning from recall.'),

    -- =================== TOOLS ===================
    -- Cursor (676-680) — entity 020
    (676, '0195f300-1001-7000-b000-000000000020', 'TOOLS', 5, 'Cursor 0.55 adds a background composer that runs long multi-file refactors without blocking the editor.'),
    (677, '0195f300-1001-7000-b000-000000000020', 'TOOLS', 4, 'Cursor adds native Jupyter notebook mode with in-cell AI editing, expanding its data-science workflow coverage.'),
    (678, '0195f300-1001-7000-b000-000000000020', 'TOOLS', 4, 'Cursor Privacy Mode v2 routes all inference to self-hosted endpoints, satisfying strict enterprise data policies.'),
    (679, '0195f300-1001-7000-b000-000000000020', 'TOOLS', 4, 'Cursor Agents Mode adds a browser sandbox that lets agents verify changes against live web applications.'),
    (680, '0195f300-1001-7000-b000-000000000020', 'TOOLS', 3, 'Cursor reaches 5 million paid seats as enterprise adoption of AI editors accelerates in Q1 2026.'),
    -- GitHub Copilot (681-685) — entity 021
    (681, '0195f300-1001-7000-b000-000000000021', 'TOOLS', 4, 'GitHub Copilot Spaces adds repo-aware long-context multi-file reasoning for whole-codebase questions.'),
    (682, '0195f300-1001-7000-b000-000000000021', 'TOOLS', 4, 'GitHub Copilot adds Anthropic Claude as a selectable backend for Pro+ users, broadening model choice.'),
    (683, '0195f300-1001-7000-b000-000000000021', 'TOOLS', 4, 'GitHub Copilot Workspace now auto-generates test suites alongside code changes for PR-ready submissions.'),
    (684, '0195f300-1001-7000-b000-000000000021', 'TOOLS', 4, 'GitHub Copilot Code Review adds severity-tagged suggestions inside PR conversations to focus reviewer attention.'),
    (685, '0195f300-1001-7000-b000-000000000021', 'TOOLS', 3, 'GitHub Copilot mobile lands on iOS and Android with voice-driven Q&A mode for on-the-go developer queries.'),
    -- Claude Code (686-690) — entity 022
    (686, '0195f300-1001-7000-b000-000000000022', 'TOOLS', 5, 'Claude Code 0.20 adds background worktree mode that runs parallel multi-branch sessions in isolated workspaces.'),
    (687, '0195f300-1001-7000-b000-000000000022', 'TOOLS', 4, 'Claude Code adds a native hooks system for pre-tool and post-tool custom logic, enabling per-team policies.'),
    (688, '0195f300-1001-7000-b000-000000000022', 'TOOLS', 4, 'Claude Code Skills marketplace lets teams share reusable slash commands across projects and organizations.'),
    (689, '0195f300-1001-7000-b000-000000000022', 'TOOLS', 4, 'Claude Code Plan Mode adds a branching plan editor with reviewer approval flow for risky changes.'),
    (690, '0195f300-1001-7000-b000-000000000022', 'TOOLS', 4, 'Claude Code cron skill lets agents self-schedule recurring background tasks with minute-level granularity.'),

    -- =================== REGULATIONS ===================
    -- EU AI Act (691-693) — entity 060
    (691, '0195f300-1001-7000-b000-000000000060', 'REGULATIONS', 4, 'EU AI Act schedules the first round of GPAI compliance audits for May 2026, opening enforcement under the new code.'),
    (692, '0195f300-1001-7000-b000-000000000060', 'REGULATIONS', 3, 'EU AI Act Office publishes an updated Code of Practice for foundation model providers covering documentation requirements.'),
    (693, '0195f300-1001-7000-b000-000000000060', 'REGULATIONS', 3, 'EU AI Act member-state coordinators hold their first joint enforcement working group to align cross-border practice.'),
    -- NIST AI RMF (694-695) — entity 061
    (694, '0195f300-1001-7000-b000-000000000061', 'REGULATIONS', 4, 'NIST releases AI RMF 2.0 Profile for generative AI risk management, including hallucination and provenance controls.'),
    (695, '0195f300-1001-7000-b000-000000000061', 'REGULATIONS', 3, 'NIST AI RMF crosswalk maps controls to ISO 42001, easing joint compliance programs for multinational teams.'),

    -- =================== SHARED_RESOURCES ===================
    -- Hugging Face (696-698) — entity 030
    (696, '0195f300-1001-7000-b000-000000000030', 'SHARED_RESOURCES', 3, 'Hugging Face Spaces adds a persistent storage tier for stateful demo applications that need durable user data.'),
    (697, '0195f300-1001-7000-b000-000000000030', 'SHARED_RESOURCES', 4, 'Hugging Face adds trust-and-safety scanning for all new public model uploads to flag risky weights pre-publication.'),
    (698, '0195f300-1001-7000-b000-000000000030', 'SHARED_RESOURCES', 3, 'Hugging Face Datasets adds streaming mode for trillion-token pretraining sets without local storage requirements.'),
    -- Papers with Code (699-700) — entity 031
    (699, '0195f300-1001-7000-b000-000000000031', 'SHARED_RESOURCES', 3, 'Papers with Code adds a live trending-papers feed ranked by author reputation and citation velocity.'),
    (700, '0195f300-1001-7000-b000-000000000031', 'SHARED_RESOURCES', 3, 'Papers with Code datasets index crosses 12K reproducible benchmark sets across vision, language, and multimodal tasks.')
    ) AS t(seq, entity_id, page, score, summary)
) LOOP
    i := i + 1;

    -- article_raw id (d prefix for seq 501-700)
    v_art_id := format('0195f300-d%s-7000-8000-000000000001', lpad(rec.seq::text, 3, '0'))::UUID;

    -- published_at from article_raw
    SELECT published_at INTO v_pub_at
    FROM content.article_raw
    WHERE id = v_art_id;

    IF v_pub_at IS NULL THEN
        RAISE NOTICE 'Skipping seq %: article_raw not found (run stage-1-extra-new-200-v2.sql first)', rec.seq;
        skipped := skipped + 1;
        CONTINUE;
    END IF;

    -- user_article_state id (lookup by article_raw_id + system user)
    SELECT id INTO v_uas_id
    FROM content.user_article_state
    WHERE article_raw_id = v_art_id
      AND user_id = v_user_id
      AND revoked_at IS NULL
    LIMIT 1;

    IF v_uas_id IS NULL THEN
        RAISE NOTICE 'Skipping seq %: user_article_state not found (run ingest-bulk API first)', rec.seq;
        skipped := skipped + 1;
        CONTINUE;
    END IF;

    -- user_article_ai_state id (must be PENDING)
    SELECT id INTO v_aai_id
    FROM content.user_article_ai_state
    WHERE user_article_state_id = v_uas_id
      AND ai_status = 'PENDING'
    LIMIT 1;

    IF v_aai_id IS NULL THEN
        RAISE NOTICE 'Skipping seq %: PENDING ai_state not found (run pregen-ai-state API first)', rec.seq;
        skipped := skipped + 1;
        CONTINUE;
    END IF;

    -- Write agent_json_raw in v0.3 nested format (ai_status stays PENDING)
    UPDATE content.user_article_ai_state
    SET
        agent_json_raw = jsonb_build_object(
            'representative_entity', jsonb_build_object(
                'id',   rec.entity_id,
                'page', rec.page
            ),
            'side_category_code',
              CASE
                WHEN rec.page = 'CASE_STUDIES' THEN
                  CASE
                    -- APPLIED_RESEARCH: research/lab papers (15)
                    WHEN rec.seq IN (632, 634, 636, 638, 640,
                                     642, 644, 646, 648, 650,
                                     652, 654, 656, 658, 660)
                      THEN 'APPLIED_RESEARCH'
                    -- CASE_STUDY: deployment/customer stories (15)
                    ELSE 'CASE_STUDY'
                  END
                ELSE NULL
              END,
            'ai_summary', rec.summary,
            'ai_score',   rec.score,
            'ai_model_name', 'claude-opus-4-6'
        ),
        ai_model_name   = 'claude-opus-4-6',
        ai_processed_at = v_pub_at + INTERVAL '2 hours',
        updated_at      = NOW()
    WHERE id = v_aai_id;

END LOOP;

RAISE NOTICE 'Done: processed % records, skipped %', i - skipped, skipped;
END $$;

COMMIT;
