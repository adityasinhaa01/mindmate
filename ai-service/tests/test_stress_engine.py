import os
from pathlib import Path
import pytest
import numpy as np
import pandas as pd
from app.services.stress_engine import (
    StressModelEngine,
    get_stress_engine,
    FEATURE_COLS,
    CLASS_LABELS,
    CLASS_TO_LEVEL,
)


def test_model_loading_and_attributes():
    engine = get_stress_engine()
    assert engine.is_loaded is True
    assert engine.scaler is not None
    assert engine.classifier is not None
    assert engine.regressor is not None

    # Scaler verification
    assert engine.scaler.n_features_in_ == 7
    assert list(engine.scaler.feature_names_in_) == FEATURE_COLS
    assert len(engine.scaler.mean_) == 7

    # Classifier verification
    assert list(engine.classifier.classes_) == [0, 1, 2, 3]
    assert engine.classifier.n_features_in_ == 7
    assert len(engine.classifier.feature_importances_) == 7

    # Regressor verification
    assert engine.regressor.n_features_in_ == 7


def test_feature_ordering_and_scaling():
    engine = get_stress_engine()
    # Check exact feature ordering
    expected_order = [
        "Nervousness",
        "Unable to control",
        "Worry",
        "Trouble in Relaxation",
        "Restlessness",
        "Irritability",
        "Fear",
    ]
    assert FEATURE_COLS == expected_order

    # Check scaling of mean values (1.5 for uniform 0..3) using DataFrame with feature names
    mean_df = pd.DataFrame([[1.5] * 7], columns=FEATURE_COLS)
    scaled = engine.scaler.transform(mean_df)
    # Scaled mean should be approximately zero
    np.testing.assert_allclose(scaled, np.zeros((1, 7)), atol=1e-5)


def test_prediction_no_stress():
    engine = get_stress_engine()
    input_data = {
        "Nervousness": 0,
        "Unable to control": 0,
        "Worry": 0,
        "Trouble in Relaxation": 0,
        "Restlessness": 0,
        "Irritability": 0,
        "Fear": 0,
    }
    result = engine.predict(input_data)
    assert result["score"] >= 0 and result["score"] <= 35
    assert result["level"] == "Low"
    assert result["mlPrediction"]["predicted_class"] == "No Stress"
    assert result["mlPrediction"]["confidence_score"] > 0.8
    assert result["mlPrediction"]["raw_regression_score"] < 0.5
    assert result["mlPrediction"]["top_contributor"] is None  # all zero symptoms


def test_prediction_severe_stress():
    engine = get_stress_engine()
    input_data = {
        "Nervousness": 3,
        "Unable to control": 3,
        "Worry": 3,
        "Trouble in Relaxation": 3,
        "Restlessness": 3,
        "Irritability": 3,
        "Fear": 3,
    }
    result = engine.predict(input_data)
    assert result["score"] >= 65
    assert result["level"] == "High"
    assert result["mlPrediction"]["predicted_class"] == "Severe Stress"
    assert result["mlPrediction"]["confidence_score"] > 0.8
    assert result["mlPrediction"]["raw_regression_score"] > 2.5
    assert result["mlPrediction"]["top_contributor"] in FEATURE_COLS


def test_prediction_moderate_stress():
    engine = get_stress_engine()
    input_data = {
        "Nervousness": 2,
        "Unable to control": 1,
        "Worry": 2,
        "Trouble in Relaxation": 1,
        "Restlessness": 2,
        "Irritability": 1,
        "Fear": 2,
    }
    result = engine.predict(input_data)
    assert result["mlPrediction"]["predicted_class"] == "Moderate Stress"
    assert result["level"] == "Moderate"
    assert 35 <= result["score"] <= 75
    assert result["mlPrediction"]["top_contributor"] in FEATURE_COLS
    # Verify probability distribution sums to 1.0
    prob_sum = sum(result["mlPrediction"]["probabilities"].values())
    assert abs(prob_sum - 1.0) < 0.01


def test_missing_required_features_raises_error():
    engine = get_stress_engine()
    incomplete_data = {
        "Nervousness": 1,
        "Worry": 2,
        # Missing other 5 features
    }
    with pytest.raises(ValueError) as excinfo:
        engine.predict(incomplete_data)
    assert "Missing required clinical assessment feature" in str(excinfo.value)


def test_invalid_feature_values_raises_error():
    engine = get_stress_engine()
    invalid_data = {
        "Nervousness": 99,  # out of 0..3 range
        "Unable to control": 0,
        "Worry": 0,
        "Trouble in Relaxation": 0,
        "Restlessness": 0,
        "Irritability": 0,
        "Fear": 0,
    }
    with pytest.raises(ValueError) as excinfo:
        engine.predict(invalid_data)
    assert "must be an integer between 0 and 3" in str(excinfo.value)

    negative_data = {
        "Nervousness": -1,
        "Unable to control": 0,
        "Worry": 0,
        "Trouble in Relaxation": 0,
        "Restlessness": 0,
        "Irritability": 0,
        "Fear": 0,
    }
    with pytest.raises(ValueError) as excinfo:
        engine.predict(negative_data)
    assert "must be an integer between 0 and 3" in str(excinfo.value)


def test_missing_model_artifacts_raises_filenotfound(tmp_path):
    empty_dir = tmp_path / "non_existent_models"
    empty_dir.mkdir()
    with pytest.raises(FileNotFoundError) as excinfo:
        StressModelEngine(models_dir=empty_dir)
    assert "Missing required model artifact(s)" in str(excinfo.value)

