# On-Chain Security Suite  
### AI-Powered Token Auditor • ML Deployer Reputation Engine • Etherscan V2 Integration • Solidity Registries
<p align="center">
  <img src="https://img.shields.io/badge/Powered%20By-AI%20%26%20ML-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Security-Web3%20Security-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Solidity-0.8.x-black?style=for-the-badge&logo=solidity" />
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Etherscan-V2%20API-1f78ff?style=for-the-badge&logo=ethereum" />
  <img src="https://img.shields.io/badge/ML-RandomForest-brightgreen?style=for-the-badge&logo=scikit-learn" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<br>

---

The **On-Chain Security Suite** is a complete, end-to-end Web3 security pipeline.  
It combines:

- **Static analysis of token contracts** (rugpull pattern detection)  
- **Machine learning–based reputation scoring** for deployer addresses  
- **Etherscan V2 integration** for fetching real on-chain data  
- **Solidity registries** to store token audits and deployer scores on-chain  

This project is designed as:

- A **portfolio-quality security research project**  
- A **practical toolkit** for analysts and developers  
- A **template** for building more advanced Web3 security systems  

---

## Table of Contents

1. [Motivation & Problem Statement](#motivation--problem-statement)  
2. [High-Level Overview](#high-level-overview)  
3. [Core Components](#core-components)  
4. [Architecture](#architecture)  
5. [Folder Structure](#folder-structure)  
6. [Installation & Setup](#installation--setup)  
7. [Token Risk Auditor (Static Analyzer)](#token-risk-auditor-static-analyzer)  
    - [Patterns Detected](#patterns-detected)  
    - [Feature Extraction](#feature-extraction)  
    - [Risk Scoring Logic](#risk-scoring-logic)  
8. [Deployer Reputation Engine (ML Model)](#deployer-reputation-engine-ml-model)  
    - [Deployer-Level Features](#deployer-level-features)  
    - [Labeling Strategy](#labeling-strategy)  
    - [Model Architecture](#model-architecture)  
    - [From Probability to Risk Categories](#from-probability-to-risk-categories)  
9. [Machine Learning Training Pipeline](#machine-learning-training-pipeline)  
10. [Etherscan V2 Integration](#etherscan-v2-integration)  
    - [Fetching Transactions](#fetching-transactions)  
    - [Fetching Contract Source Code](#fetching-contract-source-code)  
    - [Building Deployer History Automatically](#building-deployer-history-automatically)  
11. [Solidity Registries](#solidity-registries)  
    - [TokenAuditRegistry.sol](#tokenauditregistrysol)  
    - [DeployerReputationRegistry.sol](#deployerreputationregistrysol)  
12. [CLI Tools & Workflows](#cli-tools--workflows)  
13. [End-to-End Example Flow](#end-to-end-example-flow)  
14. [Assumptions & Limitations](#assumptions--limitations)  
15. [Ideas for Extension](#ideas-for-extension)  
16. [Roadmap](#roadmap)  
17. [License](#license)  

---

## Motivation & Problem Statement

The token ecosystem on Ethereum and EVM-compatible chains is:

- Fast-moving  
- Permissionless  
- Filled with both innovation **and** scams  

Common problems:

- **Rugpulls**, the owner drains liquidity or mints massive supply  
- **Honeypots**, you can buy but not sell  
- **Blacklist-based traps**, certain addresses are silently blocked  
- **Tax manipulation**, “fair” token suddenly applies massive fees  
- **Bad actors**, deployers who keep launching scams

Humans cannot manually review every contract. We need tools that:

- Read Solidity source code  
- Detect patterns associated with malicious behavior  
- Aggregate deployer history  
- Use ML to estimate how risky a deployer is  
- Integrate with real on-chain data (Etherscan)  
- Optionally store results on-chain for transparency  

That’s exactly what this suite does.

---

## High-Level Overview

The project has **three main layers**:

1. **Token-Level Analysis**  
   - Reads Solidity token contracts  
   - Extracts risk features  
   - Produces a risk score and label  

2. **Deployer-Level Reputation**  
   - Aggregates all tokens deployed by an address  
   - Uses a machine learning model to estimate “maliciousness probability”  
   - Outputs a trust score and human-readable label  

3. **Integration & Transparency Layer**  
   - Uses Etherscan V2 to discover deployed contracts and fetch source code  
   - Provides Solidity registries to store audit and reputation results on-chain  

This makes it possible to:

- Analyze local contracts  
- Analyze real world deployers  
- Train and use real ML models  
- (If desired) publish security results on-chain.

---

## Core Components

- **`src/token_auditor`**  
  Static analysis for smart contracts (rugpull detection).

- **`src/reputation`**  
  Feature extraction and ML-based scoring for deployers.

- **`src/etherscan_integration`**  
  Etherscan V2 API client for fetching real on-chain history.

- **`src/ml`**  
  Machine learning training + model utilities.

- **`contracts/`**  
  Two Solidity contracts for on-chain storage of audits & reputation.

- **`data/`**  
  Example token contracts and a synthetic deployer dataset.

- **`artifacts/`**  
  Trained ML models (`deployer_model.joblib`).

---

## Architecture

The On-Chain Security Suite consists of three major layers:
1. **Token-Level Analysis**  
2. **Deployer-Level ML Reputation Scoring**  
3. **Blockchain Integration (Etherscan V2 + Solidity Registries)**

Below is the full architecture diagram:

                               ┌───────────────────────────┐
                               │  Solidity Token Contract  │
                               └──────────────┬────────────┘
                                              │
                                              ▼
                               ┌─────────────────────────────┐
                               │  Static Token Auditor       │
                               │  - Regex feature extraction │
                               │  - Risk scoring ruleset     │
                               └──────────────┬──────────────┘
                                              │
                         Token risk label ────┘
                                              │
                                              ▼
                 ┌─────────────────────────────────────────────┐
                 │   Deployer History (Local or Etherscan)     │
                 │   - List of deployed contract addresses     │
                 │   - Token risk scores/labels per contract   │
                 └──────────────┬──────────────────────────────┘
                                │
                                ▼
                  ┌────────────────────────────────┐
                  │ Deployer Feature Aggregator    │
                  │  - n_safe                      │
                  │  - n_suspicious                │
                  │  - n_rugpull                   │
                  │  - frac_safe / frac_rugpull    │
                  └──────────────┬─────────────────┘
                                 │
                                 ▼
                     ┌──────────────────────────┐
                     │ ML Deployer Reputation   │
                     │   (RandomForest Model)   │
                     │   - P(bad deployer)      │
                     │   - Trust Score (0–100)  │
                     │   - Risk Class           │
                     └──────────────┬───────────┘
                                    │
                                    ▼
               ┌─────────────────────────────────────────────┐
               │            Final Reputation Results         │
               │   { score, risk_class, label, features }    │
               └──────────────┬──────────────────────────────┘
                              │
                              ▼
     ┌──────────────────────────────────────────────────────────────────────┐
     │          Optional On-Chain Registries (Solidity)                     │
     │                                                                      │
     │  TokenAuditRegistry.sol          DeployerReputationRegistry.sol      │
     │  - Report token risk             - Store deployer trust score        │
     │  - Store details JSON            - Expose transparent on-chain data  │
     └──────────────────────────────────────────────────────────────────────┘

                     ▲
                     │
    ┌────────────────┴────────────────┐
    │     Etherscan V2 Integration    │
    │  - Fetch deployer tx list       │
    │  - Fetch contract source code   │
    │  - Auto-classify tokens         │
    └─────────────────────────────────┘


And **Etherscan V2** is used to auto-generate the “Deployer History (JSON)” layer by discovering and classifying real contracts.

---

## Folder Structure

```text
onchain-security-suite/
│
├── contracts/
│   ├── TokenAuditRegistry.sol
│   └── DeployerReputationRegistry.sol
│
├── data/
│   ├── tokens/
│   │   ├── safe_token_1.sol
│   │   ├── rugpull_token_1.sol
│   │   └── suspicious_token_1.sol
│   └── deployers_example.json
│
├── src/
│   ├── token_auditor/
│   │   ├── features.py
│   │   ├── model.py
│   │   └── classify.py
│   │
│   ├── reputation/
│   │   ├── features.py
│   │   ├── model.py
│   │   └── classify.py
│   │
│   ├── etherscan_integration/
│   │   ├── fetcher.py
│   │   └── build_history.py
│   │
│   ├── ml/
│   │   ├── train_deployer_model.py
│   │   └── model_utils.py
│   │
│   ├── cli_token.py
│   ├── cli_deployer.py
│   └── cli_fetch_and_score.py
│
├── artifacts/
│   └── deployer_model.joblib   # created after ML training
│
├── requirements.txt
└── README.md
```

---

## Installation & Setup

```bash
# 1. Clone repo
git clone https://github.com/AmirhosseinHonardoust/onchain-security-suite.git
cd onchain-security-suite

# 2. Create virtual environment (recommended)
python -m venv .venv
.\.venv\Scripts\activate   # on Windows

# 3. Install dependencies
pip install -r requirements.txt
```

Dependencies include:

* `requests`, for Etherscan V2 API
* `scikit-learn`, for ML model
* `joblib`, for saving/loading models

---

## Token Risk Auditor (Static Analyzer)

### Goal

Analyze **a single token contract** (ERC-20–style) and estimate:

* How dangerous its logic is
* Whether it contains classic rugpull mechanics
* A numeric risk score + qualitative label

### Patterns Detected

The token auditor focuses on **structural and semantic red flags**, such as:

1. **Owner Minting**

   ```solidity
   function mint(uint256 amount) public onlyOwner { ... }
   ```

   * Red flag: Owner can unilaterally increase supply → dumping risk.

2. **General Mint Functions**

   ```solidity
   function mint(address to, uint256 amount) external { ... }
   ```

   * Without clear access control, this is dangerous.

3. **Fee Manipulation**

   ```solidity
   function setFee(uint256 _newFee) external onlyOwner { ... }
   ```

   * Allows future tax changes (from 5% to 90% after listing).

4. **Blacklisting / Whitelisting**

   ```solidity
   mapping(address => bool) public isBlacklisted;
   ```

   * Can be used to trap specific users.

5. **Trading Locks**

   ```solidity
   bool public tradingOpen;
   ```

   * If the owner controls this flag, they can freeze trading.

6. **Max Transaction Limits (maxTx)**

   ```solidity
   uint256 public maxTxAmount;
   ```

   * Can be used to prevent selling or force tiny sells only.

These patterns are implemented as regex rules in `token_auditor/features.py`.

### Feature Extraction

Example (simplified):

```python
features = {
    "n_lines": 143.0,
    "n_public": 6.0,
    "n_external": 1.0,
    "has_mint": 1.0,
    "has_owner_mint": 1.0,
    "has_set_fee": 1.0,
    "has_blacklist": 0.0,
    "has_trading_lock": 1.0,
    "has_max_tx": 0.0,
}
```

We capture:

* **Structural features**:

  * `n_lines`: lines of code
  * `n_public`: number of occurrences of `public`
  * `n_external`: number of occurrences of `external`
* **Pattern features**:

  * `has_owner_mint`
  * `has_set_fee`
  * `has_blacklist`
  * `has_trading_lock`
  * `has_max_tx`

### Risk Scoring Logic

The core idea is a **weighted feature sum**:

<img width="170" height="72" alt="Screenshot 2025-11-20 at 13-31-16 Repo style analysis" src="https://github.com/user-attachments/assets/8caa1231-b937-413b-8aa5-1dcf8bf00973" />

Where:

* <img width="21" height="32" alt="Screenshot 2025-11-20 at 13-31-58 Repo style analysis" src="https://github.com/user-attachments/assets/19cc8cbb-b26f-4190-be0f-59a8b8e89277" /> = feature (0 or 1 for patterns, numeric for others)
* <img width="26" height="26" alt="Screenshot 2025-11-20 at 13-32-43 Repo style analysis" src="https://github.com/user-attachments/assets/5a75f4b0-5c76-40a5-83af-4ab983d4b18d" /> = risk weight

Example weighting:

* `has_owner_mint` → +40
* `has_mint` (non-owner) → +20
* `has_set_fee` → +25
* `has_blacklist` → +20
* `has_trading_lock` → +25
* `has_max_tx` → +15
* `n_lines > 800` → +15
* `n_lines > 300` → +8

The final score is clamped to `[0, 100]`.

### Risk Levels

* `0–20` → **Low**, label `safe`
* `21–60` → **Medium**, label `suspicious`
* `61–100` → **High**, label `rugpull_candidate`

So the auditor output looks like:

```json
{
  "file": "rugpull_token_1.sol",
  "features": { ... },
  "risk_score": 100,
  "risk_level": "High",
  "label": "rugpull_candidate"
}
```

### How to Run

```bash
python -m src.cli_token --file data/tokens/rugpull_token_1.sol
```

---

## Deployer Reputation Engine (ML Model)

A **single token** is not the whole story. The deployer might have:

* a history of safe tokens
* a history of multiple rugpulls
* mixed behavior

We aggregate **all tokens they deployed** and compute higher-level features.

### Deployer-Level Features

For each deployer address, we track:

* `n_contracts`, number of known deployed contracts
* `n_safe`, how many were labeled `safe`
* `n_suspicious`
* `n_rugpull`, labeled `rugpull_candidate`
* `frac_safe` = `n_safe / n_contracts`
* `frac_rugpull` = `n_rugpull / n_contracts`

This is produced by:
`src/reputation/features.py`

### Labeling Strategy

For training the initial model, we use a **simple, interpretable rule**:

* If `n_rugpull >= 2` → label `1` (bad deployer)
* Else → label `0` (good/neutral deployer)

This is not “ultimate truth” but an intuitive starting point.

### Model Architecture

We use:

* `RandomForestClassifier`
* `n_estimators = 200`
* `class_weight = "balanced"`

Why RandomForest?

* Handles mixed numeric features well
* Gives feature importances
* Robust to outliers
* Easy to interpret and explain

### From Probability to Risk Categories

The model outputs <img width="137" height="27" alt="Screenshot 2025-11-20 at 13-34-44 Repo style analysis" src="https://github.com/user-attachments/assets/54b2cb60-f7d4-40a3-bc26-18a075821dd4" />

We convert that to a **risk_score** and **label**:

```python
prob_bad = ml_score(features)
risk_score = int(round(prob_bad * 100))
```

Mapping:

* `risk_score <= 25` → `Low`, `trusted`
* `26–60` → `Medium`, `watchlist`
* `61–100` → `High`, `high_risk`

So the final result per deployer is:

```json
{
  "features": { ... },
  "score": 87,
  "risk_class": "High",
  "label": "high_risk"
}
```

---

## Machine Learning Training Pipeline

The training script is:

* `src/ml/train_deployer_model.py`

It does:

1. Load `data/deployers_example.json`
2. Aggregate features per deployer
3. Build `X` (features) and `y` (labels)
4. Train RandomForest
5. Save model to `artifacts/deployer_model.joblib`
6. Print feature importances

### How to Run

```bash
python -m src.ml.train_deployer_model
```

You must do this **once** before using the ML-based deployer reputation, so that `artifacts/deployer_model.joblib` exists.

---

## Etherscan V2 Integration

The Etherscan integration lives in:

* `src/etherscan_integration/fetcher.py`
* `src/etherscan_integration/build_history.py`

It uses the **new Etherscan V2 endpoint**:

```text
https://api.etherscan.io/v2/api
```

with parameters:

* `chainid` (1 for Ethereum mainnet)
* `module`
* `action`
* `address`
* `apikey`

### Fetching Transactions

We use:

```text
module = account
action = txlist
```

This returns all transactions related to an address.
We then filter for those with a `contractAddress` field, these correspond to **contracts that were created** (i.e. deployed).

### Fetching Contract Source Code

For each `contractAddress`, we use:

```text
module = contract
action = getsourcecode
```

If the contract is verified on Etherscan:

* We get a `SourceCode` field with Solidity code
* We pass this into `token_auditor.audit_source()`

If not verified:

* We skip it (no source to analyze)

### Building Deployer History Automatically

The function:

```python
build_history_for_deployer(deployer, api_key)
```

performs:

1. Fetch txs by deployer
2. Filter contract creation txs
3. For each contract:

   * fetch source code
   * run token auditor
   * store `address`, `label`, `risk_score`, `risk_level`

Output structure:

```json
{
  "0xDEPL...": {
    "contracts": [
      {
        "address": "0xCONTRACT1",
        "label": "rugpull_candidate",
        "risk_score": 90,
        "risk_level": "High"
      },
      ...
    ]
  }
}
```

`save_history()` writes this to a JSON file so it can be used by the ML reputation engine.

---

## Solidity Registries

### `TokenAuditRegistry.sol`

This contract stores audits **per token** (by `bytes32 tokenId`, which could be a hash of the token address).

Fields stored:

* `score` (0–100)
* `level` (`Low`, `Medium`, `High`)
* `label` (`"rugpull_candidate"`)
* `detailsJson` (optional, full feature set)
* `auditor` (who submitted the result)
* `timestamp`

It exposes:

* `submitAudit(tokenId, score, level, label, detailsJson)`
* `getAudit(tokenId)`

This enables explorers or DApps to query the **latest audit info** for a token.

---

### `DeployerReputationRegistry.sol`

This contract stores **deployer reputation**:

* `score` (0–100)
* `riskClass` (`Low`, `Medium`, `High`)
* `label` (`trusted`, `watchlist`, etc.)
* `numContracts`
* `lastUpdated`
* `updater` (who wrote the entry)

It exposes:

* `updateReputation(deployer, score, riskClass, label, numContracts)`
* `getReputation(deployer)`

Your Python tooling could be extended to **push** ML-derived scores on-chain.

---

## CLI Tools & Workflows

### 1. Token Auditor CLI

```bash
python -m src.cli_token --file data/tokens/rugpull_token_1.sol
```

Use this when:

* You have a local token contract file
* You want a quick static risk assessment

---

### 2. Deployer Reputation CLI (Offline Dataset)

```bash
python -m src.cli_deployer --data data/deployers_example.json
```

Or, for a single deployer:

```bash
python -m src.cli_deployer --data data/deployers_example.json --deployer 0xDEADDEAD...
```

Use this when:

* You already have a JSON mapping `deployer → contracts + labels`
* You want to test the ML scoring independently of Etherscan

---

### 3. Etherscan Fetch + Score CLI

```bash
python -m src.cli_fetch_and_score --deployer <0xDEPL...> --api_key <YOUR_ETHERSCAN_API_KEY>
```

This does:

1. `[1/2]` Fetch contracts by deployer from Etherscan V2
2. For each verified contract:

   * fetch source
   * run token auditor
   * store result in `data/deployer_<address>.json`
3. `[2/2]` Run ML-based reputation scoring using that JSON
4. Print final score + label for that deployer

---

## End-to-End Example Flow

Full pipeline:

1. **Train ML model** (once):

   ```bash
   python -m src.ml.train_deployer_model
   ```

2. **Audit a local token**:

   ```bash
   python -m src.cli_token --file data/tokens/suspicious_token_1.sol
   ```

3. **Score example deployers (offline data)**:

   ```bash
   python -m src.cli_deployer --data data/deployers_example.json
   ```

4. **Fetch + analyze a real deployer from Etherscan**:

   ```bash
   python -m src.cli_fetch_and_score --deployer 0xYOURDEPLOYER --api_key YOUR_API_KEY
   ```

5. (Optional) **Upload scores to on-chain registry** via Remix / Hardhat scripts.

---

## Assumptions & Limitations

This suite is **powerful**, but not magic. Key limitations:

* **Static Analysis Only**

  * No runtime simulation, no mempool analysis
  * Cannot detect dynamic behavior like:

    * Liquidity removal
    * Price manipulation
    * MEV attacks

* **Heuristic Token Labeling**

  * The token risk model is rule-based
  * Some legitimate contracts might have “dangerous-looking” features (false positives)

* **Synthetic Training Data**

  * Initial ML model uses synthetic / example data
  * For production use, you should:

    * Collect real deployer histories
    * Use ground-truth scam labels

* **Etherscan Constraints**

  * Only works for **verified contracts**
  * Subject to Etherscan rate limits and API key tier

These limitations are explicitly documented so the project is realistic and honest.

---

## Ideas for Extension

Some natural extensions you can build next:

* Use AST-based parsing instead of regex
* Attach SHAP to the RandomForest model for explainable reputation
* Add token similarity clustering (token “families”)
* Integrate CodeBERT/LLM-based code embeddings
* Support multiple chains (BSC, Polygon, Arbitrum, Base) with other explorers
* Build a small web dashboard using FastAPI + React
* Build an on-chain oracle that serves reputation scores to DApps

You can treat this suite as the **core engine** for a future Web3 security product.

---

## Roadmap

* [ ] Multichain explorer integrations
* [ ] More complex ML labeling logic
* [ ] Deployable Docker image
* [ ] Web dashboard visualization
* [ ] Integration with wallets (warn user on high-risk tokens)
* [ ] Batch scanning of new token deployments
* [ ] Automatic push to DeployerReputationRegistry on each score update

---

## License

This project is released under the **MIT License**.
You are free to use it, modify it, and build on top of it.

---

## Contributions

Contributions are welcome. Ideas:

* New risk patterns for the token auditor
* Better ML models or ensembles
* Real-world datasets (scrubbed & anonymized)
* Documentation improvements
* Hardhat deployment scripts
* Visualization tools

Open an issue or PR to discuss changes.

---

## Summary

The **On-Chain Security Suite** demonstrates how to combine:

* Smart-contract understanding
* Pattern-based security
* Machine learning
* Live blockchain data
* On-chain registries

into a cohesive, explainable, and practical Web3 security toolkit.
