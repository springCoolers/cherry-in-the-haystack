-- ============================================================
-- Stage 1 Extra — FRAMEWORKS 50개 추가 (아티클 목록용)
-- seq 201 ~ 250
-- Prerequisites: stage-0-foundation.sql, stage-1-article-raw.sql
-- ============================================================

BEGIN;

INSERT INTO content.article_raw (id, source_id, title, url, published_at, representative_key, language)
VALUES
-- =================== Agent (12개) ===================
-- LangChain (3)
('0195f300-b201-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LangChain v0.3 Simplified Chain API Released',                 'https://example.com/fw-201', '2026-04-07T09:00:00+09:00', 'seed-fw-201-' || md5('LangChain v0.3 Simplified Chain API Released'),                 'en'),
('0195f300-b202-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LangChain Adds Native Tool Calling Support',                    'https://example.com/fw-202', '2026-04-03T09:00:00+09:00', 'seed-fw-202-' || md5('LangChain Adds Native Tool Calling Support'),                    'en'),
('0195f300-b203-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'LangChain Expression Language (LCEL) Performance Improvements', 'https://example.com/fw-203', '2026-03-28T09:00:00+09:00', 'seed-fw-203-' || md5('LangChain Expression Language (LCEL) Performance Improvements'), 'en'),
-- LangGraph (3)
('0195f300-b204-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LangGraph 0.3 State Management Overhaul',                       'https://example.com/fw-204', '2026-04-06T09:00:00+09:00', 'seed-fw-204-' || md5('LangGraph 0.3 State Management Overhaul'),                       'en'),
('0195f300-b205-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LangGraph Human-in-the-Loop Patterns Guide',                    'https://example.com/fw-205', '2026-04-01T09:00:00+09:00', 'seed-fw-205-' || md5('LangGraph Human-in-the-Loop Patterns Guide'),                    'en'),
('0195f300-b206-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'LangGraph Multi-Agent Supervisor Pattern Deep Dive',            'https://example.com/fw-206', '2026-03-25T09:00:00+09:00', 'seed-fw-206-' || md5('LangGraph Multi-Agent Supervisor Pattern Deep Dive'),            'en'),
-- CrewAI (3)
('0195f300-b207-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'CrewAI 0.86 Adds Task Dependencies and Async Execution',        'https://example.com/fw-207', '2026-04-05T09:00:00+09:00', 'seed-fw-207-' || md5('CrewAI 0.86 Adds Task Dependencies and Async Execution'),        'en'),
('0195f300-b208-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'CrewAI Enterprise Features: Memory and Knowledge Bases',        'https://example.com/fw-208', '2026-03-30T09:00:00+09:00', 'seed-fw-208-' || md5('CrewAI Enterprise Features: Memory and Knowledge Bases'),        'en'),
-- AutoGPT (3)
('0195f300-b209-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'AutoGPT Platform v0.4 Launches with Visual Workflow Builder',   'https://example.com/fw-209', '2026-04-08T09:00:00+09:00', 'seed-fw-209-' || md5('AutoGPT Platform v0.4 Launches with Visual Workflow Builder'),   'en'),
('0195f300-b210-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000007', 'AutoGPT Benchmarks: 168k GitHub Stars Milestone',              'https://example.com/fw-210', '2026-04-02T09:00:00+09:00', 'seed-fw-210-' || md5('AutoGPT Benchmarks: 168k GitHub Stars Milestone'),              'en'),
('0195f300-b211-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'AutoGPT Forge SDK for Custom Agent Development',               'https://example.com/fw-211', '2026-03-27T09:00:00+09:00', 'seed-fw-211-' || md5('AutoGPT Forge SDK for Custom Agent Development'),               'en'),

-- =================== Fine-Tuning (8개) ===================
-- Unsloth (4)
('0195f300-b212-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'Unsloth v2026.3 Adds Llama 4 Scout Support',                   'https://example.com/fw-212', '2026-04-04T09:00:00+09:00', 'seed-fw-212-' || md5('Unsloth v2026.3 Adds Llama 4 Scout Support'),                   'en'),
('0195f300-b213-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'Unsloth 2x Faster Fine-tuning with 60% Less VRAM',             'https://example.com/fw-213', '2026-03-31T09:00:00+09:00', 'seed-fw-213-' || md5('Unsloth 2x Faster Fine-tuning with 60% Less VRAM'),             'en'),
('0195f300-b214-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'Unsloth GGUFification: Direct GGUF Export Support',            'https://example.com/fw-214', '2026-03-26T09:00:00+09:00', 'seed-fw-214-' || md5('Unsloth GGUFification: Direct GGUF Export Support'),            'en'),
('0195f300-b215-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000007', 'Unsloth vs LoRA Benchmarks: Speed and Memory Analysis',        'https://example.com/fw-215', '2026-04-07T09:00:00+09:00', 'seed-fw-215-' || md5('Unsloth vs LoRA Benchmarks: Speed and Memory Analysis'),        'en'),
-- LLaMA-Factory (4)
('0195f300-b216-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LLaMA-Factory v0.9 Unifies SFT, DPO, and RLHF Pipelines',     'https://example.com/fw-216', '2026-04-06T09:00:00+09:00', 'seed-fw-216-' || md5('LLaMA-Factory v0.9 Unifies SFT, DPO, and RLHF Pipelines'),     'en'),
('0195f300-b217-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LLaMA-Factory Web UI Now Supports Multi-GPU Training',         'https://example.com/fw-217', '2026-04-01T09:00:00+09:00', 'seed-fw-217-' || md5('LLaMA-Factory Web UI Now Supports Multi-GPU Training'),         'en'),
('0195f300-b218-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LLaMA-Factory Adds Qwen3 and Gemma 3 Model Support',           'https://example.com/fw-218', '2026-03-27T09:00:00+09:00', 'seed-fw-218-' || md5('LLaMA-Factory Adds Qwen3 and Gemma 3 Model Support'),           'en'),
('0195f300-b219-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'LLaMA-Factory ORPO Training Method Integration',               'https://example.com/fw-219', '2026-03-22T09:00:00+09:00', 'seed-fw-219-' || md5('LLaMA-Factory ORPO Training Method Integration'),               'en'),

-- =================== RAG (9개) ===================
-- RAGFlow (3)
('0195f300-b220-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'RAGFlow v0.14 Adds GraphRAG and Hybrid Search',                'https://example.com/fw-220', '2026-04-07T09:00:00+09:00', 'seed-fw-220-' || md5('RAGFlow v0.14 Adds GraphRAG and Hybrid Search'),                'en'),
('0195f300-b221-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'RAGFlow Chunking Strategies: DeepDoc vs Standard',             'https://example.com/fw-221', '2026-04-02T09:00:00+09:00', 'seed-fw-221-' || md5('RAGFlow Chunking Strategies: DeepDoc vs Standard'),             'en'),
('0195f300-b222-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'RAGFlow Enterprise: Multi-Tenant Knowledge Base Management',   'https://example.com/fw-222', '2026-03-28T09:00:00+09:00', 'seed-fw-222-' || md5('RAGFlow Enterprise: Multi-Tenant Knowledge Base Management'),   'en'),
-- Haystack (3)
('0195f300-b223-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'Haystack 2.0 Declarative Pipeline YAML Configuration',        'https://example.com/fw-223', '2026-04-05T09:00:00+09:00', 'seed-fw-223-' || md5('Haystack 2.0 Declarative Pipeline YAML Configuration'),        'en'),
('0195f300-b224-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'Haystack Adds Native Cohere and Mistral Integrations',         'https://example.com/fw-224', '2026-03-29T09:00:00+09:00', 'seed-fw-224-' || md5('Haystack Adds Native Cohere and Mistral Integrations'),         'en'),
-- RAGAS (3)
('0195f300-b225-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'RAGAS v0.2 Introduces Testset Generation from Documents',      'https://example.com/fw-225', '2026-04-08T09:00:00+09:00', 'seed-fw-225-' || md5('RAGAS v0.2 Introduces Testset Generation from Documents'),      'en'),
('0195f300-b226-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'RAGAS Context Precision vs Recall: Evaluation Guide',          'https://example.com/fw-226', '2026-04-03T09:00:00+09:00', 'seed-fw-226-' || md5('RAGAS Context Precision vs Recall: Evaluation Guide'),          'en'),
('0195f300-b227-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'RAGAS Supports LangChain and LlamaIndex Native Evaluation',    'https://example.com/fw-227', '2026-03-25T09:00:00+09:00', 'seed-fw-227-' || md5('RAGAS Supports LangChain and LlamaIndex Native Evaluation'),    'en'),

-- =================== Serving (8개) ===================
-- vLLM (4)
('0195f300-b228-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'vLLM v0.8 Speculative Decoding and Chunked Prefill',           'https://example.com/fw-228', '2026-04-06T09:00:00+09:00', 'seed-fw-228-' || md5('vLLM v0.8 Speculative Decoding and Chunked Prefill'),           'en'),
('0195f300-b229-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000007', 'vLLM Production Deployment on Kubernetes Guide',               'https://example.com/fw-229', '2026-04-01T09:00:00+09:00', 'seed-fw-229-' || md5('vLLM Production Deployment on Kubernetes Guide'),               'en'),
('0195f300-b230-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'vLLM OpenAI-Compatible Server: Multi-Modal Support Added',     'https://example.com/fw-230', '2026-03-27T09:00:00+09:00', 'seed-fw-230-' || md5('vLLM OpenAI-Compatible Server: Multi-Modal Support Added'),     'en'),
('0195f300-b231-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'vLLM vs TensorRT-LLM: Throughput Benchmark 2026',             'https://example.com/fw-231', '2026-03-22T09:00:00+09:00', 'seed-fw-231-' || md5('vLLM vs TensorRT-LLM: Throughput Benchmark 2026'),             'en'),
-- Ollama (4)
('0195f300-b232-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000007', 'Ollama v0.6 Adds Model Context Caching',                       'https://example.com/fw-232', '2026-04-07T09:00:00+09:00', 'seed-fw-232-' || md5('Ollama v0.6 Adds Model Context Caching'),                       'en'),
('0195f300-b233-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000007', 'Ollama Multimodal Streaming Stability Improvements',           'https://example.com/fw-233', '2026-04-02T09:00:00+09:00', 'seed-fw-233-' || md5('Ollama Multimodal Streaming Stability Improvements'),           'en'),
('0195f300-b234-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'Ollama REST API: Batch Completion Endpoint Added',             'https://example.com/fw-234', '2026-03-28T09:00:00+09:00', 'seed-fw-234-' || md5('Ollama REST API: Batch Completion Endpoint Added'),             'en'),
('0195f300-b235-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'Ollama Docker Compose Setup for Local LLM Lab',                'https://example.com/fw-235', '2026-03-23T09:00:00+09:00', 'seed-fw-235-' || md5('Ollama Docker Compose Setup for Local LLM Lab'),                'en'),

-- =================== Data & Storage (6개) ===================
-- LlamaIndex (3)
('0195f300-b236-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LlamaIndex v0.12 Hybrid Search Pipeline Overhaul',             'https://example.com/fw-236', '2026-04-05T09:00:00+09:00', 'seed-fw-236-' || md5('LlamaIndex v0.12 Hybrid Search Pipeline Overhaul'),             'en'),
('0195f300-b237-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LlamaIndex PropertyGraphIndex for Knowledge Graph RAG',        'https://example.com/fw-237', '2026-03-31T09:00:00+09:00', 'seed-fw-237-' || md5('LlamaIndex PropertyGraphIndex for Knowledge Graph RAG'),        'en'),
('0195f300-b238-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'LlamaIndex Workflow API: Event-Driven Agent Orchestration',    'https://example.com/fw-238', '2026-03-26T09:00:00+09:00', 'seed-fw-238-' || md5('LlamaIndex Workflow API: Event-Driven Agent Orchestration'),    'en'),
-- ChromaDB (3)
('0195f300-b239-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'ChromaDB 0.6 Persistent Client and Multi-Collection Support',  'https://example.com/fw-239', '2026-04-04T09:00:00+09:00', 'seed-fw-239-' || md5('ChromaDB 0.6 Persistent Client and Multi-Collection Support'),  'en'),
('0195f300-b240-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'ChromaDB Metadata Filtering: Advanced Query Patterns',         'https://example.com/fw-240', '2026-03-29T09:00:00+09:00', 'seed-fw-240-' || md5('ChromaDB Metadata Filtering: Advanced Query Patterns'),         'en'),
('0195f300-b241-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000005', 'ChromaDB vs Pinecone vs Weaviate: 2026 Vector DB Comparison',  'https://example.com/fw-241', '2026-03-24T09:00:00+09:00', 'seed-fw-241-' || md5('ChromaDB vs Pinecone vs Weaviate: 2026 Vector DB Comparison'),  'en'),

-- =================== LLMOps (4개) ===================
-- MLflow (4)
('0195f300-b242-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'MLflow 3.0 AI Gateway and Prompt Engineering UI',             'https://example.com/fw-242', '2026-04-06T09:00:00+09:00', 'seed-fw-242-' || md5('MLflow 3.0 AI Gateway and Prompt Engineering UI'),             'en'),
('0195f300-b243-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'MLflow LLM Evaluate: Automated Model Comparison Pipeline',     'https://example.com/fw-243', '2026-04-01T09:00:00+09:00', 'seed-fw-243-' || md5('MLflow LLM Evaluate: Automated Model Comparison Pipeline'),     'en'),
('0195f300-b244-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'MLflow Tracing API for LLM Call Instrumentation',             'https://example.com/fw-244', '2026-03-27T09:00:00+09:00', 'seed-fw-244-' || md5('MLflow Tracing API for LLM Call Instrumentation'),             'en'),
('0195f300-b245-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000007', 'MLflow vs Weights and Biases: LLMOps Platform Shootout',      'https://example.com/fw-245', '2026-03-22T09:00:00+09:00', 'seed-fw-245-' || md5('MLflow vs Weights and Biases: LLMOps Platform Shootout'),      'en'),

-- =================== Observability (3개) ===================
-- Langfuse (3)
('0195f300-b246-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'Langfuse v3 Real-Time LLM Observability Dashboard',           'https://example.com/fw-246', '2026-04-07T09:00:00+09:00', 'seed-fw-246-' || md5('Langfuse v3 Real-Time LLM Observability Dashboard'),           'en'),
('0195f300-b247-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'Langfuse Token Cost Tracking and Budget Alerts',               'https://example.com/fw-247', '2026-04-03T09:00:00+09:00', 'seed-fw-247-' || md5('Langfuse Token Cost Tracking and Budget Alerts'),               'en'),
('0195f300-b248-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'Langfuse Scores API: Custom Evaluation Metrics',              'https://example.com/fw-248', '2026-03-29T09:00:00+09:00', 'seed-fw-248-' || md5('Langfuse Scores API: Custom Evaluation Metrics'),              'en'),

-- =================== Prompt Engineering (2개) ===================
-- DSPy (2)
('0195f300-b249-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'DSPy 2.5 MIPROv2 Optimizer for Automated Prompt Tuning',      'https://example.com/fw-249', '2026-04-05T09:00:00+09:00', 'seed-fw-249-' || md5('DSPy 2.5 MIPROv2 Optimizer for Automated Prompt Tuning'),      'en'),
('0195f300-b250-7000-8000-000000000001', '0195f300-0001-7000-a000-000000000006', 'DSPy vs Manual Prompting: Benchmark Results on GPT-5',        'https://example.com/fw-250', '2026-03-30T09:00:00+09:00', 'seed-fw-250-' || md5('DSPy vs Manual Prompting: Benchmark Results on GPT-5'),        'en')
ON CONFLICT (id) DO NOTHING;

COMMIT;
