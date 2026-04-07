import { Body, Controller, HttpCode, Post } from '@nestjs/common';
import { ApiBody, ApiOperation, ApiTags } from '@nestjs/swagger';

import { ZodValidationPipe } from 'src/middleware/zod-validation.pipe';
import { ArticleIngestionService } from './article-ingestion.service';
import { AiStatePreGenService } from './ai-state-pregen.service';
import { IngestDto } from './input-dto/ingest.dto';

@Controller('pipeline')
@ApiTags('Pipeline (System)')
export class PipelineController {
  constructor(
    private readonly ingestionService: ArticleIngestionService,
    private readonly aiStatePreGenService: AiStatePreGenService,
  ) {}

  @Post('ingest')
  @HttpCode(200)
  @ApiOperation({ summary: '[시스템] article_raw 1건 → 시스템 유저 user_article_state 생성' })
  @ApiBody({ type: IngestDto })
  async ingest(
    @Body(new ZodValidationPipe(IngestDto.schema)) dto: IngestDto,
  ): Promise<{ created: boolean }> {
    const created = await this.ingestionService.processNewArticle(dto.articleRawId);
    return { created };
  }

  @Post('ingest-bulk')
  @HttpCode(200)
  @ApiOperation({ summary: '[시스템] 미처리 article_raw 전체 → user_article_state 일괄 생성' })
  async ingestBulk(): Promise<{ created: number }> {
    return this.ingestionService.processAllUnprocessed();
  }

  @Post('pregen-ai-state')
  @HttpCode(200)
  @ApiOperation({ summary: '[시스템] ai_state 없는 user_article_state 전체 → PENDING ai_state 일괄 생성' })
  async pregenAiState(): Promise<{ created: number }> {
    return this.aiStatePreGenService.pregenAllPending();
  }
}
