/**
 * Raw ethers.js deploy (bypass hardhat-ethers).
 * Needed because hardhat-ethers signers.ts:195 calls eth_getTransactionByHash
 * with an argument Status Hoodi RPC rejects.
 *
 * Usage:
 *   ts-node scripts/deploy-raw.ts
 */

import { ethers, FetchRequest } from "ethers";
import * as fs from "fs";
import * as path from "path";
import * as dotenv from "dotenv";

dotenv.config({ path: path.resolve(__dirname, "../../api/.env") });

// Force IPv4 resolution (Tailscale + IPv6 issue)
FetchRequest.registerGetUrl(FetchRequest.createGetUrlFunc({ family: 4 }));

async function main() {
  const rpcUrl = process.env.STATUS_RPC_URL || "https://public.hoodi.rpc.status.network";
  const pk = process.env.DEPLOYER_PRIVATE_KEY;
  if (!pk) throw new Error("DEPLOYER_PRIVATE_KEY missing in .env");

  const provider = new ethers.JsonRpcProvider(
    rpcUrl,
    { chainId: 374, name: "statusHoodi" },
    { batchMaxCount: 1 }  // Status Hoodi RPC rejects batch requests (503)
  );

  const wallet = new ethers.Wallet(pk, provider);
  console.log("Deployer:", wallet.address);

  const balance = await provider.getBalance(wallet.address);
  console.log("Balance:", ethers.formatEther(balance), "ETH");

  const nonce = await provider.getTransactionCount(wallet.address);
  console.log("Nonce:", nonce);

  const artifactPath = path.resolve(
    __dirname,
    "../artifacts/contracts/CherryCredit.sol/CherryCredit.json"
  );
  const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf-8"));

  // Build constructor data: bytecode + encoded args
  const iface = new ethers.Interface(artifact.abi);
  const encodedArgs = iface.encodeDeploy([wallet.address]);
  const data = artifact.bytecode + encodedArgs.slice(2);

  // Status Network requires linea_estimateGas (not eth_estimateGas) — Karma/RLN-aware
  console.log("Calling linea_estimateGas (Status Network requirement)...");
  const lineaGas: any = await provider.send("linea_estimateGas", [{
    from: wallet.address,
    data,
  }]);
  console.log("linea_estimateGas:", lineaGas);
  const gasLimit = BigInt(lineaGas.gasLimit);
  const baseFee = BigInt(lineaGas.baseFeePerGas ?? 0);
  const priorityFee = BigInt(lineaGas.priorityFeePerGas ?? 0);
  console.log(`gasLimit=${gasLimit}, baseFee=${baseFee}, priorityFee=${priorityFee}`);

  // Sign a raw legacy tx manually (bypass ethers populateTransaction)
  const tx = {
    type: 0,
    chainId: 374,
    nonce,
    gasLimit,
    gasPrice: baseFee + priorityFee, // 0 for gasless-eligible users (Karma + RLN registered)
    data,
    // `to` omitted → contract deployment
  };

  console.log("Signing raw tx...");
  const signed = await wallet.signTransaction(tx);
  console.log("Broadcasting...");
  const txResp = await provider.broadcastTransaction(signed);
  console.log("Deploy tx hash:", txResp.hash);

  console.log("Waiting for confirmation...");
  const receipt = await txResp.wait();
  if (!receipt || !receipt.contractAddress) {
    throw new Error("Deploy failed — no contractAddress in receipt");
  }
  const address = receipt.contractAddress;

  console.log("");
  console.log("═══════════════════════════════════════");
  console.log("CherryCredit deployed to:", address);
  console.log("═══════════════════════════════════════");
  console.log("Explorer:", `https://hoodiscan.status.network/address/${address}`);
  console.log("");
  console.log("→ .env 갱신:");
  console.log(`CHERRY_CREDIT_ADDRESS=${address}`);
}

main().catch((e) => {
  console.error(e);
  process.exitCode = 1;
});
