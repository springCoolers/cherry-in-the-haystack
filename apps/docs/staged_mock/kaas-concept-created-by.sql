-- kaas.concept에 created_by 컬럼 추가 + 기존 데이터 __SYSTEM__ 설정
-- 실행: DBeaver 또는 psql에서 실행

ALTER TABLE kaas.concept
  ADD COLUMN IF NOT EXISTS created_by VARCHAR(100) DEFAULT '__SYSTEM__';

-- 기존 9개 컨셉을 __SYSTEM__ 소유로 명시
UPDATE kaas.concept SET created_by = '__SYSTEM__' WHERE created_by IS NULL;

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_kaas_concept_created_by ON kaas.concept (created_by);
