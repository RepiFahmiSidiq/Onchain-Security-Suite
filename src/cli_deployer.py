import argparse, json
from src.reputation.classify import score_all, score_single

def main():
    p = argparse.ArgumentParser(description="Deployer Reputation CLI")
    p.add_argument("--data", required=True, help="Path to deployer history JSON")
    p.add_argument("--deployer", help="Optional single deployer address")
    args = p.parse_args()

    if args.deployer:
        result = score_single(args.data, args.deployer)
        print(json.dumps(result, indent=2))
    else:
        result = score_all(args.data)
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
