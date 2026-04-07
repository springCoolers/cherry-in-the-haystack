import { Controller, Get, Patch, Param, HttpCode } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { PatchNotesService, PatchNotesResponse } from './patch-notes.service';
import { CaseStudiesService, CaseStudiesResponse } from './case-studies.service';

@Controller('patch-notes')
@ApiTags('Patch Notes')
export class PatchNotesController {
  constructor(
    private readonly patchNotesService: PatchNotesService,
    private readonly caseStudiesService: CaseStudiesService,
  ) {}

  @Get()
  @ApiOperation({ summary: '최근 7일 패치노트 (팔로우 엔터티 기준)' })
  async getPatchNotes(): Promise<PatchNotesResponse> {
    return this.patchNotesService.getPatchNotes();
  }

  @Get('case-studies')
  @ApiOperation({ summary: 'CASE_STUDIES 전체 아티클 (카테고리 그룹, 사이드카테고리 태그)' })
  async getCaseStudies(): Promise<CaseStudiesResponse> {
    return this.caseStudiesService.getCaseStudies();
  }

  @Patch(':articleStateId/read')
  @HttpCode(204)
  @ApiOperation({ summary: '기사 읽음 처리' })
  async markAsRead(@Param('articleStateId') articleStateId: string): Promise<void> {
    return this.patchNotesService.markAsRead(articleStateId);
  }
}
