/**
 * IChainAdapter — 블록체인 추상화 인터페이스
 *
 * 모든 온체인 작업은 이 인터페이스를 통해 호출.
 * 환경변수 CHAIN_ADAPTER (status | bnb | near | mock) 로 구현체 스위칭.
 */

export interface TxResult {
  hash: string;
  chain: string;
  explorerUrl: string;
}

export interface KarmaTier {
  /** Legacy 4-tier (Bronze/Silver/Gold/Platinum) — mapped from onchain tier name for KaaS discount table */
  tier: "Bronze" | "Silver" | "Gold" | "Platinum";
  /** Karma balance (human-readable, already divided by 10^18) */
  balance: number;
  /** Status Network Karma onchain tier ID (0=none, 1=entry, 2=newbie, 3=basic, 4=active, 5=regular, 6=power, 7=pro, 8=high-throughput, 9=s-tier, 10=legendary) */
  onchainTierId?: number;
  /** Onchain tier name (e.g. "active", "pro") — raw value from KarmaTiers contract */
  onchainTierName?: string;
  /** Number of gasless transactions allowed per epoch at this tier */
  txPerEpoch?: number;
}

export interface IChainAdapter {
  /** 프로비넌스(지식 구매 영수증) 온체인 기록 */
  recordProvenance(hash: string, agent: string, conceptId: string): Promise<TxResult>;

  /** 에이전트 크레딧 충전 */
  depositCredit(agent: string, amount: number): Promise<TxResult>;

  /** 에이전트 크레딧 차감 (구매/팔로우 시) */
  consumeCredit(agent: string, amount: number, conceptId: string, actionType: string): Promise<TxResult>;

  /** 큐레이터 보상 출금 */
  withdrawReward(curator: string, amount: number): Promise<TxResult>;

  /** Karma 티어 조회 (Status Network 전용) */
  getKarmaTier(address: string): Promise<KarmaTier>;
}
