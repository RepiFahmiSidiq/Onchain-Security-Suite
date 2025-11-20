from typing import Dict, Tuple

def score_token(features: Dict[str, float]) -> Tuple[int, str, str]:
    score = 0

    if features.get("has_owner_mint", 0) >= 1:
        score += 40
    elif features.get("has_mint", 0) >= 1:
        score += 20

    if features.get("has_set_fee", 0) >= 1:
        score += 25
    if features.get("has_blacklist", 0) >= 1:
        score += 20
    if features.get("has_trading_lock", 0) >= 1:
        score += 25
    if features.get("has_max_tx", 0) >= 1:
        score += 15

    n_lines = features.get("n_lines", 0)
    if n_lines > 800:
        score += 15
    elif n_lines > 300:
        score += 8

    score = max(0, min(100, score))

    if score <= 20:
        level, label = "Low", "safe"
    elif score <= 60:
        level, label = "Medium", "suspicious"
    else:
        level, label = "High", "rugpull_candidate"

    return int(score), level, label
