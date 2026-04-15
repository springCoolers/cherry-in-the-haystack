import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import * as dotenv from "dotenv";
import * as path from "path";

// .env는 apps/api/.env에 있음 (모노레포 구조)
dotenv.config({ path: path.resolve(__dirname, "../api/.env") });

const config: HardhatUserConfig = {
  solidity: "0.8.24",
  networks: {
    // Status Network Sepolia (currently live deployment)
    // Uses DEPLOYER_PRIVATE_KEY → 0xd4452Aa4Ea996995AF94FbC4aEE4929BbCEBe7C4
    statusSepolia: {
      url: process.env.STATUS_RPC_URL || "https://public.sepolia.rpc.status.network",
      chainId: 1660990954,
      accounts: process.env.DEPLOYER_PRIVATE_KEY ? [process.env.DEPLOYER_PRIVATE_KEY] : [],
      gasPrice: 0,
    },
    // Status Network Hoodi (new redeploy target — Sepolia sunsets end of April 2026)
    // Uses HOODI_DEPLOYER_PRIVATE_KEY → 0xdab76820d6BEb239DB5ec031a6970f59EEbae130
    statusHoodi: {
      url: process.env.STATUS_HOODI_RPC_URL || "https://public.hoodi.rpc.status.network",
      chainId: 374,
      accounts: process.env.HOODI_DEPLOYER_PRIVATE_KEY ? [process.env.HOODI_DEPLOYER_PRIVATE_KEY] : [],
      gasPrice: 0,
    },
    // opBNB Testnet (Day 4용)
    opbnbTestnet: {
      url: "https://opbnb-testnet-rpc.bnbchain.org:8545",
      chainId: 5611,
      accounts: process.env.DEPLOYER_PRIVATE_KEY ? [process.env.DEPLOYER_PRIVATE_KEY] : [],
    },
  },
  // Contract verify (Blockscout-based explorers don't require a real API key — any string is OK)
  etherscan: {
    apiKey: {
      statusHoodi: "empty",
      statusSepolia: "empty",
    },
    customChains: [
      {
        network: "statusHoodi",
        chainId: 374,
        urls: {
          apiURL: "https://hoodiscan.status.network/api",
          browserURL: "https://hoodiscan.status.network",
        },
      },
      {
        network: "statusSepolia",
        chainId: 1660990954,
        urls: {
          apiURL: "https://sepoliascan.status.network/api",
          browserURL: "https://sepoliascan.status.network",
        },
      },
    ],
  },
  sourcify: {
    enabled: false, // disable Sourcify (Blockscout verify is enough on Hoodi)
  },
};

export default config;
