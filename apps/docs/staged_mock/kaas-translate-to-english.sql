-- ============================================
-- Cherry KaaS — Translate Korean seed data to English
-- Target: kaas.concept (summary, content_md) + kaas.evidence (summary, comment)
-- Usage: psql ... -f kaas-translate-to-english.sql
--        or run via DBeaver / admin UI
-- Idempotent: safe to re-run (UPDATE matches existing ids)
-- ============================================

BEGIN;

-- ============================================
-- kaas.concept — summary + content_md
-- ============================================

-- RAG
UPDATE kaas.concept SET
  summary = 'A technique that dynamically injects external knowledge into LLM responses at inference time to improve accuracy. Combines vector DB search with generative models to reduce hallucination and reflect up-to-date information.',
  content_md = E'# Retrieval-Augmented Generation (RAG)\n\n## Overview\nRAG retrieves relevant documents from an external knowledge source before the LLM generates a response, injecting them as context.\n\n## Core Components\n1. **Retriever**: searches vector DB for relevant documents\n2. **Generator**: receives retrieved docs as context and produces the answer\n3. **Vector Store**: stores document embeddings and performs ANN search\n\n## Implementation Patterns\n- Naive RAG: simple retrieve → generate (~60% accuracy)\n- Advanced RAG: Hybrid search + Reranking (85%+ accuracy)\n- Contextual RAG: adds context prefix to chunks (67% fewer failures)\n\n## Code Example\n```python\nfrom langchain.chains import RetrievalQA\nqa_chain = RetrievalQA.from_chain_type(\n    llm=ChatOpenAI(model="gpt-4"),\n    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),\n    chain_type="stuff"\n)\nresult = qa_chain.run("What is RAG?")\n```\n\n## Key Metrics\n- Precision@k: fraction of relevant docs in top-k results\n- Recall@k: fraction of all relevant docs retrieved\n- MRR: reciprocal rank of the first relevant doc'
WHERE id = 'rag';

-- Chain-of-Thought
UPDATE kaas.concept SET
  summary = 'A prompting technique that makes LLMs explicitly produce intermediate reasoning steps before the final answer. Dramatically improves performance on math, logic, and multi-step reasoning tasks.',
  content_md = E'# Chain-of-Thought (CoT) Prompting\n\n## Overview\nCoT guides the LLM to explicitly produce intermediate reasoning steps before the final answer.\n\n## Main Variants\n1. **Few-shot CoT**: show reasoning steps alongside examples\n2. **Zero-shot CoT**: a single line — "Let''s think step by step"\n3. **Self-Consistency**: majority vote across several reasoning paths\n4. **Tree-of-Thought**: explore reasoning branches as a tree\n\n## Effect\n- GSM8K benchmark: +20% accuracy vs. baseline (Wei et al. 2022)\n- Zero-shot CoT alone produces dramatic gains (Kojima et al.)\n\n## Prompt Example\n```\nQ: Roger has 5 tennis balls. He buys 2 more cans of 3. How many does he have?\n\nA: Let''s think step by step.\n1. Roger starts with 5 balls.\n2. He buys 2 cans × 3 balls = 6 balls.\n3. Total: 5 + 6 = 11 balls.\nThe answer is 11.\n```'
WHERE id = 'chain-of-thought';

-- Embeddings
UPDATE kaas.concept SET
  summary = 'Techniques for converting text into high-dimensional dense vectors to measure semantic similarity. Vector DBs store these embeddings and use ANN search to find similar documents quickly.',
  content_md = E'# Embeddings & Vector Databases\n\n## What is an Embedding?\nA technique that converts text into high-dimensional dense vectors so that semantic similarity can be quantified.\n\n## Key Models\n- **text-embedding-3-large** (OpenAI): 3072 dims, Matryoshka representation\n- **BGE-M3** (BAAI): multilingual, sparse+dense hybrid\n- **Cohere embed-v3**: multilingual, retrieval-optimized\n\n## Vector DB Comparison\n| DB | Index | Notes |\n|---|---|---|\n| Pinecone | Proprietary | Fully managed |\n| Weaviate | HNSW | Hybrid search |\n| Qdrant | HNSW | Rust-based, high performance |\n| Milvus | IVF+PQ | Large-scale data |\n\n## Key Concepts\n- **ANN (Approximate Nearest Neighbor)**: trade small accuracy loss for large speedups\n- **HNSW**: most general-purpose recall-latency tradeoff\n- **Cosine similarity**: measures similarity via vector angle'
