-- ============================================================
-- Migration: kaas.concept에 세일 여부 컬럼 추가
-- 목적: 큐레이터가 직접 세일 설정 가능
-- ============================================================

ALTER TABLE kaas.concept
  ADD COLUMN IF NOT EXISTS is_on_sale BOOLEAN DEFAULT false;
