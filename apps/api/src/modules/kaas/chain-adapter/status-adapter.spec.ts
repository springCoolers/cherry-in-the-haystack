import { mapOnchainTier } from './status-adapter';

/**
 * mapOnchainTier — Status Network 11-tier → KaaS 4-tier mapping
 *
 * Status Hoodi KarmaTiers contract returns one of 11 tier names:
 *   none, entry, newbie, basic, active, regular, power, pro, high-throughput, s-tier, legendary
 *
 * KaaS discount table operates on the legacy 4-tier model:
 *   Bronze, Silver, Gold, Platinum
 *
 * This mapping must remain stable — changing it shifts the discount applied
 * at purchase time for every Status-network agent.
 */
describe('mapOnchainTier', () => {
  describe('Bronze (no discount)', () => {
    it.each(['none', 'entry', 'newbie'])(
      '%s → Bronze',
      (name) => {
        expect(mapOnchainTier(name)).toBe('Bronze');
      },
    );
  });

  describe('Silver (5% discount)', () => {
    it.each(['basic', 'active'])('%s → Silver', (name) => {
      expect(mapOnchainTier(name)).toBe('Silver');
    });
  });

  describe('Gold (15% discount)', () => {
    it.each(['regular', 'power'])('%s → Gold', (name) => {
      expect(mapOnchainTier(name)).toBe('Gold');
    });
  });

  describe('Platinum (30% discount)', () => {
    it.each(['pro', 'high-throughput', 's-tier', 'legendary'])(
      '%s → Platinum',
      (name) => {
        expect(mapOnchainTier(name)).toBe('Platinum');
      },
    );
  });

  describe('unknown / safety fallback', () => {
    it('unknown tier → Bronze (safest default — no discount)', () => {
      expect(mapOnchainTier('mythic')).toBe('Bronze');
      expect(mapOnchainTier('')).toBe('Bronze');
      expect(mapOnchainTier('GOLD')).toBe('Bronze'); // case-sensitive
    });
  });

  describe('full coverage of 11 documented onchain tiers', () => {
    it('every onchain tier name maps to a valid 4-tier value', () => {
      const ALL_ONCHAIN = [
        'none', 'entry', 'newbie', 'basic', 'active',
        'regular', 'power', 'pro', 'high-throughput', 's-tier', 'legendary',
      ];
      const VALID_LEGACY = new Set(['Bronze', 'Silver', 'Gold', 'Platinum']);
      for (const t of ALL_ONCHAIN) {
        expect(VALID_LEGACY.has(mapOnchainTier(t))).toBe(true);
      }
    });
  });
});