WHERE id = 'embeddings';

-- Fine-tuning
UPDATE kaas.concept SET
  summary = 'Additional training of a pre-trained LLM for a specific domain or task. Parameter-efficient methods such as LoRA and QLoRA dramatically reduce GPU cost.',
  content_md = E'# Fine-tuning & PEFT\n\n## Overview\nAdditional training of a pre-trained LLM tailored to a specific domain or task.\n\n## PEFT Methods\n1. **LoRA**: Low-Rank Adaptation. Trains ~0.1% of params with performance close to full fine-tuning\n2. **QLoRA**: 4-bit quantization + LoRA. Trains 65B models on a single GPU\n3. **Prefix Tuning**: prepend learnable prefix tokens to inputs\n4. **Adapter**: insert small adapter modules per layer\n\n## When to Fine-tune\n- Need domain-specific vocabulary/style\n- Prompting alone is insufficient\n- Need consistent output format\n\n## Code Example (LoRA with PEFT)\n```python\nfrom peft import LoraConfig, get_peft_model\nconfig = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"])\nmodel = get_peft_model(base_model, config)\n```'
WHERE id = 'fine-tuning';

-- Multi-Agent
UPDATE kaas.concept SET
  summary = 'Architectures where multiple AI agents divide roles and collaborate to perform complex tasks.',
  content_md = E'# Multi-Agent Systems\n\n## Overview\nAn architecture where multiple AI agents take distinct roles and collaborate to complete complex tasks.\n\n## Major Frameworks\n1. **AutoGen** (Microsoft): conversation-based, strong for code generation\n2. **CrewAI**: role-based orchestration, natural-language workflows\n3. **LangGraph**: state-machine-based, great for complex branching\n\n## Design Patterns\n- **Supervisor**: central agent distributes tasks to sub-agents\n- **Peer-to-peer**: agents converse directly with each other\n- **Hierarchical**: multi-level delegation structure\n\n## Considerations\n- Inter-agent communication protocols (A2A, MCP)\n- Shared vs isolated memory\n- Failure handling and retries'
WHERE id = 'multi-agent';

-- Evaluation
UPDATE kaas.concept SET
  summary = 'Systematic measurement of LLM output quality. Combines LLM-as-judge and human evaluation to assess accuracy, usefulness, and safety.',
  content_md = E'# LLM Evaluation & Benchmarks\n\n## Evaluation Methods\n1. **Automatic metrics**: BLEU, ROUGE, BERTScore\n2. **LLM-as-Judge**: GPT-4 judges output quality (80%+ agreement with human evaluation)\n3. **Human evaluation**: directly rate accuracy, usefulness, safety\n\n## Key Benchmarks\n- **MMLU**: multi-domain knowledge test\n- **HumanEval**: code generation ability\n- **GSM8K**: math reasoning\n- **TruthfulQA**: factuality verification\n\n## Multi-dimensional Evaluation Framework\n- Factual accuracy\n- Toxicity / bias\n- Consistency across prompts\n- Instruction following\n\n## Practical Tips\n- Multi-dimensional evaluation is more reliable than a single benchmark\n- Build domain-specific evaluation datasets'
WHERE id = 'evaluation';

