import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

from src.reputation.features import load_deployer_history, aggregate_deployer_features

ARTIFACT_PATH = Path("artifacts/deployer_model.joblib")

def load_dataset(json_path: str):
    history = load_deployer_history(json_path)
    feats = aggregate_deployer_features(history)

    X = []
    y = []

    for deployer, f in feats.items():
        vec = [
            f["n_contracts"],
            f["n_safe"],
            f["n_suspicious"],
            f["n_rugpull"],
            f["frac_safe"],
            f["frac_rugpull"],
        ]
        X.append(vec)
        label = 1 if f["n_rugpull"] >= 2 else 0
        y.append(label)

    return np.array(X), np.array(y)

def train(json_path: str = "data/deployers_example.json"):
    X, y = load_dataset(json_path)

    clf = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42
    )
    clf.fit(X, y)

    ARTIFACT_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(clf, ARTIFACT_PATH)

    print(f"Model trained and saved → {ARTIFACT_PATH}")
    print("Feature importances:")
    for i, imp in enumerate(clf.feature_importances_):
        print(f"  f{i}: {imp:.4f}")

if __name__ == "__main__":
    train()
