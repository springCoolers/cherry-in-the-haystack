import { Controller } from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';

/**
 * 주의: chat 엔드포인트는 kaas-query.controller.ts의 @Post('llm/chat')로 통합됨.
 * 경로 충돌(v1/kaas/llm/chat) 방지를 위해 이 컨트롤러의 chat 메서드는 제거함.
 */
@Controller('v1/kaas/llm')
@ApiTags('KaaS — LLM Proxy')
export class KaasLlmController {}