-- Prompt Engineering
UPDATE kaas.concept SET
  summary = 'Techniques for systematically designing prompts to produce desired LLM outputs.',
  content_md = E'# Prompt Engineering\n\n## Core Principles\n1. **Specific instructions**: state requests unambiguously\n2. **Use delimiters**: separate sections with XML tags or markdown\n3. **Break down tasks**: decompose complex work into smaller steps\n4. **Provide examples**: use few-shot to demonstrate desired output\n\n## Advanced Techniques\n- **System Prompt**: set role, tone, and constraints\n- **Few-shot Learning**: teach the pattern with 2-5 examples\n- **Chain-of-Thought**: elicit reasoning steps\n- **XML Tags**: improve Claude consistency by ~40%\n\n## Prompt Template\n```\n<role>You are a senior AI engineer.</role>\n<task>Analyze the following code for performance issues.</task>\n<format>Return a JSON with {issue, severity, suggestion}.</format>\n<code>{user_code}</code>\n```\n\n## Anti-patterns\n- Overly long prompts (token waste)\n- Contradictory instructions\n- Requiring complex formats without examples'
WHERE id = 'prompt-engineering';

-- Agent Architectures
UPDATE kaas.concept SET
  summary = 'Design patterns for LLM-based autonomous agents. Implements tool use, planning, and self-correction via ReAct, Plan-and-Execute, and Reflection.',
  content_md = E'# Agent Architectures\n\n## Main Patterns\n1. **ReAct**: interleave Reasoning + Acting. reason → act → observe → repeat\n2. **Plan-and-Execute**: plan first, then execute step-by-step\n3. **Reflection**: self-correcting loop that evaluates and improves its own output\n4. **Tool-calling**: pattern for invoking external tools (APIs, DBs, code execution)\n\n## ReAct Example\n```\nThought: I need to find the population of Tokyo.\nAction: search("Tokyo population 2024")\nObservation: Tokyo has 13.96 million people.\nThought: I now have the answer.\nAnswer: Tokyo''s population is approximately 13.96 million.\n```\n\n## Framework Comparison\n| Framework | Pattern | Strength |\n|---|---|---|\n| LangChain | Tool-calling | Most general-purpose |\n| LangGraph | State machine | Complex branching |\n| CrewAI | Role-based | Multi-agent |\n| AutoGen | Conversational | Code generation |'
WHERE id = 'agent-architectures';

-- Semantic Search
UPDATE kaas.concept SET
  summary = 'Document search based on meaning rather than keyword matching. Measures relevance via cosine similarity in embedding space.',
  content_md = E'# Semantic Search\n\n## Overview\nSearches documents by meaning (semantic) rather than keyword matching (BM25).\n\n## BM25 vs Dense Retrieval\n| Method | Principle | Pros | Cons |\n|---|---|---|---|\n| BM25 | Keyword frequency | Fast, precise keyword matching | Misses synonyms |\n| Dense | Embedding similarity | Semantic understanding | Slow, infra required |\n| Hybrid | Combine both | Best performance | Higher complexity |\n\n## Reranking\nStage-1 retrieval (recall-focused) → Stage-2 reranking (precision-focused)\n- Cohere Rerank, ColBERT\n- Balances accuracy and cost\n\n## DPR (Dense Passage Retrieval)\n- +9% recall over BM25 on open-domain QA\n- Dual encoder trained on question-passage pairs'
WHERE id = 'semantic-search';


-- ============================================
-- kaas.evidence — summary + comment
-- ============================================

-- RAG
UPDATE kaas.evidence SET
  summary = 'Retrieval-first mental model. Precision@k is the key metric. Chunking strategy matters more than model choice.',
  comment = 'Most accessible RAG primer. Must-read chunking section for practical use.'
WHERE id = 'rag-ev-001';

UPDATE kaas.evidence SET
  summary = 'Naive RAG reaches only ~60% retrieval accuracy. Hybrid + rerank brings it to 85%+.',
  comment = 'Essential for understanding the production gap. Numbers-driven comparison is persuasive.'
WHERE id = 'rag-ev-002';

UPDATE kaas.evidence SET
  summary = 'Adding a context prefix to each chunk reduces retrieval failures by 67%.',
  comment = 'SOTA technique as of 2026. Low implementation cost, high impact.'
WHERE id = 'rag-ev-003';

-- Chain-of-Thought
UPDATE kaas.evidence SET
  summary = 'Few-shot CoT improves GSM8K accuracy by +20% over baseline.',
  comment = 'The foundational CoT paper. Required reading.'
WHERE id = 'cot-ev-001';

