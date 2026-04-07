import { Inject, Injectable, Logger, NotFoundException } from '@nestjs/common';
import { Knex } from 'knex';
import { v7 as uuidv7 } from 'uuid';

import type { ArticleRawEntity } from './entity/article-raw.entity';

export const SYSTEM_USER_ID = '00000000-0000-0000-0000-000000000000';

@Injectable()
export class ArticleIngestionService {
  private readonly logger = new Logger(ArticleIngestionService.name);

  constructor(
    @Inject('KNEX_CONNECTION')
    private readonly knex: Knex,
  ) {}

  /**
   * article_raw 1건에 대해 시스템 유저(공통) user_article_state를 생성한다.
   * 이미 존재하면 스킵한다.
   *
   * @returns 생성됐으면 true, 이미 존재해서 스킵됐으면 false
   */
  async processNewArticle(articleRawId: string): Promise<boolean> {
    const article = await this.knex<ArticleRawEntity>('content.article_raw')
      .where({ id: articleRawId })
      .first();

    if (!article) {
      throw new NotFoundException(`article_raw not found: ${articleRawId}`);
    }

    const existing = await this.knex('content.user_article_state')
      .where({ user_id: SYSTEM_USER_ID, article_raw_id: articleRawId })
      .whereNull('revoked_at')
      .first('id');

    if (existing) {
      this.logger.log(`Already exists — skipped for system / article ${articleRawId}`);
      return false;
    }

    const discoveredAt = this.resolveDiscoveredAt(article.published_at);
    const now = new Date();

    await this.knex('content.user_article_state').insert({
      id: uuidv7(),
      user_id: SYSTEM_USER_ID,
      article_raw_id: articleRawId,
      discovered_at: discoveredAt,
      representative_entity_id: null,
      side_category_id: null,
      impact_score: 0,
      is_high_impact: false,
      is_hidden: false,
      meta_json: null,
      created_at: now,
      updated_at: now,
    });

    this.logger.log(`Created system user_article_state for article ${articleRawId}`);
    return true;
  }

  /**
   * user_article_state가 없는 article_raw 전체를 INSERT...SELECT 단일 쿼리로 처리한다.
   * Node.js 메모리를 사용하지 않고 DB 내부에서 완결된다.
   *
   * @returns 생성된 건수
   */
  async processAllUnprocessed(): Promise<{ created: number }> {
    const result = await this.knex.raw<{ rowCount: number }>(`
      INSERT INTO content.user_article_state
        (id, user_id, article_raw_id, discovered_at,
         representative_entity_id, side_category_id,
         impact_score, is_high_impact, is_hidden, meta_json,
         created_at, updated_at)
      SELECT
        gen_random_uuid(),
        :systemUserId::UUID,
        ar.id,
        COALESCE(ar.published_at, NOW()) + INTERVAL '1 hour',
        NULL, NULL, 0, FALSE, FALSE, NULL,
        NOW(), NOW()
      FROM content.article_raw ar
      WHERE ar.storage_state = 'ACTIVE'
        AND NOT EXISTS (
          SELECT 1 FROM content.user_article_state uas
          WHERE uas.article_raw_id = ar.id
            AND uas.user_id = :systemUserId::UUID
            AND uas.revoked_at IS NULL
        )
    `, { systemUserId: SYSTEM_USER_ID });

    const created = result.rowCount ?? 0;
    this.logger.log(`processAllUnprocessed done — created: ${created}`);
    return { created };
  }

  private resolveDiscoveredAt(publishedAt: Date | null): Date {
    if (!publishedAt) return new Date();
    const t = new Date(publishedAt);
    t.setTime(t.getTime() + 60 * 60 * 1000); // +1h
    return t;
  }
}
