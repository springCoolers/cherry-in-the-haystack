-- ============================================================
-- 기존 SALE 상품 DB 반영
-- 규칙: 각 카테고리에서 quality_score 최고인 컨셉 1개씩
-- is_on_sale=true, sale_discount=20 (기존 하드코딩 20%)
-- ============================================================

UPDATE kaas.concept SET is_on_sale = false, sale_discount = 20;

UPDATE kaas.concept c
SET is_on_sale = true
FROM (
  SELECT DISTINCT ON (category) id
  FROM kaas.concept
  WHERE is_active = true
  ORDER BY category, quality_score DESC
) top
WHERE c.id = top.id;
