from fastapi import APIRouter, HTTPException, status
from app.schemas.wellness import StressComputeRequest, StressComputeResponse
from app.services.stress_engine import get_stress_engine, get_recommendations

router = APIRouter(prefix="/wellness", tags=["Wellness"])


@router.post("/compute-stress", response_model=StressComputeResponse)
def compute_stress(payload: StressComputeRequest):
    try:
        engine = get_stress_engine()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Machine learning inference engine is not ready: {str(e)}",
        )

    # Feature dictionary corresponding to exact training names and order
    feature_dict = {
        "Nervousness": payload.nervousness,
        "Unable to control": payload.unable_to_control,
        "Worry": payload.worry,
        "Trouble in Relaxation": payload.trouble_in_relaxation,
        "Restlessness": payload.restlessness,
        "Irritability": payload.irritability,
        "Fear": payload.fear,
    }

    try:
        result = engine.predict(feature_dict)
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(ve),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ML inference error: {str(e)}",
        )

    recs = get_recommendations(sleep=payload.sleep, study=payload.study, screen=payload.screen)

    return StressComputeResponse(
        score=result["score"],
        level=result["level"],
        recommendations=recs,
        mlPrediction=result["mlPrediction"],
    )