# Minimal Code Review Prompt

You are reviewing the codebase for Epic 1+2 integration.

## References
- Integration plan: `_bmad-output/planning-artifacts/epic-1-2-team-integration-plan.md`
- Schema: `docs/architecture/ddl-v1.0.sql`
- Status: `_bmad-output/implementation-artifacts/1-1-status-check.md`

## Review Format

For each component, provide:

```
[path]
Purpose: one line
Entry: file:line
Key files: file1 (purpose), file2 (purpose)
State: working | partial | broken
Reusable: yes/no
```

## Areas

1. **TS**: `packages/pipeline/`, `apps/api/`, `apps/web/`
2. **Python**: `dev/packages/ontology/`, `dev/packages/pdf_knowledge_extractor/`
3. **Branches**: `feat/pdf-extractor-v2`, `feat/pdf-knowledge-extractor`, `feature/ontology`, `feat/agent-writer`

## What I Need

- How to create a new job?
- How is DB connected?
- Which Python methods → API endpoints?
- What's blocking integration?

No long reports. Just the facts.
