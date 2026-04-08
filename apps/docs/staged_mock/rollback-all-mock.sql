-- ============================================================
-- Rollback All Mock Data + Reset Stats
-- Target:
--   - article_raw seeded by staged_mock (a001~a150, b201~b250, c301~c500)
--   - dependent user_article_state / user_article_ai_state rows
--   - snapshot stats tables
-- ============================================================

BEGIN;

DO $$
DECLARE
    v_ids UUID[] := ARRAY[]::UUID[];
    i INT;
BEGIN
    -- stage-1-article-raw + stage-1-model-updates-extra
    FOR i IN 1..150 LOOP
        v_ids := v_ids || format('0195f300-a%s-7000-8000-000000000001', lpad(i::text, 3, '0'))::UUID;
    END LOOP;

    -- stage-1-frameworks-extra
    FOR i IN 201..250 LOOP
        v_ids := v_ids || format('0195f300-b%s-7000-8000-000000000001', lpad(i::text, 3, '0'))::UUID;
    END LOOP;

    -- stage-1-extra-new-200
    FOR i IN 301..500 LOOP
        v_ids := v_ids || format('0195f300-c%s-7000-8000-000000000001', lpad(i::text, 3, '0'))::UUID;
    END LOOP;

    -- Delete in dependency order: ai_state -> uas -> article_raw
    DELETE FROM content.user_article_ai_state
    WHERE user_article_state_id IN (
        SELECT id FROM content.user_article_state WHERE article_raw_id = ANY(v_ids)
    );
    RAISE NOTICE 'Deleted user_article_ai_state rows for mock article IDs';

    DELETE FROM content.user_article_state
    WHERE article_raw_id = ANY(v_ids);
    RAISE NOTICE 'Deleted user_article_state rows for mock article IDs';

    DELETE FROM content.article_raw
    WHERE id = ANY(v_ids);
    RAISE NOTICE 'Deleted article_raw rows for mock IDs';
END $$;

-- Reset weekly snapshots used by landing/model/framework stats
DELETE FROM snapshot.platform_weekly_stat;
DELETE FROM snapshot.model_updates_weekly_rank;
DELETE FROM snapshot.frameworks_weekly_rank;

COMMIT;
