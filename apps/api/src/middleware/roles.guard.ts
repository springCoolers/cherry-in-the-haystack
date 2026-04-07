import { CanActivate, ExecutionContext, Injectable } from "@nestjs/common";
import { Reflector } from "@nestjs/core";

import { ROLES_KEY } from "src/common/decorators/roles.decorator";
import { Role } from "src/modules/users/entity/user.entity";

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private readonly reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>(ROLES_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);

    // @Roles 지정이 없으면 모두 허용
    if (!requiredRoles || requiredRoles.length === 0) return true;

    const { user } = context.switchToHttp().getRequest();

    // ★ Role.ANY 가 포함돼 있고 비로그인이라면 통과
    if (requiredRoles.includes(Role.ANY) && (!user || !user.role)) {
      return true;
    }

    // 로그인한 경우: role 검사
    if (!user || !user.role) return false;
    return requiredRoles.includes(user.role);
  }
}
