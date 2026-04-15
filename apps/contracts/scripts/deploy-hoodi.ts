import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", ethers.formatEther(balance), "ETH");

  const nonce = await ethers.provider.getTransactionCount(deployer.address);
  console.log("Nonce:", nonce);

  // deploy-only, skip post-deploy tests (Status Network RPC quirk with getTransaction)
  const CherryCredit = await ethers.getContractFactory("CherryCredit");
  console.log("Sending deploy transaction...");

  try {
    const contract = await CherryCredit.deploy(deployer.address);
    const deployTx = contract.deploymentTransaction();
    if (deployTx) {
      console.log("Deploy tx hash:", deployTx.hash);
    }
    await contract.waitForDeployment();
    const address = await contract.getAddress();
    console.log("");
    console.log("═══════════════════════════════════════");
    console.log("CherryCredit deployed to:", address);
    console.log("═══════════════════════════════════════");
    console.log("");
    console.log("→ .env 갱신:");
    console.log(`CHERRY_CREDIT_ADDRESS=${address}`);
  } catch (e: any) {
    // If deploy actually succeeded but hardhat threw on post-deploy check,
    // we still want the predicted address.
    const predicted = ethers.getCreateAddress({
      from: deployer.address,
      nonce,
    });
    console.log("");
    console.log("⚠ hardhat threw during post-deploy verification.");
    console.log("Predicted contract address (from nonce):", predicted);
    console.log("Error:", e.message ?? e);
    console.log("");
    console.log("→ explorer에서 확인:");
    console.log(`https://hoodiscan.status.network/address/${predicted}`);
    throw e;
  }
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
