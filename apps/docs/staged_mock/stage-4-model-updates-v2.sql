-- ============================================================
-- Stage 4 Model Updates v2 — 50 agent_json_raw UPDATE
-- seq 701 ~ 750 / article_raw ID: 0195f300-d{seq:03d}-7000-8000-000000000001
-- user_id: SYSTEM_USER_ID = 00000000-0000-0000-0000-000000000000
-- agent_json_raw: v0.3 format (representative_entity nested object)
-- ai_status: stays PENDING → parse-agent-json API 호출 후 SUCCESS
--
-- Page: MODEL_UPDATES (no side_category for this page)
--
-- Prerequisites:
--   stage-1-model-updates-v2.sql 적용
--   + ingest-bulk API
--   + pregen-ai-state API
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

    -- =================== GPT-5.4 (701-708) — entity 001 ===================
    (701, '0195f300-1001-7000-b000-000000000001', 'MODEL_UPDATES', 5, 'GPT-5.4 expands its context window to 1 million tokens, enabling whole-codebase and book-length document workflows in a single API call.'),
    (702, '0195f300-1001-7000-b000-000000000001', 'MODEL_UPDATES', 4, 'GPT-5.4 Realtime voice API cuts round-trip latency to 280ms, unlocking near-natural conversational voice agents.'),
    (703, '0195f300-1001-7000-b000-000000000001', 'MODEL_UPDATES', 5, 'OpenAI cuts GPT-5.4 output token pricing by 40% across all API tiers, materially shifting cost economics for production GenAI apps.'),
    (704, '0195f300-1001-7000-b000-000000000001', 'MODEL_UPDATES', 4, 'GPT-5.4 reasoning mode adds a configurable thinking budget parameter, letting developers trade latency for answer quality per request.'),
    (705, '0195f300-1001-7000-b000-000000000001', 'MODEL_UPDATES', 5, 'GPT-5.4 Computer Use API reaches GA for enterprise customers, productizing agentic browser and desktop automation at scale.'),
    (706, '0195f300-1001-7000-b000-000000000001', 'MODEL_UPDATES', 4, 'GPT-5.4 adds native PDF and image processing in a single API call, removing the need for client-side preprocessing pipelines.'),
    (707, '0195f300-1001-7000-b000-000000000001', 'MODEL_UPDATES', 4, 'GPT-5.4 Predicted Outputs feature cuts code edit latency by 5x by speculatively decoding from a hint of the expected response.'),
    (708, '0195f300-1001-7000-b000-000000000001', 'MODEL_UPDATES', 4, 'GPT-5.4 Structured Outputs now guarantee 100% JSON Schema conformance via constrained decoding at the sampler.'),

    -- =================== Claude 3.7 Sonnet (709-716) — entity 002 ===================
    (709, '0195f300-1001-7000-b000-000000000002', 'MODEL_UPDATES', 5, 'Claude 3.7 Sonnet adds Extended Thinking mode for visible step-by-step reasoning on hard math, coding, and analytical tasks.'),
    (710, '0195f300-1001-7000-b000-000000000002', 'MODEL_UPDATES', 5, 'Claude 3.7 Sonnet Computer Use tool reaches GA with a 25% higher action accuracy than the prior preview release.'),
    (711, '0195f300-1001-7000-b000-000000000002', 'MODEL_UPDATES', 4, 'Claude 3.7 Sonnet Citations feature returns verifiable source spans by default, raising trust for retrieval-augmented workflows.'),
    (712, '0195f300-1001-7000-b000-000000000002', 'MODEL_UPDATES', 5, 'Claude 3.7 Sonnet tops the SWE-bench Verified leaderboard at 78% solve rate on real-world GitHub issues.'),
    (713, '0195f300-1001-7000-b000-000000000002', 'MODEL_UPDATES', 4, 'Claude 3.7 Sonnet adds a Files API for persistent document workflows, enabling cross-session document context without re-uploading.'),
    (714, '0195f300-1001-7000-b000-000000000002', 'MODEL_UPDATES', 4, 'Anthropic cuts Claude 3.7 Sonnet input token pricing by 30% via a new batched inference tier for non-realtime workloads.'),
    (715, '0195f300-1001-7000-b000-000000000002', 'MODEL_UPDATES', 4, 'Claude 3.7 Sonnet adds a native text editor tool for code modification workflows that integrates cleanly with agentic coding loops.'),
    (716, '0195f300-1001-7000-b000-000000000002', 'MODEL_UPDATES', 4, 'Claude 3.7 Sonnet vision API now processes up to 100 images per request, expanding multimodal use cases for document analysis.'),

    -- =================== Gemini 2.0 Flash (717-723) — entity 003 ===================
    (717, '0195f300-1001-7000-b000-000000000003', 'MODEL_UPDATES', 5, 'Gemini 2.0 Flash adds the native Multimodal Live API for real-time conversational experiences with low-latency audio and video.'),
    (718, '0195f300-1001-7000-b000-000000000003', 'MODEL_UPDATES', 4, 'Gemini 2.0 Flash tool use mode adds a native code execution sandbox, enabling on-server Python evaluation during model calls.'),
    (719, '0195f300-1001-7000-b000-000000000003', 'MODEL_UPDATES', 5, 'Google DeepMind releases the Gemini 2.0 Flash Thinking variant tuned for chain-of-thought reasoning at low cost.'),
    (720, '0195f300-1001-7000-b000-000000000003', 'MODEL_UPDATES', 5, 'Gemini 2.0 Flash context caching cuts repeated prompt cost by 75%, materially improving economics for RAG and long-context workloads.'),
    (721, '0195f300-1001-7000-b000-000000000003', 'MODEL_UPDATES', 4, 'Gemini 2.0 Flash is now available on Vertex AI with enterprise compliance controls, unlocking regulated-industry deployments.'),
    (722, '0195f300-1001-7000-b000-000000000003', 'MODEL_UPDATES', 4, 'Gemini 2.0 Flash adds native audio output for voice agent applications without an external TTS pipeline.'),
    (723, '0195f300-1001-7000-b000-000000000003', 'MODEL_UPDATES', 4, 'Gemini 2.0 Flash image generation API reaches general availability, integrating natively with the chat completions endpoint.'),

    -- =================== Grok-3 (724-730) — entity 004 ===================
    (724, '0195f300-1001-7000-b000-000000000004', 'MODEL_UPDATES', 4, 'Grok-3 API ships a real-time X platform search tool integration, giving agents access to live social conversation context.'),
    (725, '0195f300-1001-7000-b000-000000000004', 'MODEL_UPDATES', 5, 'Grok-3 tops the MMLU-Pro leaderboard among frontier closed-source models, narrowing the gap to GPT-5.4.'),
    (726, '0195f300-1001-7000-b000-000000000004', 'MODEL_UPDATES', 4, 'Grok-3 reasoning mode beats competitors on AIME and HMMT math contests, signaling strong olympiad-level math reasoning.'),
    (727, '0195f300-1001-7000-b000-000000000004', 'MODEL_UPDATES', 4, 'Grok-3 DeepSearch agent lands for multi-step web research with citations, competing directly with OpenAI Deep Research.'),
    (728, '0195f300-1001-7000-b000-000000000004', 'MODEL_UPDATES', 4, 'Grok-3 voice mode lands on iOS and Android with sub-second response latency for natural conversational voice flows.'),
    (729, '0195f300-1001-7000-b000-000000000004', 'MODEL_UPDATES', 3, 'Grok-3 adds image generation via the Aurora diffusion backend, unifying text and image output behind one API.'),
    (730, '0195f300-1001-7000-b000-000000000004', 'MODEL_UPDATES', 4, 'xAI releases a Grok-3 Mini variant targeted at cost-sensitive workloads at one tenth the price of the flagship model.'),

    -- =================== LLaMA 4 (731-737) — entity 005 ===================
    (731, '0195f300-1001-7000-b000-000000000005', 'MODEL_UPDATES', 5, 'Meta releases LLaMA 4 Maverick variant under a custom community license, opening enterprise-grade open weights for local deployment.'),
    (732, '0195f300-1001-7000-b000-000000000005', 'MODEL_UPDATES', 5, 'LLaMA 4 Behemoth preview lands as Meta largest foundation model to date, pushing the open-weight frontier forward.'),
    (733, '0195f300-1001-7000-b000-000000000005', 'MODEL_UPDATES', 5, 'LLaMA 4 Scout variant hits a 10 million token context window via native long-attention architecture, leading the open-weight pack.'),
    (734, '0195f300-1001-7000-b000-000000000005', 'MODEL_UPDATES', 4, 'LLaMA 4 multimodal variant adds native image and video understanding, removing the need for separate vision encoders.'),
    (735, '0195f300-1001-7000-b000-000000000005', 'MODEL_UPDATES', 4, 'LLaMA 4 Instruct variant tops the Open LLM Leaderboard on multilingual reasoning across 26 languages.'),
    (736, '0195f300-1001-7000-b000-000000000005', 'MODEL_UPDATES', 4, 'LLaMA 4 Code variant adds repository-level reasoning for whole-codebase tasks, narrowing the gap to closed coding models.'),
    (737, '0195f300-1001-7000-b000-000000000005', 'MODEL_UPDATES', 4, 'LLaMA 4 hits 1 billion cumulative downloads across Hugging Face and direct mirrors, cementing its dominance among open weights.'),

    -- =================== DeepSeek-R1 (738-744) — entity 006 ===================
    (738, '0195f300-1001-7000-b000-000000000006', 'MODEL_UPDATES', 5, 'DeepSeek-R1 adds distilled 1.5B and 7B reasoning models for edge deployment, bringing chain-of-thought to consumer hardware.'),
    (739, '0195f300-1001-7000-b000-000000000006', 'MODEL_UPDATES', 5, 'DeepSeek-R1 paper documents the GRPO training recipe for reasoning capability, providing a reproducible RL alignment approach.'),
    (740, '0195f300-1001-7000-b000-000000000006', 'MODEL_UPDATES', 4, 'DeepSeek-R1 updates its activation threshold for lower inference cost at the same quality, improving production economics.'),
    (741, '0195f300-1001-7000-b000-000000000006', 'MODEL_UPDATES', 5, 'DeepSeek-R1 API cuts output pricing to one twentieth of GPT-5.4 pricing, redrawing the cost frontier for reasoning workloads.'),
    (742, '0195f300-1001-7000-b000-000000000006', 'MODEL_UPDATES', 4, 'DeepSeek-R1 Vision variant adds native multimodal reasoning to the open lineage, expanding beyond text-only frontiers.'),
    (743, '0195f300-1001-7000-b000-000000000006', 'MODEL_UPDATES', 4, 'DeepSeek-R1 tops the AIDER code editing benchmark among open-weight models, validating its real-world coding utility.'),
    (744, '0195f300-1001-7000-b000-000000000006', 'MODEL_UPDATES', 4, 'DeepSeek-R1 reaches 500 million cumulative API tokens served across providers, signaling broad production adoption.'),

    -- =================== Mistral Large 2 (745-750) — entity 007 ===================
    (745, '0195f300-1001-7000-b000-000000000007', 'MODEL_UPDATES', 4, 'Mistral Large 2 adds function calling mode with parallel tool execution, supporting concurrent multi-tool agents in a single step.'),
    (746, '0195f300-1001-7000-b000-000000000007', 'MODEL_UPDATES', 4, 'Mistral Large 2 Code variant lands under Apache 2.0 license for enterprise use, removing license friction for commercial coding stacks.'),
    (747, '0195f300-1001-7000-b000-000000000007', 'MODEL_UPDATES', 4, 'Mistral cuts Large 2 API pricing by 50% to compete with GPT and Claude on cost across enterprise workloads.'),
    (748, '0195f300-1001-7000-b000-000000000007', 'MODEL_UPDATES', 4, 'Mistral Large 2 Multilingual variant adds native Korean and Japanese reasoning, expanding APAC coverage substantially.'),
    (749, '0195f300-1001-7000-b000-000000000007', 'MODEL_UPDATES', 4, 'Mistral Large 2 adds JSON Schema validation for guaranteed structured outputs, matching the constrained decoding feature in rival APIs.'),
    (750, '0195f300-1001-7000-b000-000000000007', 'MODEL_UPDATES', 4, 'Mistral Large 2 releases a distilled Mini variant for on-device deployment, targeting privacy-first mobile and edge workloads.')
    ) AS t(seq, entity_id, page, score, summary)
) LOOP
    i := i + 1;

    -- article_raw id (d prefix for seq 701-750)
    v_art_id := format('0195f300-d%s-7000-8000-000000000001', lpad(rec.seq::text, 3, '0'))::UUID;

    -- published_at from article_raw
    SELECT published_at INTO v_pub_at
    FROM content.article_raw
    WHERE id = v_art_id;

    IF v_pub_at IS NULL THEN
        RAISE NOTICE 'Skipping seq %: article_raw not found', rec.seq;
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
        RAISE NOTICE 'Skipping seq %: user_article_state not found (run ingest-bulk first)', rec.seq;
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
        RAISE NOTICE 'Skipping seq %: PENDING ai_state not found (run pregen-ai-state first)', rec.seq;
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
            'side_category_code', NULL,  -- MODEL_UPDATES has no side_category
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
