from typing import Dict, Tuple
from src.ml.model_utils import ml_score

def score_deployer(features: Dict[str, float]) -> Tuple[int, str, str]:
    prob_bad = ml_score(features)  # probability that deployer is 'bad'
    risk_score = int(round(prob_bad * 100))

    if risk_score <= 25:
        return risk_score, "Low", "trusted"
    elif risk_score <= 60:
        return risk_score, "Medium", "watchlist"
    else:
        return risk_score, "High", "high_risk"
