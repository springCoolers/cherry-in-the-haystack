-- ============================================================
-- Migration: core.app_user에 카르마 + 지갑 컬럼 추가
-- 목적: 유저가 올린 컨셉(상품)에 작성자 카르마 표시
-- 경로: concept.created_by → app_user.id → karma_tier 조회
-- ============================================================

-- 1. 지갑 주소 (온체인 카르마 조회용)
ALTER TABLE core.app_user
  ADD COLUMN IF NOT EXISTS wallet_address VARCHAR(42);

-- 2. 카르마 티어 (Bronze / Silver / Gold / Platinum)
ALTER TABLE core.app_user
  ADD COLUMN IF NOT EXISTS karma_tier VARCHAR(20) DEFAULT 'Bronze';

-- 3. 카르마 잔액 (온체인 캐싱)
ALTER TABLE core.app_user
  ADD COLUMN IF NOT EXISTS karma_balance INTEGER DEFAULT 0;

-- 시스템 유저에 기본값 설정
UPDATE core.app_user
  SET karma_tier = 'Gold', karma_balance = 500
  WHERE id = '00000000-0000-0000-0000-000000000000';
