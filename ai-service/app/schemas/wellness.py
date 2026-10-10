from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any, Union

GAD7_STR_MAPPING = {
    "no": 0,
    "mild": 1,
    "moderate": 2,
    "severe": 3,
}


def parse_gad7_value(v: Any, field_name: str) -> int:
    if isinstance(v, str):
        cleaned = v.strip().lower()
        if cleaned in GAD7_STR_MAPPING:
            return GAD7_STR_MAPPING[cleaned]
        try:
            v = int(cleaned)
        except ValueError:
            raise ValueError(
                f"Field '{field_name}' must be one of [0, 1, 2, 3] or ['No', 'Mild', 'Moderate', 'Severe'], got '{v}'"
            )
    if isinstance(v, (int, float)):
        int_v = int(v)
        if int_v != v or int_v < 0 or int_v > 3:
            raise ValueError(f"Field '{field_name}' must be an integer between 0 and 3, got '{v}'")
        return int_v
    raise ValueError(f"Field '{field_name}' must be an integer (0-3) or string ('No', 'Mild', 'Moderate', 'Severe')")


class StressComputeRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # Academic & daily lifestyle habits (used for recommendations, visuals, and companion context)
    sleep: float = Field(..., ge=0, le=24, description="Sleep duration in hours (0-24)")
    study: float = Field(..., ge=0, le=24, description="Study duration in hours (0-24)")
    screen: float = Field(..., ge=0, le=24, description="Screen exposure in hours (0-24)")
    exam: int = Field(..., ge=0, description="Days until next exam")
    mood: Optional[str] = "okay"
    note: Optional[str] = ""

    # Clinical GAD-7 psychological questionnaire features required for ML model inference
    nervousness: Union[int, str] = Field(..., description="Feeling nervous, anxious, or on edge (0: No, 1: Mild, 2: Moderate, 3: Severe)")
    unable_to_control: Union[int, str] = Field(..., alias="unableToControl", description="Unable to stop or control worrying (0-3)")
    worry: Union[int, str] = Field(..., description="Worrying too much about different things (0-3)")
    trouble_in_relaxation: Union[int, str] = Field(..., alias="troubleInRelaxation", description="Trouble in relaxation (0-3)")
    restlessness: Union[int, str] = Field(..., description="Hard to sit still / restlessness (0-3)")
    irritability: Union[int, str] = Field(..., description="Becoming easily annoyed or irritable (0-3)")
    fear: Union[int, str] = Field(..., description="Feeling afraid as if something awful might happen (0-3)")

    @field_validator(
        "nervousness",
        "unable_to_control",
        "worry",
        "trouble_in_relaxation",
        "restlessness",
        "irritability",
        "fear",
        mode="before",
    )
    @classmethod
    def validate_gad7_field(cls, v: Any, info) -> int:
        return parse_gad7_value(v, info.field_name)


class MLPredictionDetails(BaseModel):
    predicted_class: str = Field(..., description="Random Forest Classifier predicted tier (No Stress, Mild Stress, Moderate Stress, Severe Stress)")
    confidence_score: float = Field(..., description="Maximum class probability from RFC")
    probabilities: Dict[str, float] = Field(..., description="Probability distribution across all 4 stress tiers")
    top_contributor: Optional[str] = Field(None, description="Primary clinical GAD-7 symptom driving the prediction")
    raw_regression_score: float = Field(..., description="Continuous regression severity index (0.0 to 3.0)")


class RecommendationItem(BaseModel):
    id: str
    title: str
    blurb: str
    mins: int
    secs: int
    tint: str


class StressComputeResponse(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Normalized continuous 0-100 severity index from ML regressor")
    level: str = Field(..., description="Stress classification category ('Low', 'Moderate', 'High')")
    recommendations: List[RecommendationItem] = Field(..., description="Personalized coping exercises")
    mlPrediction: Optional[MLPredictionDetails] = Field(None, description="Detailed ML model inference metrics")