-- Rollback: 잘못 넣은 200개 기사 삭제
-- article_raw ID 패턴: 0195f300-a{001~200}-7000-8000-000000000001

DO $$
DECLARE
    v_ids UUID[];
    i INT;
BEGIN
    -- 생성된 200개 article_raw ID 수집
    v_ids := ARRAY[]::UUID[];
    FOR i IN 1..200 LOOP
        v_ids := v_ids || format('0195f300-a%s-7000-8000-000000000001', lpad(i::text, 3, '0'))::UUID;
    END LOOP;

    -- 역순 삭제: ai_state -> uas -> article_raw
    DELETE FROM content.user_article_ai_state
    WHERE user_article_state_id IN (
        SELECT id FROM content.user_article_state WHERE article_raw_id = ANY(v_ids)
    );
    RAISE NOTICE 'Deleted user_article_ai_state rows';

    DELETE FROM content.user_article_state WHERE article_raw_id = ANY(v_ids);
    RAISE NOTICE 'Deleted user_article_state rows';

    DELETE FROM content.article_raw WHERE id = ANY(v_ids);
    RAISE NOTICE 'Deleted article_raw rows';
END $$;
