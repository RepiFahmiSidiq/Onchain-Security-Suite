from typing import Dict, Any
from .features import load_deployer_history, aggregate_deployer_features
from .model import score_deployer

def score_all(history_path: str) -> Dict[str, Any]:
    history = load_deployer_history(history_path)
    feats = aggregate_deployer_features(history)
    results: Dict[str, Any] = {}
    for deployer, f in feats.items():
        score, risk_class, label = score_deployer(f)
        results[deployer] = {
            "features": f,
            "score": score,
            "risk_class": risk_class,
            "label": label,
        }
    return results

def score_single(history_path: str, deployer: str) -> Dict[str, Any]:
    all_res = score_all(history_path)
    return all_res.get(deployer, {
        "error": "deployer_not_found",
        "score": None,
        "risk_class": None,
        "label": None
    })
