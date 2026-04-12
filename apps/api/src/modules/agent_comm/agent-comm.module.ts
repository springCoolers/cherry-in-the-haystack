import { Module } from '@nestjs/common';
import { DatabaseModule } from 'src/common/basic-module/database.module';
import { AgentCommController } from './agent-comm.controller';
import { AgentCommService } from './agent-comm.service';

@Module({
  imports: [DatabaseModule],
  controllers: [AgentCommController],
  providers: [AgentCommService],
})
export class AgentCommModule {}
