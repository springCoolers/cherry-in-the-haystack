import { Inject, Injectable } from '@nestjs/common';
import { Knex } from 'knex';
import { SYSTEM_USER_ID } from '../pipeline/article-ingestion.service';

export interface CaseStudyItem {
  id: string;
  articleStateId: string;
  title: string;
  oneLiner: string;
  entityName: string;
  categoryName: string;
  categoryCode: string;
  sideCategory: string | null;       // 'Case Study' | 'Applied Research' | null
  sideCategoryCode: string | null;   // 'CASE_STUDY' | 'APPLIED_RESEARCH' | null
  score: number;
  date: string;
}

export interface CaseStudiesCategoryGroup {
  id: string;
  code: string;
  name: string;
  items: CaseStudyItem[];
}

export interface CaseStudiesResponse {
  groups: CaseStudiesCategoryGroup[];
  total: number;
  period: { from: string; to: string };
}

@Injectable()
export class CaseStudiesService {
  constructor(
    @Inject('KNEX_CONNECTION')
    private readonly knex: Knex,
  ) {}

  async getCaseStudies(): Promise<CaseStudiesResponse> {
    const rows = await this.knex.raw<{ rows: any[] }>(`
      SELECT
        ar.id                                        AS article_raw_id,
        uas.id                                       AS article_state_id,
        ar.title,
        ar.published_at,
        aai.ai_summary,
        aai.ai_score,
        aai.representative_entity_name               AS entity_name,
        ec.id                                        AS category_id,
        ec.code                                      AS category_code,
        ec.name                                      AS category_name,
        ec.sort_order                                AS sort_order,
        sc.code                                      AS side_cat_code,
        sc.name                                      AS side_cat_name
      FROM content.user_article_state uas
      JOIN content.article_raw ar
        ON ar.id = uas.article_raw_id
      JOIN content.user_article_ai_state aai
        ON aai.user_article_state_id = uas.id
       AND aai.ai_status = 'SUCCESS'
      JOIN personal.entity_follow ef
        ON ef.tracked_entity_id = aai.representative_entity_id
       AND ef.user_id = :systemUserId::UUID
       AND ef.is_following = TRUE
       AND ef.revoked_at IS NULL
      LEFT JOIN content.entity_category ec
        ON ec.id = aai.representative_entity_category_id
      LEFT JOIN content.side_category sc
        ON sc.id = uas.side_category_id
      WHERE uas.user_id = :systemUserId::UUID
        AND uas.revoked_at IS NULL
        AND aai.representative_entity_page = 'CASE_STUDIES'
      ORDER BY ec.sort_order ASC, ar.published_at DESC
    `, { systemUserId: SYSTEM_USER_ID });

    // 카테고리별로 그룹핑
    const groupMap = new Map<string, CaseStudiesCategoryGroup>();

    for (const r of rows.rows) {
      const catId = r.category_id ?? 'unknown';
      if (!groupMap.has(catId)) {
        groupMap.set(catId, {
          id: catId,
          code: r.category_code ?? '',
          name: r.category_name ?? 'Unknown',
          items: [],
        });
      }
      groupMap.get(catId)!.items.push({
        id: r.article_raw_id,
        articleStateId: r.article_state_id,
        title: r.title,
        oneLiner: r.ai_summary ?? '',
        entityName: r.entity_name ?? '',
        categoryName: r.category_name ?? '',
        categoryCode: r.category_code ?? '',
        sideCategory: r.side_cat_name ?? null,
        sideCategoryCode: r.side_cat_code ?? null,
        score: r.ai_score ?? 0,
        date: new Date(r.published_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      });
    }

    const groups = Array.from(groupMap.values());
    const total = rows.rows.length;

    const dates = rows.rows.map((r) => new Date(r.published_at).getTime()).filter(Boolean);
    const period = dates.length > 0
      ? {
          from: new Date(Math.min(...dates)).toISOString().slice(0, 10),
          to: new Date(Math.max(...dates)).toISOString().slice(0, 10),
        }
      : { from: '', to: '' };

    return { groups, total, period };
  }
}
