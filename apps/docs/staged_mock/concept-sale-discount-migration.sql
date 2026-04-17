-- ============================================================
-- Migration: kaas.concept에 세일 할인율 컬럼 추가
-- 범위: 0 ~ 100 (퍼센트). 예: 20 = 20% 할인
-- is_on_sale=true일 때만 적용
-- ============================================================

ALTER TABLE kaas.concept
  ADD COLUMN IF NOT EXISTS sale_discount INTEGER DEFAULT 20;
