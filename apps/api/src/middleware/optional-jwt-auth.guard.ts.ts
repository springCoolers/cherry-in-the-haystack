import { Injectable, UnauthorizedException } from "@nestjs/common";
import { AuthGuard } from "@nestjs/passport";
import { TokenExpiredError } from "jsonwebtoken";

@Injectable()
export class OptionalJwtAuthGuard extends AuthGuard("jwt") {
  // err: Passport 내부 에러, user: payload 디코딩 결과, info: 검증 과정 정보
  handleRequest(err: any, user: any, info: any) {
    // 1) JWT 자체 오류는 그대로 던져서 401 처리
    if (err) {
      throw err;
    }

    // 2) 토큰이 만료된 경우 401 Unauthorized
    if (info instanceof TokenExpiredError || info?.name === "TokenExpiredError") {
      throw new UnauthorizedException("토큰이 만료되었습니다.");
    }

    // 3) 그 외(토큰 없음 or 유효)에는 user || undefined 반환
    return user ?? undefined;
  }
}
