import { Test, TestingModule } from '@nestjs/testing';
import { KaasKnowledgeService } from './kaas-knowledge.service';

/**
 * KaasKnowledgeService unit tests
 *
 * Focus: search / findById / mapConcept (snake_case → camelCase),
 *        evidence joining, is_active filter, ordering by quality_score.
 *
 * Knex builder is mocked as a chainable thenable. Each `await` on the
 * builder pulls the next array from `resultsQueue`. Sub-query callbacks
 * (`.where(function(){...})`) are invoked with `this = builder` so any
 * nested whereRaw/orWhereRaw chains stay legal.
 */
describe('KaasKnowledgeService', () => {
  let service: KaasKnowledgeService;
  let resultsQueue: any[][];
  let calls: { table: string; method: string; args: any[] }[];

  const mkBuilder = (lastTable: { value: string }) => {
    const builder: any = {};
    const record = (method: string) => (...args: any[]) => {
      calls.push({ table: lastTable.value, method, args });
      // sub-query callback support
      if (method === 'where' && typeof args[0] === 'function') {
        args[0].call(builder);
      }
      return builder;
    };
    for (const m of [
      'where', 'whereIn', 'whereRaw', 'orWhereRaw', 'orderBy',
      'limit', 'select', 'count', 'returning', 'update', 'insert', 'delete',
    ]) {
      builder[m] = jest.fn(record(m));
    }
    builder.first = jest.fn().mockImplementation(() => {
      calls.push({ table: lastTable.value, method: 'first', args: [] });
      const r = resultsQueue.shift() ?? [];
      return Promise.resolve(Array.isArray(r) ? r[0] : r);
    });
    // thenable
    builder.then = (resolve: any, reject: any) => {
      try {
        const r = resultsQueue.shift() ?? [];
        return Promise.resolve(r).then(resolve, reject);
      } catch (e) {
        return Promise.reject(e).catch(reject);
      }
    };
    return builder;
  };

  const mkKnex = () => {
    const lastTable = { value: '' };
    const fn: any = jest.fn((table: string) => {
      lastTable.value = table;
      return mkBuilder(lastTable);
    });
    fn.raw = jest.fn((sql: string) => sql);
    return fn;
  };

  beforeEach(async () => {
    resultsQueue = [];
    calls = [];
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        KaasKnowledgeService,
        { provide: 'KNEX_CONNECTION', useFactory: mkKnex },
      ],
    }).compile();
    service = module.get<KaasKnowledgeService>(KaasKnowledgeService);
  });

  describe('search', () => {
    it('returns mapped Concept[] when matches found', async () => {
      const conceptRow = {
        id: 'rag', title: 'Retrieval-Augmented Generation', category: 'RAG',
        summary: 'RAG basics', quality_score: '4.5', source_count: 3,
        updated_at: '2026-04-15T00:00:00Z', related_concepts: ['embeddings'],
      };
      const evidenceRow = {
        id: 'rag-ev-1', concept_id: 'rag',
        source: 'arXiv', summary: 'paper summary',
        curator: 'Hyejin Kim', curator_tier: 'Gold', comment: 'solid',
      };
      resultsQueue.push([conceptRow]);  // first await: concept rows
      resultsQueue.push([evidenceRow]); // second await: evidence rows

      const r = await service.search('rag');
      expect(r).toHaveLength(1);
      expect(r[0]).toMatchObject({
        id: 'rag',
        title: 'Retrieval-Augmented Generation',
        qualityScore: 4.5,        // parseFloat applied
        sourceCount: 3,
        updatedAt: '2026-04-15',  // ISO slice(0,10)
        relatedConcepts: ['embeddings'],
      });
      expect(r[0].evidence).toHaveLength(1);
      expect(r[0].evidence[0]).toMatchObject({
        curator: 'Hyejin Kim',
        curatorTier: 'Gold',       // snake_case → camelCase
      });
    });

    it('returns [] and skips evidence query when no concepts match', async () => {
      resultsQueue.push([]);  // empty concept result
      const r = await service.search('nonexistent');
      expect(r).toEqual([]);
      // evidence table must NOT be queried (perf optimization)
      const evidenceCalls = calls.filter((c) => c.table === 'kaas.evidence');
      expect(evidenceCalls).toHaveLength(0);
    });

    it('lowercases the query and wraps with %...% (case-insensitive LIKE)', async () => {
      resultsQueue.push([]);
      await service.search('GPT-5');
      const whereRawCall = calls.find((c) => c.method === 'whereRaw');
      expect(whereRawCall).toBeDefined();
      // Second arg is the bind array
      expect(whereRawCall!.args[1]).toEqual(['%gpt-5%']);
    });

    it('searches across title, summary, AND id (3 OR clauses)', async () => {
      resultsQueue.push([]);
      await service.search('rag');
      const rawCalls = calls.filter((c) => c.method === 'whereRaw' || c.method === 'orWhereRaw');
      // 1 whereRaw + 2 orWhereRaw = 3 fields
      expect(rawCalls).toHaveLength(3);
      const sqls = rawCalls.map((c) => c.args[0]);
      expect(sqls.some((s) => s.includes('title'))).toBe(true);
      expect(sqls.some((s) => s.includes('summary'))).toBe(true);
      expect(sqls.some((s) => s.includes('id'))).toBe(true);
    });

    it('orders results by quality_score DESC', async () => {
      resultsQueue.push([]);
      await service.search('any');
      const orderCall = calls.find((c) => c.method === 'orderBy');
      expect(orderCall?.args).toEqual(['quality_score', 'desc']);
    });

    it('applies is_active = true filter', async () => {
      resultsQueue.push([]);
      await service.search('any');
      const activeFilter = calls.find(
        (c) => c.method === 'where' && c.args[0] === 'is_active' && c.args[1] === true,
      );
      expect(activeFilter).toBeDefined();
    });

    it('joins evidence using whereIn over matched concept ids', async () => {
      resultsQueue.push([{ id: 'a', title: 'A', category: 'x', summary: 's', quality_score: 1 }]);
      resultsQueue.push([]);
      await service.search('a');
      const whereInCall = calls.find((c) => c.method === 'whereIn' && c.table === 'kaas.evidence');
      expect(whereInCall?.args).toEqual(['concept_id', ['a']]);
    });
  });

  describe('findById', () => {
    it('returns null when concept does not exist', async () => {
      resultsQueue.push([null]);  // .first() unwraps
      const r = await service.findById('missing');
      expect(r).toBeNull();
    });

    it('returns mapped Concept (without contentMd) when found', async () => {
      resultsQueue.push([{
        id: 'rag', title: 'RAG', category: 'RAG', summary: 's',
        quality_score: 5, source_count: 0, related_concepts: null,
      }]);
      resultsQueue.push([]);  // no evidence
      const r = await service.findById('rag');
      expect(r).toMatchObject({ id: 'rag', title: 'RAG', qualityScore: 5 });
      expect((r as any).contentMd).toBeUndefined();  // findById never adds content
      expect(r!.relatedConcepts).toEqual([]);  // null → [] default
    });
  });

  describe('findByIdWithContent', () => {
    it('returns null when concept does not exist', async () => {
      resultsQueue.push([null]);
      const r = await service.findByIdWithContent('missing');
      expect(r).toBeNull();
    });

    it('includes contentMd in response when present', async () => {
      resultsQueue.push([{
        id: 'rag', title: 'RAG', category: 'RAG', summary: 's',
        quality_score: 5, content_md: '## RAG full content here',
      }]);
      resultsQueue.push([]);
      const r = await service.findByIdWithContent('rag');
      expect(r?.contentMd).toBe('## RAG full content here');
    });

    it('returns contentMd as null when DB column is null', async () => {
      resultsQueue.push([{
        id: 'rag', title: 'RAG', category: 'RAG', summary: 's',
        quality_score: 5, content_md: null,
      }]);
      resultsQueue.push([]);
      const r = await service.findByIdWithContent('rag');
      expect(r?.contentMd).toBeNull();
    });
  });

  describe('findAll', () => {
    it('returns [] and skips evidence query when no active concepts', async () => {
      resultsQueue.push([]);
      const r = await service.findAll();
      expect(r).toEqual([]);
      expect(calls.filter((c) => c.table === 'kaas.evidence')).toHaveLength(0);
    });

    it('returns concepts ordered by quality_score with their evidence', async () => {
      resultsQueue.push([
        { id: 'a', title: 'A', category: 'x', summary: '', quality_score: 5 },
        { id: 'b', title: 'B', category: 'x', summary: '', quality_score: 3 },
      ]);
      resultsQueue.push([
        { id: 'a-ev-1', concept_id: 'a', source: 's', summary: '', curator: 'c', curator_tier: 'Gold', comment: '' },
        { id: 'b-ev-1', concept_id: 'b', source: 's', summary: '', curator: 'c', curator_tier: 'Silver', comment: '' },
      ]);
      const r = await service.findAll();
      expect(r).toHaveLength(2);
      expect(r[0].evidence).toHaveLength(1);
      expect(r[1].evidence).toHaveLength(1);
      expect(r[0].evidence[0].id).toBe('a-ev-1');  // each concept gets ONLY its evidence
      expect(r[1].evidence[0].id).toBe('b-ev-1');
    });
  });

  describe('findByCategory', () => {
    it('filters by category + is_active', async () => {
      resultsQueue.push([]);
      await service.findByCategory('RAG');
      const filterCall = calls.find(
        (c) =>
          c.method === 'where' &&
          typeof c.args[0] === 'object' &&
          c.args[0]?.category === 'RAG' &&
          c.args[0]?.is_active === true,
      );
      expect(filterCall).toBeDefined();
    });
  });
});
