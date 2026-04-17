-- ============================================================
-- snapshot.platform_weekly_stat — week_start='2026-04-08' row 강제 재집계
-- 이유: 해당 row가 데이타 가공 전(SUCCESS=4건일 때) 빌드되어 stale
-- 효과: treemap_distribution_json + items_this_week + topics_covered_count 갱신
-- ============================================================
BEGIN;

WITH agg AS (
  SELECT
    aai.representative_entity_page::TEXT AS page,
    COUNT(DISTINCT uas.article_raw_id) AS article_count
  FROM content.user_article_ai_state aai
  JOIN content.user_article_state uas ON uas.id = aai.user_article_state_id
  JOIN content.article_raw ar ON ar.id = uas.article_raw_id
  WHERE aai.ai_status = 'SUCCESS'
    AND ar.published_at >= '2026-04-08'::DATE
    AND ar.published_at <  '2026-04-14'::DATE + INTERVAL '1 day'
  GROUP BY aai.representative_entity_page
), totals AS (
  SELECT SUM(article_count)::INT AS total, COUNT(*)::INT AS topics FROM agg
), treemap AS (
  SELECT jsonb_agg(
    jsonb_build_object(
      'page',          a.page,
      'article_count', a.article_count,
      'percent',       ROUND((a.article_count::NUMERIC / NULLIF(t.total, 0)) * 100, 1)
    ) ORDER BY a.article_count DESC
  ) AS j
  FROM agg a CROSS JOIN totals t
)
UPDATE snapshot.platform_weekly_stat AS s
SET
  items_this_week           = t.total,
  topics_covered_count      = t.topics,
  treemap_distribution_json = tm.j,
  updated_at                = NOW()
FROM totals t, treemap tm
WHERE s.week_start = '2026-04-08';

COMMIT;
