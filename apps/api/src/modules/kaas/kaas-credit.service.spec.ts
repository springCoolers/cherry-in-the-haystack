import { Test, TestingModule } from '@nestjs/testing';
import { HttpException } from '@nestjs/common';
import { KaasCreditService } from './kaas-credit.service';
import { KARMA_DISCOUNT } from './types/kaas.types';

/**
 * KaasCreditService unit tests
 *
 * Focus: Karma-tier discount math + insufficient-credit error path.
 * Knex is mocked at the query-builder level — every chain returns the mock,
 * and `select`/`insert` resolve with the value queued via `__queueResult()`.
 */
describe('KaasCreditService', () => {
  let service: KaasCreditService;
  let queuedResults: any[];
  let lastInsertCall: { table: string; payload: any } | null;

  // Build a chainable mock that always returns itself except on terminal calls
  const buildMockKnex = () => {
    const fn: any = jest.fn((table: string) => {
      // Track which table was queried (for assertions)
      fn.__lastTable = table;
      return fn;
    });
    fn.where = jest.fn().mockReturnValue(fn);
    fn.select = jest.fn().mockImplementation(() =>
      Promise.resolve(queuedResults.shift() ?? [{ deposited: 0, consumed: 0 }]),
    );
    fn.insert = jest.fn().mockImplementation((payload: any) => {
      lastInsertCall = { table: fn.__lastTable, payload };
      return Promise.resolve();
    });
    fn.raw = jest.fn().mockImplementation((sql: string) => sql);
    return fn;
  };

  beforeEach(async () => {
    queuedResults = [];
    lastInsertCall = null;

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        KaasCreditService,
        { provide: 'KNEX_CONNECTION', useFactory: buildMockKnex },
      ],
    }).compile();

    service = module.get<KaasCreditService>(KaasCreditService);
  });

  describe('getBalance', () => {
    it('returns deposited - consumed when ledger has both', async () => {
      queuedResults.push([{ deposited: 500, consumed: 270 }]);
      const r = await service.getBalance('agent-1');
      expect(r).toEqual({ balance: 230, totalDeposited: 500, totalConsumed: 270 });
    });

    it('returns zero balance for empty ledger', async () => {
      queuedResults.push([{ deposited: 0, consumed: 0 }]);
      const r = await service.getBalance('agent-2');
      expect(r).toEqual({ balance: 0, totalDeposited: 0, totalConsumed: 0 });
    });
  });

  describe('consume — Karma discount tiers', () => {
    // Each test seeds enough deposit to cover the consume call.
    const seedBalance = (deposited: number) =>
      queuedResults.push([{ deposited, consumed: 0 }]);

    it('Bronze (0% discount) — 20cr purchase costs 20cr', async () => {
      seedBalance(100);
      const r = await service.consume('a', 20, 'Bronze', 'rag', 'purchase');
      expect(r.consumed).toBe(20);
      expect(r.remaining).toBe(80);
      expect(lastInsertCall?.payload.amount).toBe(-20);
    });

    it('Silver (5% discount) — 20cr → 19cr', async () => {
      seedBalance(100);
      const r = await service.consume('a', 20, 'Silver', 'rag', 'purchase');
      expect(r.consumed).toBe(19); // round(20 * 0.95) = 19
      expect(r.remaining).toBe(81);
    });

    it('Gold (15% discount) — 20cr → 17cr', async () => {
      seedBalance(100);
      const r = await service.consume('a', 20, 'Gold', 'rag', 'purchase');
      expect(r.consumed).toBe(17); // round(20 * 0.85) = 17
      expect(r.remaining).toBe(83);
    });

    it('Platinum (30% discount) — 20cr → 14cr', async () => {
      seedBalance(100);
      const r = await service.consume('a', 20, 'Platinum', 'rag', 'purchase');
      expect(r.consumed).toBe(14); // round(20 * 0.70) = 14
      expect(r.remaining).toBe(86);
    });

    it('Platinum follow (25cr) → 18cr', async () => {
      seedBalance(100);
      const r = await service.consume('a', 25, 'Platinum', 'rag', 'follow');
      // round(25 * 0.70) = round(17.5) = 18
      expect(r.consumed).toBe(18);
      expect(r.remaining).toBe(82);
    });

    it('discount table covers all 4 tiers', () => {
      expect(KARMA_DISCOUNT).toEqual({
        Bronze: 0,
        Silver: 0.05,
        Gold: 0.15,
        Platinum: 0.30,
      });
    });
  });

  describe('consume — insufficient balance', () => {
    it('throws 402 INSUFFICIENT_CREDITS when balance < required', async () => {
      queuedResults.push([{ deposited: 10, consumed: 0 }]);
      await expect(
        service.consume('agent-x', 20, 'Bronze', 'rag', 'purchase'),
      ).rejects.toThrow(HttpException);
    });

    it('error response includes credits_required and credits_available', async () => {
      queuedResults.push([{ deposited: 5, consumed: 0 }]);
      try {
        await service.consume('agent-x', 20, 'Bronze', 'rag', 'purchase');
        fail('expected throw');
      } catch (e: any) {
        const body = e.getResponse();
        expect(body).toMatchObject({
          code: 'INSUFFICIENT_CREDITS',
          credits_required: 20,
          credits_available: 5,
        });
        expect(e.getStatus()).toBe(402);
      }
    });

    it('Platinum discount is applied BEFORE balance check (cheaper user passes)', async () => {
      // 16cr balance, Platinum discount on 20cr = 14cr → should pass
      queuedResults.push([{ deposited: 16, consumed: 0 }]);
      const r = await service.consume('a', 20, 'Platinum', 'rag', 'purchase');
      expect(r.consumed).toBe(14);
      expect(r.remaining).toBe(2);
    });
  });

  describe('deposit', () => {
    it('inserts ledger row and returns updated balance', async () => {
      // First call: insert (no result needed). Second call: getBalance.
      queuedResults.push([{ deposited: 250, consumed: 0 }]);
      const r = await service.deposit('agent-1', 250, '0xabc', 'status');
      expect(r.balance).toBe(250);
      expect(r.txHash).toBe('0xabc');
      expect(lastInsertCall?.payload).toMatchObject({
        agent_id: 'agent-1',
        amount: 250,
        type: 'deposit',
        tx_hash: '0xabc',
        chain: 'status',
      });
    });

    it('persists null tx_hash and chain when omitted', async () => {
      queuedResults.push([{ deposited: 100, consumed: 0 }]);
      await service.deposit('agent-1', 100);
      expect(lastInsertCall?.payload).toMatchObject({
        tx_hash: null,
        chain: null,
      });
    });
  });
});
