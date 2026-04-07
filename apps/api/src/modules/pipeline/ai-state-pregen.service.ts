import { Inject, Injectable, Logger } from '@nestjs/common';
import { Knex } from 'knex';

import { SYSTEM_USER_ID } from './article-ingestion.service';

@Injectable()
export class AiStatePreGenService {
  private readonly logger = new Logger(AiStatePreGenService.name);

  constructor(
    @Inject('KNEX_CONNECTION')
    private readonly knex: Knex,
  ) {}

  /**
   * user_article_ai_state가 없는 user_article_state 전체에 대해
   * PENDING ai_state를 INSERT...SELECT 단일 쿼리로 생성한다.
   *
   * @returns 생성된 건수
   */
  async pregenAllPending(): Promise<{ created: number }> {
    const result = await this.knex.raw<{ rowCount: number }>(`
      INSERT INTO content.user_article_ai_state
        (id, user_id, user_article_state_id, ai_status)
      SELECT
        gen_random_uuid(),
        :systemUserId::UUID,
        uas.id,
        'PENDING'
      FROM content.user_article_state uas
      WHERE uas.user_id = :systemUserId::UUID
        AND uas.revoked_at IS NULL
        AND NOT EXISTS (
          SELECT 1 FROM content.user_article_ai_state aai
          WHERE aai.user_article_state_id = uas.id
        )
    `, { systemUserId: SYSTEM_USER_ID });

    const created = result.rowCount ?? 0;
    this.logger.log(`pregenAllPending done — created: ${created}`);
    return { created };
  }
}
