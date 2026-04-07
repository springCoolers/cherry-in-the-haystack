import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';

import { ArticleIngestionService } from 'src/modules/pipeline/article-ingestion.service';

@Injectable()
export class IngestionScheduleService {
  private readonly logger = new Logger(IngestionScheduleService.name);

  constructor(private readonly ingestionService: ArticleIngestionService) {}

  @Cron(CronExpression.EVERY_10_MINUTES)
  async runIngestion(): Promise<void> {
    this.logger.log('Scheduled ingestion started');
    const result = await this.ingestionService.processAllUnprocessed();
    this.logger.log(`Scheduled ingestion done — created: ${result.created}`);
  }
}
