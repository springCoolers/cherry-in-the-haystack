import { Body, Controller, Delete, Get, HttpCode, NotFoundException, Param, Patch, Post, Query } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { ZodValidationPipe } from 'src/middleware/zod-validation.pipe';
import { KaasKnowledgeService } from './kaas-knowledge.service';
import { CreateConceptDto, CreateConceptSchema } from './input-dto/create-concept.dto';
import { UpdateConceptDto, UpdateConceptSchema } from './input-dto/update-concept.dto';
import { CreateEvidenceDto, CreateEvidenceSchema } from './input-dto/create-evidence.dto';
import { UpdateEvidenceDto, UpdateEvidenceSchema } from './input-dto/update-evidence.dto';

@Controller('v1/kaas/admin')
@ApiTags('KaaS — Admin')
export class KaasAdminController {
  constructor(private readonly knowledge: KaasKnowledgeService) {}

  /* ───── Concept CRUD ───── */

  @Get('concepts')
  @ApiOperation({ summary: '큐레이션 개념 목록 (created_by 필터 지원)' })
  async listConcepts(@Query('created_by') createdBy?: string) {
    return this.knowledge.findAllAdmin(createdBy);
  }

  @Get('concepts/:id')
  @ApiOperation({ summary: 'Admin — 개념 상세 (content_md + evidence)' })
  async getConcept(@Param('id') id: string) {
    const concept = await this.knowledge.findByIdAdmin(id);
    if (!concept) throw new NotFoundException('Concept not found');
    return concept;
  }

  @Post('concepts')
  @HttpCode(201)
  @ApiOperation({ summary: 'Admin — 개념 생성' })
  async createConcept(
    @Body() dto: any,
  ) {
    return this.knowledge.createConcept(dto);
  }

  @Patch('concepts/:id')
  @ApiOperation({ summary: 'Admin — 개념 수정' })
  async updateConcept(
    @Param('id') id: string,
    @Body(new ZodValidationPipe(UpdateConceptSchema)) dto: UpdateConceptDto,
  ) {
    return this.knowledge.updateConcept(id, dto as Record<string, unknown>);
  }

  @Delete('concepts/:id')
  @HttpCode(204)
  @ApiOperation({ summary: 'Admin — 개념 소프트 삭제' })
  async deleteConcept(@Param('id') id: string) {
    await this.knowledge.softDeleteConcept(id);
  }

  /* ───── Evidence CRUD ───── */

  @Post('concepts/:conceptId/evidence')
  @HttpCode(201)
  @ApiOperation({ summary: 'Admin — Evidence 추가' })
  async addEvidence(
    @Param('conceptId') conceptId: string,
    @Body(new ZodValidationPipe(CreateEvidenceSchema)) dto: CreateEvidenceDto,
  ) {
    return this.knowledge.addEvidence(conceptId, dto);
  }

  @Patch('concepts/:conceptId/evidence/:evidenceId')
  @ApiOperation({ summary: 'Admin — Evidence 수정' })
  async updateEvidence(
    @Param('conceptId') conceptId: string,
    @Param('evidenceId') evidenceId: string,
    @Body(new ZodValidationPipe(UpdateEvidenceSchema)) dto: UpdateEvidenceDto,
  ) {
    return this.knowledge.updateEvidence(conceptId, evidenceId, dto as Record<string, unknown>);
  }

  @Delete('concepts/:conceptId/evidence/:evidenceId')
  @HttpCode(204)
  @ApiOperation({ summary: 'Admin — Evidence 삭제' })
  async deleteEvidence(
    @Param('conceptId') conceptId: string,
    @Param('evidenceId') evidenceId: string,
  ) {
    await this.knowledge.deleteEvidence(conceptId, evidenceId);
  }
}
