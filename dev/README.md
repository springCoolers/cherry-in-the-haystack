# Dev Directory

프로젝트의 주요 개발 코드가 위치하는 루트 디렉토리입니다.

## 디렉토리 구조

```
dev/
├─ apps/            # 애플리케이션 코드
│  ├─ web/          # 프런트엔드 (Next.js/React 등)
│  ├─ api/          # 백엔드 (FastAPI/Express 등)
│  └─ agent/        # LLM/프롬프트/평가
├─ packages/        # 공용 모듈 (유틸, 디자인시스템 등)
├─ infra/           # IaC + 배포 스크립트
├─ scripts/         # CI/CD, 마이그레이션, 동기화 스크립트
└─ .github/         # GitHub 설정
   └─ workflows/    # CI/CD 워크플로우
```
