import json
import time
from pathlib import Path
from typing import Any, Dict

from .fetcher import get_contracts_by_deployer, get_contract_source
from src.token_auditor.classify import audit_source


def build_history_for_deployer(deployer: str, api_key: str) -> Dict[str, Any]:
    txs = get_contracts_by_deployer(deployer, api_key)
    contracts = []

    if not txs:
        # No contracts deployed by this address
        return {deployer: {"contracts": []}}

    for tx in txs:
        addr = tx.get("contractAddress")
        if not addr:
            continue

        source = get_contract_source(addr, api_key)
        if not source:
            # Source not verified / unavailable → skip
            continue

        audit = audit_source(source, name=addr)
        label = audit["label"]

        contracts.append({
            "address": addr,
            "label": label,
            "risk_score": audit["risk_score"],
            "risk_level": audit["risk_level"],
        })

        time.sleep(0.25)  # basic rate-limiting

    return {deployer: {"contracts": contracts}}


def save_history(deployer: str, api_key: str, out_path: str) -> None:
    history = build_history_for_deployer(deployer, api_key)
    Path(out_path).write_text(json.dumps(history, indent=2), encoding="utf-8")
