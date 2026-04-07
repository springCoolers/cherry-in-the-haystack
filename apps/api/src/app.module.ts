import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AppUserModule } from './modules/app_user/app-user.module';
import { PipelineModule } from './modules/pipeline/pipeline.module';
import { PipelineUserModule } from './modules/pipeline_user/pipeline-user.module';
import { AppScheduleModule } from './modules/schedule/schedule.module';

@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true }), AppUserModule, PipelineModule, PipelineUserModule, AppScheduleModule],
  controllers: [],
  providers: [],
})
export class AppModule {}
