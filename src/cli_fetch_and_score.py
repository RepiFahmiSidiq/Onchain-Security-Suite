import argparse
import json
from pathlib import Path

from src.etherscan_integration.build_history import save_history
from src.reputation.classify import score_all

def main():
    p = argparse.ArgumentParser(description="Fetch deployer history from Etherscan, then score reputation.")
    p.add_argument("--deployer", required=True, help="Deployer address")
    p.add_argument("--api_key", required=True, help="Etherscan API key")
    p.add_argument("--out", default=None, help="Output JSON path (optional)")
    args = p.parse_args()

    out_path = args.out or f"data/deployer_{args.deployer}.json"
    Path("data").mkdir(exist_ok=True)

    print(f"[1/2] Fetching and classifying contracts for deployer {args.deployer}...")
    save_history(args.deployer, args.api_key, out_path)

    print(f"[2/2] Scoring deployer reputation from {out_path}...")
    scores = score_all(out_path)
    print(json.dumps(scores.get(args.deployer, {}), indent=2))

if __name__ == "__main__":
    main()