UPDATE kaas.evidence SET
  summary = 'A single line "Let''s think step by step" dramatically improves zero-shot reasoning.',
  comment = 'Simplest CoT technique that applies immediately in practice.'
WHERE id = 'cot-ev-002';

-- Embeddings
UPDATE kaas.evidence SET
  summary = 'text-embedding-3-large: 3072 dimensions with Matryoshka dimension reduction.',
  comment = 'First reference when choosing embedding models.'
WHERE id = 'emb-ev-001';

UPDATE kaas.evidence SET
  summary = 'HNSW index offers the most general-purpose recall-latency tradeoff.',
  comment = 'Recommended for vector DB beginners.'
WHERE id = 'emb-ev-002';

UPDATE kaas.evidence SET
  summary = 'Combining BM25 + vector search captures both keyword and semantic benefits.',
  comment = 'Must-read when implementing hybrid search.'
WHERE id = 'emb-ev-003';

-- Fine-tuning
UPDATE kaas.evidence SET
  summary = 'Trains only 0.1% of parameters while matching full fine-tuning performance.',
  comment = 'The starting point for PEFT.'
WHERE id = 'ft-ev-001';

UPDATE kaas.evidence SET
  summary = '4-bit quantization + LoRA enables training 65B models on a single GPU.',
  comment = 'Essential technique in GPU-constrained environments.'
WHERE id = 'ft-ev-002';

-- Multi-Agent
UPDATE kaas.evidence SET
  summary = 'Multi-agent outperforms single-agent by +15% on code generation.',
  comment = 'Best entry point to multi-agent systems.'
WHERE id = 'ma-ev-001';

UPDATE kaas.evidence SET
  summary = 'Role-based orchestration allows defining workflows in natural language.',
  comment = 'Practical orchestration pattern for real-world use.'
WHERE id = 'ma-ev-002';

-- Evaluation
UPDATE kaas.evidence SET
  summary = 'GPT-4 judgments match human evaluation 80%+ of the time.',
  comment = 'Practical method for automating LLM evaluation.'
WHERE id = 'eval-ev-001';

UPDATE kaas.evidence SET
  summary = 'Multi-dimensional evaluation is more reliable than single benchmarks.',
  comment = 'Reference for designing evaluation frameworks.'
WHERE id = 'eval-ev-002';

-- Prompt Engineering
UPDATE kaas.evidence SET
  summary = 'Specific instructions and step-by-step decomposition determine ~80% of quality.',
  comment = 'Must-read for prompt engineering fundamentals.'
WHERE id = 'pe-ev-001';

UPDATE kaas.evidence SET
  summary = 'XML tags and role assignment improve consistency by ~40%.',
  comment = 'Claude-focused but broadly useful.'
WHERE id = 'pe-ev-002';

-- Agent Architectures
UPDATE kaas.evidence SET
  summary = 'Interleaved reasoning + acting achieves +6% accuracy on HotpotQA.',
  comment = 'Foundational paper for agent architectures.'
WHERE id = 'aa-ev-001';

UPDATE kaas.evidence SET
  summary = 'Tool-calling is the most common agent pattern in production.',
  comment = 'Reference when implementing production agents.'
WHERE id = 'aa-ev-002';

-- Semantic Search
UPDATE kaas.evidence SET
  summary = 'Dense retrieval improves recall by +9% over BM25 on open-domain QA.',
  comment = 'The starting point for dense retrieval.'
WHERE id = 'ss-ev-001';

UPDATE kaas.evidence SET
  summary = 'A two-stage pipeline balances accuracy and cost.',
  comment = 'Quantifies the benefit of introducing reranking.'
WHERE id = 'ss-ev-002';


-- ============================================
-- Verification query (commented out — uncomment to run)
-- ============================================
-- SELECT id, LEFT(summary, 80) AS summary_preview, LENGTH(content_md) AS content_len
-- FROM kaas.concept ORDER BY id;
-- SELECT id, concept_id, LEFT(summary, 60) AS summary, LEFT(comment, 40) AS comment
-- FROM kaas.evidence ORDER BY concept_id, id;

COMMIT;
