import joblib
from typing import Dict

MODEL_PATH = "artifacts/deployer_model.joblib"

def ml_score(features: Dict[str, float]) -> float:
    clf = joblib.load(MODEL_PATH)
    vec = [[
        features["n_contracts"],
        features["n_safe"],
        features["n_suspicious"],
        features["n_rugpull"],
        features["frac_safe"],
        features["frac_rugpull"],
    ]]
    prob_bad = clf.predict_proba(vec)[0][1]
    return float(prob_bad)
