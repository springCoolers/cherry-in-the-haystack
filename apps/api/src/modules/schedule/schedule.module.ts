import { Module } from '@nestjs/common';
import { ScheduleModule } from '@nestjs/schedule';

import { PipelineModule } from 'src/modules/pipeline/pipeline.module';
import { IngestionScheduleService } from './ingestion-schedule.service';

@Module({
  imports: [ScheduleModule.forRoot(), PipelineModule],
  providers: [IngestionScheduleService],
})
export class AppScheduleModule {}
