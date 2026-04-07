import { Module } from '@nestjs/common';

import { DatabaseModule } from 'src/common/basic-module/database.module';
import { PipelineController } from './pipeline.controller';
import { ArticleIngestionService } from './article-ingestion.service';
import { AiStatePreGenService } from './ai-state-pregen.service';

@Module({
  imports: [DatabaseModule],
  controllers: [PipelineController],
  providers: [ArticleIngestionService, AiStatePreGenService],
  exports: [ArticleIngestionService, AiStatePreGenService],
})
export class PipelineModule {}
