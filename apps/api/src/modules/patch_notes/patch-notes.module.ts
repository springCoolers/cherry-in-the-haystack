import { Module } from '@nestjs/common';
import { DatabaseModule } from 'src/common/basic-module/database.module';
import { PatchNotesController } from './patch-notes.controller';
import { PatchNotesService } from './patch-notes.service';
import { CaseStudiesService } from './case-studies.service';

@Module({
  imports: [DatabaseModule],
  controllers: [PatchNotesController],
  providers: [PatchNotesService, CaseStudiesService],
  exports: [PatchNotesService, CaseStudiesService],
})
export class PatchNotesModule {}
