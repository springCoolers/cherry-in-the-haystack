import { Module } from '@nestjs/common';

import { DatabaseModule } from 'src/common/basic-module/database.module';
import { PipelineController } from './pipeline.controller';
import { ArticleIngestionService } from './article-ingestion.service';
import { AiStatePreGenService } from './ai-state-pregen.service';
import { AgentJsonParserService } from './agent-json-parser.service';

@Module({
  imports: [DatabaseModule],
  controllers: [PipelineController],
  providers: [ArticleIngestionService, AiStatePreGenService, AgentJsonParserService],
  exports: [ArticleIngestionService, AiStatePreGenService, AgentJsonParserService],
})
export class PipelineModule {}
