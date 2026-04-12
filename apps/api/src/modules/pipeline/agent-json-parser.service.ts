import { Inject, Injectable, Logger } from '@nestjs/common';
import { Knex } from 'knex';

import { SYSTEM_USER_ID } from './article-ingestion.service';

@Injectable()
export class AgentJsonParserService {
  private readonly logger = new Logger(AgentJsonParserService.name);

  constructor(
    @Inject('KNEX_CONNECTION')
    private readonly knex: Knex,
  ) {}

  /**
   * PENDING ai_state 중 agent_json_raw가 있는 행을 일괄 파싱한다.
   * 3개의 bulk SQL로 처리 — 루프 없음.
   *
   * 1. ai_state SUCCESS UPDATE (entity 검증 + 정규 컬럼 투영)
   * 2. ai_state FAILED UPDATE (검증 실패한 나머지)
   * 3. user_article_state UPDATE (representative_entity, impact_score, side_category)
   *
   * representative_entity 매칭 전략:
   *   A) agent_json_raw에 id가 있으면 → id로 직접 매칭 (기존 포맷)
   *   B) id가 없으면 → page + name으로 역조회 (새 포맷, ID-free)
   */
  async processPendingBatch(): Promise<{ success: number; failed: number }> {
    const successResult = await this.knex.raw<{ rowCount: number }>(`
      WITH pending AS (
        SELECT id, agent_json_raw
        FROM content.user_article_ai_state
        WHERE user_id = :systemUserId::UUID
          AND ai_status = 'PENDING'
          AND agent_json_raw IS NOT NULL
      ),
      -- representative_entity 매칭: id 우선, 없으면 page+name 역조회
      resolved AS (
        SELECT
          p.id,
          p.agent_json_raw,
          te.id   AS resolved_entity_id
        FROM pending p
        CROSS JOIN LATERAL (
          SELECT t.id
          FROM content.tracked_entity t
          WHERE
            CASE
              -- A) id가 있으면 id로 직접 매칭
              WHEN (p.agent_json_raw->'representative_entity'->>'id') IS NOT NULL
              THEN t.id = (p.agent_json_raw->'representative_entity'->>'id')::UUID

              -- B) id가 없으면 page + name으로 역조회
              ELSE lower(t.name) = lower(p.agent_json_raw->'representative_entity'->>'name')
               AND t.revoked_at IS NULL
               AND EXISTS (
                 SELECT 1 FROM content.tracked_entity_placement tep2
                 WHERE tep2.tracked_entity_id = t.id
                   AND tep2.entity_page = (p.agent_json_raw->'representative_entity'->>'page')::content.entity_page_enum
                   AND tep2.revoked_at IS NULL
                   AND tep2.is_active = TRUE
               )
            END
          LIMIT 1
        ) te
      )
      UPDATE content.user_article_ai_state aai
      SET
        representative_entity_id            = te.id,
        representative_entity_page          = tep.entity_page,
        representative_entity_category_id   = tep.entity_category_id,
        representative_entity_category_name = ec.name,
        representative_entity_name          = te.name,
        ai_summary                          = r.agent_json_raw->>'ai_summary',
        ai_score                            = (r.agent_json_raw->>'ai_score')::SMALLINT,
        ai_classification_json              = r.agent_json_raw->'ai_classification_json',
        ai_tags_json                        = r.agent_json_raw->'ai_tags_json',
        ai_snippets_json                    = r.agent_json_raw->'ai_snippets_json',
        ai_evidence_json                    = r.agent_json_raw->'ai_evidence_json',
        ai_structured_extraction_json       = r.agent_json_raw->'ai_structured_extraction_json',
        ai_status                           = 'SUCCESS'
      FROM resolved r
      JOIN content.tracked_entity te
        ON te.id = r.resolved_entity_id
      JOIN content.tracked_entity_placement tep
        ON tep.tracked_entity_id = te.id
       AND tep.entity_page = (r.agent_json_raw->'representative_entity'->>'page')::content.entity_page_enum
       AND tep.revoked_at IS NULL
       AND tep.is_active = TRUE
      JOIN content.entity_category ec
        ON ec.id = tep.entity_category_id
      WHERE aai.id = r.id
    `, { systemUserId: SYSTEM_USER_ID });

    const success = successResult.rowCount ?? 0;

    const failedResult = await this.knex.raw<{ rowCount: number }>(`
      UPDATE content.user_article_ai_state
      SET ai_status = 'FAILED'
      WHERE user_id = :systemUserId::UUID
        AND ai_status = 'PENDING'
        AND agent_json_raw IS NOT NULL
    `, { systemUserId: SYSTEM_USER_ID });

    const failed = failedResult.rowCount ?? 0;

    await this.knex.raw(`
      UPDATE content.user_article_state uas
      SET
        representative_entity_id = aai.representative_entity_id,
        side_category_id = sc.id,
        impact_score = CASE
          WHEN aai.ai_score = 5 THEN (80 + random() * 15)::NUMERIC
          WHEN aai.ai_score = 4 THEN (60 + random() * 20)::NUMERIC
          WHEN aai.ai_score = 3 THEN (40 + random() * 20)::NUMERIC
          ELSE                       (20 + random() * 20)::NUMERIC
        END,
        is_high_impact = COALESCE(aai.ai_score >= 4, FALSE),
        updated_at = NOW()
      FROM content.user_article_ai_state aai
      LEFT JOIN content.side_category sc
        ON sc.code = aai.agent_json_raw->>'side_category_code'
       AND sc.revoked_at IS NULL
      WHERE uas.id = aai.user_article_state_id
        AND aai.ai_status = 'SUCCESS'
        AND uas.user_id = :systemUserId::UUID
    `, { systemUserId: SYSTEM_USER_ID });

    this.logger.log(`processPendingBatch done — success: ${success}, failed: ${failed}`);
    return { success, failed };
  }
}
