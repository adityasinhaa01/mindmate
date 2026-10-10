"""
MindMate ML Stress Inference Engine
Performs production inference using trained Random Forest Classifier,
Random Forest Regressor, and StandardScaler trained on 16,384 student records.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

FEATURE_COLS: List[str] = [
    "Nervousness",
    "Unable to control",
    "Worry",
    "Trouble in Relaxation",
    "Restlessness",
    "Irritability",
    "Fear",
]

CLASS_LABELS: List[str] = [
    "No Stress",
    "Mild Stress",
    "Moderate Stress",
    "Severe Stress",
]

# Clinical 4-tier model mapping to application 3-tier categorization
CLASS_TO_LEVEL: Dict[str, str] = {
    "No Stress": "Low",
    "Mild Stress": "Low",
    "Moderate Stress": "Moderate",
    "Severe Stress": "High",
}

RECS: List[Dict[str, Any]] = [
    {
        "id": "breath",
        "title": "2-minute breathing exercise",
        "blurb": "Slow, even breaths settle your nervous system and clear your head.",
        "mins": 2,
        "secs": 120,
        "tint": "blue",
    },
    {
        "id": "walk",
        "title": "Take a 10-minute walk",
        "blurb": "Fresh air and movement lift your mood. Leave your phone in your pocket.",
        "mins": 10,
        "secs": 600,
        "tint": "green",
    },
    {
        "id": "screen",
        "title": "Take a screen break",
        "blurb": "Look away, stretch and rest your eyes. Try the 20-20-20 rule.",
        "mins": 5,
        "secs": 300,
        "tint": "lav",
    },
    {
        "id": "sleep",
        "title": "Improve your sleep routine",
        "blurb": "Wind down with dim lights and no scrolling for the last half hour.",
        "mins": 15,
        "secs": 900,
        "tint": "blue",
    },
    {
        "id": "focus",
        "title": "Try a focused study session",
        "blurb": "25 minutes on one topic, then a real break. Small blocks beat marathons.",
        "mins": 25,
        "secs": 1500,
        "tint": "green",
    },
]


def get_recommendations(
    sleep: float, study: float, screen: float
) -> List[Dict[str, Any]]:
    weights = {
        "breath": 2,
        "walk": 1,
        "screen": 4 if screen > 5.0 else 0,
        "sleep": 4 if sleep < 7.0 else 0,
        "focus": 0 if study > 7.0 else 1,
    }
    sorted_recs = sorted(RECS, key=lambda r: weights.get(r["id"], 0), reverse=True)
    return sorted_recs


class StressModelEngine:
    """
    Cached ML inference engine. Loads artifacts once at startup relative
    to the service root and executes preprocessing and inference.
    """

    def __init__(self, models_dir: Optional[Path] = None):
        if models_dir is None:
            # Resolve relative to this service: ai-service/models
            service_root = Path(__file__).resolve().parent.parent.parent
            models_dir = service_root / "models"

        self.models_dir = Path(models_dir)
        self.scaler = None
        self.classifier = None
        self.regressor = None
        self.metrics = None
        self.is_loaded = False
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        scaler_path = self.models_dir / "student_stress_scaler.joblib"
        clf_path = self.models_dir / "student_stress_rfc.joblib"
        reg_path = self.models_dir / "student_stress_regressor.joblib"
        metrics_path = self.models_dir / "model_metrics.json"

        missing = []
        for path in [scaler_path, clf_path, reg_path]:
            if not path.is_file():
                missing.append(str(path))

        if missing:
            raise FileNotFoundError(
                f"[StressModelEngine] Missing required model artifact(s): {', '.join(missing)}"
            )

        try:
            self.scaler = joblib.load(scaler_path)
            self.classifier = joblib.load(clf_path)
            self.regressor = joblib.load(reg_path)
        except Exception as e:
            raise RuntimeError(
                f"[StressModelEngine] Failed to deserialize model artifacts from {self.models_dir}: {e}"
            ) from e

        if metrics_path.is_file():
            try:
                with open(metrics_path, "r", encoding="utf-8") as f:
                    self.metrics = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load model metrics JSON: {e}")

        self.is_loaded = True
        logger.info("[StressModelEngine] Successfully loaded scaler, classifier, and regressor.")

    def predict(self, feature_dict: Dict[str, int]) -> Dict[str, Any]:
        """
        Executes genuine ML inference.
        Applies exact preprocessing:
        1. Formulates input row matching FEATURE_COLS order.
        2. Applies StandardScaler.transform.
        3. Executes RandomForestClassifier and RandomForestRegressor inference.
        """
        if not self.is_loaded:
            raise RuntimeError("[StressModelEngine] Model engine is not initialized.")

        raw_values: List[int] = []
        for col in FEATURE_COLS:
            val = feature_dict.get(col)
            if val is None:
                raise ValueError(f"Missing required clinical assessment feature: '{col}'")
            if not isinstance(val, (int, float, np.integer)) or val < 0 or val > 3:
                raise ValueError(
                    f"Feature '{col}' must be an integer between 0 and 3, got: {val}"
                )
            raw_values.append(int(val))

        input_df = pd.DataFrame([raw_values], columns=FEATURE_COLS)
        scaled_features = self.scaler.transform(input_df)

        # 1. Classification
        class_idx = int(self.classifier.predict(scaled_features)[0])
        probabilities = self.classifier.predict_proba(scaled_features)[0]
        predicted_class = CLASS_LABELS[class_idx]
        confidence = float(np.max(probabilities))
        prob_dict = {
            CLASS_LABELS[i]: round(float(prob), 4)
            for i, prob in enumerate(probabilities)
        }

        # 2. Regression
        reg_pred = float(self.regressor.predict(scaled_features)[0])
        bounded_reg = max(0.0, min(3.0, reg_pred))
        # Continuous 0-100 score representation derived from continuous regression severity
        score_100 = int(round((bounded_reg / 3.0) * 100))

        # 3. Categorical Level
        level = CLASS_TO_LEVEL.get(predicted_class, "Moderate")

        # 4. Primary Contributing Factor
        top_driver: Optional[str] = None
        feature_importances = getattr(self.classifier, "feature_importances_", None)
        if feature_importances is not None and len(feature_importances) == len(FEATURE_COLS):
            impacts = [raw_values[i] * feature_importances[i] for i in range(len(FEATURE_COLS))]
            max_idx = int(np.argmax(impacts))
            if raw_values[max_idx] > 0:
                top_driver = FEATURE_COLS[max_idx]

        return {
            "score": score_100,
            "level": level,
            "mlPrediction": {
                "predicted_class": predicted_class,
                "confidence_score": round(confidence, 4),
                "probabilities": prob_dict,
                "top_contributor": top_driver,
                "raw_regression_score": round(bounded_reg, 4),
            },
        }


# Singleton engine instance
_engine_instance: Optional[StressModelEngine] = None


def get_stress_engine(models_dir: Optional[Path] = None) -> StressModelEngine:
    global _engine_instance
    if _engine_instance is None or not _engine_instance.is_loaded:
        _engine_instance = StressModelEngine(models_dir=models_dir)
    return _engine_instance
