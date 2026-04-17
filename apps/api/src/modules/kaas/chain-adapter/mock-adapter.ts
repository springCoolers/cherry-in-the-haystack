/**
 * MockAdapter — DEMO_FALLBACK용 목 어댑터
 *
 * 실제 블록체인 호출 없이 랜덤 해시를 반환.
 * 체인별 적절한 explorer URL 반환 (status / near / mock).
 */

import { IChainAdapter, TxResult, KarmaTier } from "./interface";
import crypto from "crypto";

type MockChain = "status" | "near" | "mock";

function randomHash(): string {
  return "0x" + crypto.randomBytes(32).toString("hex");
}

function randomNearHash(): string {
  // NEAR tx hash는 base58 형식 (44자 내외)
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789";
  return Array.from({ length: 44 }, () => chars[Math.floor(Math.random() * chars.length)]).join("");
}

export class MockAdapter implements IChainAdapter {
  constructor(private readonly pretendChain: MockChain = "status") {}

  private makeTx(): TxResult {
    if (this.pretendChain === "near") {
      const hash = randomNearHash();
      return {
        hash,
        chain: "near",
        explorerUrl: `https://testnet.nearblocks.io/txns/${hash}`,
      };
    }
    // status / mock → Sepolia 형식
    const hash = randomHash();
    return {
      hash,
      chain: this.pretendChain === "status" ? "status" : "mock",
      explorerUrl: `https://sepoliascan.status.network/tx/${hash}`,
    };
  }

  async recordProvenance(_hash: string, _agent: string, _conceptId: string): Promise<TxResult> {
    return this.makeTx();
  }

  async depositCredit(_agent: string, _amount: number): Promise<TxResult> {
    return this.makeTx();
  }

  async consumeCredit(_agent: string, _amount: number, _conceptId: string, _actionType: string): Promise<TxResult> {
    return this.makeTx();
  }

  async withdrawReward(_curator: string, _amount: number): Promise<TxResult> {
    return this.makeTx();
  }

  async getKarmaTier(_address: string): Promise<KarmaTier> {
    return { tier: "Silver", balance: 1250 };
  }
}
