import { Controller, Get, Patch, Param, HttpCode } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { PatchNotesService, PatchNotesResponse } from './patch-notes.service';

@Controller('patch-notes')
@ApiTags('Patch Notes')
export class PatchNotesController {
  constructor(private readonly patchNotesService: PatchNotesService) {}

  @Get()
  @ApiOperation({ summary: '최근 7일 패치노트 (팔로우 엔터티 기준)' })
  async getPatchNotes(): Promise<PatchNotesResponse> {
    return this.patchNotesService.getPatchNotes();
  }

  @Patch(':articleStateId/read')
  @HttpCode(204)
  @ApiOperation({ summary: '기사 읽음 처리' })
  async markAsRead(@Param('articleStateId') articleStateId: string): Promise<void> {
    return this.patchNotesService.markAsRead(articleStateId);
  }
}
