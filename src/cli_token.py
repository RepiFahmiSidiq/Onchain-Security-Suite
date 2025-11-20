import argparse, json
from src.token_auditor.classify import audit_token

def main():
    p = argparse.ArgumentParser(description="Token Risk Auditor CLI")
    p.add_argument("--file", required=True, help="Path to Solidity token contract")
    args = p.parse_args()

    result = audit_token(args.file)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
