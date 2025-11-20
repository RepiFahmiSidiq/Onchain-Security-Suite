from pathlib import Path
from typing import Dict, Any

from .features import read_source, extract_token_features
from .model import score_token

def audit_token(path: str) -> Dict[str, Any]:
    p = Path(path)
    source = read_source(str(p))
    return audit_source(source, str(p))

def audit_source(source: str, name: str = "<memory>") -> Dict[str, Any]:
    feats = extract_token_features(source)
    score, level, label = score_token(feats)
    return {
        "file": name,
        "features": feats,
        "risk_score": score,
        "risk_level": level,
        "label": label
    }
