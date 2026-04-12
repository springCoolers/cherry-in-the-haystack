import {
  CanActivate,
  ExecutionContext,
  Injectable,
  UnauthorizedException,
} from '@nestjs/common';

@Injectable()
export class AgentApiKeyGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const apiKey = request.headers['x-api-key'];
    const expected = process.env.AGENT_API_KEY;

    if (!expected) {
      throw new UnauthorizedException('AGENT_API_KEY가 설정되지 않았습니다.');
    }

    if (!apiKey || apiKey !== expected) {
      throw new UnauthorizedException('유효하지 않은 API Key입니다.');
    }

    return true;
  }
}
