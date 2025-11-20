import json
from pathlib import Path
from typing import Dict, Any

def load_deployer_history(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def aggregate_deployer_features(history: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
    results: Dict[str, Dict[str, float]] = {}

    for deployer, info in history.items():
        contracts = info.get("contracts", [])
        n_contracts = len(contracts)
        n_safe = sum(1 for c in contracts if c.get("label") == "safe")
        n_suspicious = sum(1 for c in contracts if c.get("label") == "suspicious")
        n_rugpull = sum(1 for c in contracts if c.get("label") == "rugpull_candidate")

        frac_safe = n_safe / n_contracts if n_contracts > 0 else 0.0
        frac_rugpull = n_rugpull / n_contracts if n_contracts > 0 else 0.0

        results[deployer] = {
            "n_contracts": float(n_contracts),
            "n_safe": float(n_safe),
            "n_suspicious": float(n_suspicious),
            "n_rugpull": float(n_rugpull),
            "frac_safe": float(frac_safe),
            "frac_rugpull": float(frac_rugpull),
        }

    return results
