import { ApiProperty } from '@nestjs/swagger';
import { z } from 'zod';

const resultItemSchema = z.object({
  ai_state_id: z.string().uuid(),
  version_id: z.string().uuid(),
  result: z.record(z.unknown()),
});

export class FinishEvaluationDto {
  static schema = z.object({
    results: z.array(resultItemSchema).min(1),
  });

  @ApiProperty({
    description: '평가 결과 배열',
    example: [
      {
        ai_state_id: '00000000-0000-0000-0000-000000000001',
        version_id: '00000000-0000-0000-0000-000000000002',
        result: {
          representative_entity: {
            page: 'MODEL_UPDATES',
            category_name: 'OpenAI Family',
            name: 'GPT-4o',
          },
          ai_summary: 'GPT-4o achieves new SOTA on MMLU.',
          ai_score: 4,
          ai_classification_json: {
            final_path: {
              page: 'MODEL_UPDATES',
              category_name: 'OpenAI Family',
              entity_name: 'GPT-4o',
            },
          },
          side_category_code: null,
          ai_tags_json: [{ kind: 'TAG', value: 'GPT-4o' }],
          ai_snippets_json: { why_it_matters: 'New benchmark record.', key_points: [] },
          ai_evidence_json: { evidence_items: [] },
          ai_structured_extraction_json: { source: { name: 'Tech Blog', type: 'RSS' } },
        },
      },
    ],
  })
  results!: { ai_state_id: string; version_id: string; result: Record<string, unknown> }[];
}
