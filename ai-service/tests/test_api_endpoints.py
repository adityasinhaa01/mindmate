import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.anyio
async def test_health_check_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["ml_model_loaded"] is True


@pytest.mark.anyio
async def test_compute_stress_endpoint_valid_integers():
    payload = {
        "sleep": 7.5,
        "study": 6.0,
        "screen": 4.5,
        "exam": 14,
        "mood": "okay",
        "note": "Feeling slightly tired",
        "nervousness": 1,
        "unable_to_control": 1,
        "worry": 1,
        "trouble_in_relaxation": 2,
        "restlessness": 1,
        "irritability": 1,
        "fear": 1,
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/wellness/compute-stress", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert 0 <= data["score"] <= 100
    assert data["level"] in ["Low", "Moderate", "High"]
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0

    # Verify ML Prediction Details
    assert "mlPrediction" in data
    ml_pred = data["mlPrediction"]
    assert ml_pred["predicted_class"] in [
        "No Stress",
        "Mild Stress",
        "Moderate Stress",
        "Severe Stress",
    ]
    assert 0.0 <= ml_pred["confidence_score"] <= 1.0
    assert "probabilities" in ml_pred
    assert 0.0 <= ml_pred["raw_regression_score"] <= 3.0


@pytest.mark.anyio
async def test_compute_stress_endpoint_valid_string_labels_and_aliases():
    # Test camelCase aliases and string symptom labels
    payload = {
        "sleep": 5.0,
        "study": 8.0,
        "screen": 6.0,
        "exam": 2,
        "mood": "stressed",
        "note": "Finals are tomorrow",
        "nervousness": "Severe",
        "unableToControl": "Severe",
        "worry": "Severe",
        "troubleInRelaxation": "Severe",
        "restlessness": "Severe",
        "irritability": "Severe",
        "fear": "Severe",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/wellness/compute-stress", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["level"] == "High"
    assert data["mlPrediction"]["predicted_class"] == "Severe Stress"
    assert data["score"] >= 65


@pytest.mark.anyio
async def test_compute_stress_endpoint_missing_clinical_feature():
    payload = {
        "sleep": 7.0,
        "study": 5.0,
        "screen": 4.0,
        "exam": 10,
        "nervousness": 1,
        # Missing other 6 GAD-7 features
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/wellness/compute-stress", json=payload)

    assert response.status_code == 422  # Unprocessable Entity
    detail = response.json()["detail"]
    assert any("unable_to_control" in str(err) or "unableToControl" in str(err) for err in detail)


@pytest.mark.anyio
async def test_compute_stress_endpoint_invalid_values():
    payload = {
        "sleep": 7.0,
        "study": 5.0,
        "screen": 4.0,
        "exam": 10,
        "nervousness": 99,  # Invalid: must be 0-3
        "unable_to_control": 0,
        "worry": 0,
        "trouble_in_relaxation": 0,
        "restlessness": 0,
        "irritability": 0,
        "fear": 0,
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/wellness/compute-stress", json=payload)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_compute_stress_endpoint_invalid_sleep_hours():
    payload = {
        "sleep": 35.0,  # Invalid: cannot exceed 24 hours
        "study": 5.0,
        "screen": 4.0,
        "exam": 10,
        "nervousness": 1,
        "unable_to_control": 0,
        "worry": 0,
        "trouble_in_relaxation": 0,
        "restlessness": 0,
        "irritability": 0,
        "fear": 0,
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/wellness/compute-stress", json=payload)

    assert response.status_code == 422

