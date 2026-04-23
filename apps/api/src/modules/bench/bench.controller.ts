import {
  Body,
  Controller,
  Get,
  HttpException,
  HttpStatus,
  Logger,
  Post,
} from '@nestjs/common'
import { ApiBody, ApiOperation, ApiTags } from '@nestjs/swagger'

import {
  BenchService,
  type BenchCompareResponse,
  type BenchRunResponse,
} from './bench.service'
import type { BenchSetSummary } from './sets/set-definitions'
import type { AgentBuildInput } from './cards/compose-runtime'

@Controller('v1/kaas/bench')
@ApiTags('KaaS — Bench (Workshop Before/After demo)')
export class BenchController {
  private readonly logger = new Logger(BenchController.name)

  constructor(private readonly bench: BenchService) {}

  @Get('sets')
  @ApiOperation({
    summary: 'List the 3 benchmark sets (UI chrome: id, name, task, skills).',
  })
  listSets(): BenchSetSummary[] {
    return this.bench.listSets()
  }

  @Post('compare')
  @ApiOperation({
    summary:
      'Run baseline + enhanced Claude calls for the given set, evaluate both, return metrics.',
  })
  @ApiBody({
    schema: {
      type: 'object',
      required: ['setId'],
      properties: {
        setId: {
          type: 'string',
          enum: ['set-1-oracle', 'set-2-hunter', 'set-3-policy'],
        },
      },
    },
  })
  async compare(
    @Body() body: { setId?: string },
  ): Promise<BenchCompareResponse> {
    const setId = body?.setId
    if (!setId || typeof setId !== 'string') {
      throw new HttpException(
        { statusCode: 400, code: 'BENCH_INVALID_SET', message: 'setId is required' },
        HttpStatus.BAD_REQUEST,
      )
    }
    try {
      return await this.bench.compare(setId)
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err)
      this.logger.error(`[bench] compare failed · setId=${setId} · ${msg}`)
      throw new HttpException(
        {
          statusCode: 500,
          code: 'BENCH_COMPARE_FAILED',
          message: msg,
        },
        HttpStatus.INTERNAL_SERVER_ERROR,
      )
    }
  }

  @Post('run')
  @ApiOperation({
    summary:
      "Run a task against the user's equipped Workshop build. Baseline is empty-build; enhanced composes the runtime from card ids (prompt/mcp/memory). Empty build ⇒ enhanced ≈ baseline.",
  })
  @ApiBody({
    schema: {
      type: 'object',
      required: ['taskId', 'build'],
      properties: {
        taskId: {
          type: 'string',
          enum: ['set-1-oracle', 'set-2-hunter', 'set-3-policy'],
        },
        build: {
          type: 'object',
          properties: {
            prompt: { type: 'string', nullable: true },
            mcp: { type: 'string', nullable: true },
            skillA: { type: 'string', nullable: true },
            skillB: { type: 'string', nullable: true },
            skillC: { type: 'string', nullable: true },
            orchestration: { type: 'string', nullable: true },
            memory: { type: 'string', nullable: true },
          },
        },
      },
    },
  })
  async run(
    @Body()
    body: { taskId?: string; build?: Partial<AgentBuildInput> },
  ): Promise<BenchRunResponse> {
    const taskId = body?.taskId
    if (!taskId || typeof taskId !== 'string') {
      throw new HttpException(
        { statusCode: 400, code: 'BENCH_INVALID_TASK', message: 'taskId is required' },
        HttpStatus.BAD_REQUEST,
      )
    }
    const build: AgentBuildInput = {
      prompt: body?.build?.prompt ?? null,
      mcp: body?.build?.mcp ?? null,
      skillA: body?.build?.skillA ?? null,
      skillB: body?.build?.skillB ?? null,
      skillC: body?.build?.skillC ?? null,
      orchestration: body?.build?.orchestration ?? null,
      memory: body?.build?.memory ?? null,
    }
    try {
      return await this.bench.run(taskId, build)
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err)
      this.logger.error(`[bench] run failed · taskId=${taskId} · ${msg}`)
      throw new HttpException(
        {
          statusCode: 500,
          code: 'BENCH_RUN_FAILED',
          message: msg,
        },
        HttpStatus.INTERNAL_SERVER_ERROR,
      )
    }
  }
}
