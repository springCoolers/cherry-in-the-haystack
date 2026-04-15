-- ============================================
-- Cherry — Translate Korean prompt template data to English
-- Target: core.prompt_template + core.prompt_template_version
-- Usage: psql -f prompt-template-translate-to-english.sql
-- Idempotent: safe to re-run (UPDATE is by code/id)
-- ============================================

BEGIN;

-- ============================================
-- core.prompt_template — name, description, tone_text
-- ============================================

UPDATE core.prompt_template SET
  name = 'Default Article Analysis',
  description = 'Default template that generates article summary, score, classification, and tags',
  tone_text = 'Summarize in a technical and concise manner. The reader is an ML engineer. Score based on practical value.'
WHERE code = 'article_ai_default';

-- ============================================
-- core.prompt_template_version — change_note + few_shot_examples
-- few_shot_examples에 한글 요약이 포함되어 있음 → 영어로 교체
-- ============================================

-- Korean change_note 영문화 (A/B/C 버전 중 '새 버전' → 'New version')
UPDATE core.prompt_template_version SET
  change_note = 'New version'
WHERE change_note = '새 버전';

-- few_shot_examples 영문화 — 한글이 포함된 모든 버전에 동일한 영문 예시 적용
-- 'ai_summary' 안의 한국어를 영어로 교체
UPDATE core.prompt_template_version SET
  few_shot_examples = E'Example 1:\nInput: "GPT-4o achieves SOTA on MMLU with 88.7% accuracy..."\nOutput: {\n  "ai_summary": "OpenAI''s GPT-4o achieved state-of-the-art performance on the MMLU benchmark.",\n  "ai_score": 4,\n  "ai_classification_json": { "primary_category": "MODEL_UPDATES", "confidence": 0.95 },\n  "ai_tags_json": [{ "kind": "TAG", "value": "GPT-4o" }, { "kind": "TAG", "value": "MMLU" }]\n}'
WHERE prompt_template_id IN (SELECT id FROM core.prompt_template WHERE code = 'article_ai_default')
  AND few_shot_examples LIKE '%최고%성능%';

-- ============================================
-- prompt_text 안의 "1-2 sentence summary in Korean" → "in English"
-- (요약을 영어로 쓰도록 지시 변경)
-- ============================================

UPDATE core.prompt_template_version SET
  prompt_text = REPLACE(prompt_text, '1-2 sentence summary in Korean', '1-2 sentence summary in English')
WHERE prompt_template_id IN (SELECT id FROM core.prompt_template WHERE code = 'article_ai_default')
  AND prompt_text LIKE '%summary in Korean%';


-- ============================================
-- Verification (commented out — uncomment to inspect)
-- ============================================
-- SELECT code, name, LEFT(description, 80) AS description, LEFT(tone_text, 80) AS tone FROM core.prompt_template;
-- SELECT version_tag, change_note, LEFT(few_shot_examples, 120) AS few_shot_preview FROM core.prompt_template_version
-- WHERE prompt_template_id IN (SELECT id FROM core.prompt_template WHERE code = 'article_ai_default')
-- ORDER BY version_no;

COMMIT;
