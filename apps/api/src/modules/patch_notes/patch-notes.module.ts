import { Module } from '@nestjs/common';
import { DatabaseModule } from 'src/common/basic-module/database.module';
import { PatchNotesController } from './patch-notes.controller';
import { PatchNotesService } from './patch-notes.service';

@Module({
  imports: [DatabaseModule],
  controllers: [PatchNotesController],
  providers: [PatchNotesService],
  exports: [PatchNotesService],
})
export class PatchNotesModule {}
