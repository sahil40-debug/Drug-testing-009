from typing import Literal, Optional
from pydantic import BaseModel


class ImageQualityResult(BaseModel):
    overall: Literal["acceptable", "poor"]
    sharpness: float
    brightness: Optional[float] = None
    exposure: Optional[str] = None
    glare_detected: Optional[bool] = None
    shadows_detected: Optional[bool] = None
    message: str


class ReferenceCardResult(BaseModel):
    detected: bool
    calibration_status: Literal["not_started", "success", "failed"]
    message: str


class TestAnalysisResult(BaseModel):
    success: bool
    test_id: str

    image_quality: ImageQualityResult
    reference_card: ReferenceCardResult

    classification: Optional[
        Literal["positive", "negative", "inconclusive"]
    ] = None

    classification_reason: Optional[str] = Nonefrom typing import Literal, Optional
from pydantic import BaseModel


class ImageCheck(BaseModel):
    passed: bool


class ResolutionCheck(ImageCheck):
    width: int
    height: int


class SharpnessCheck(ImageCheck):
    score: float


class BrightnessCheck(ImageCheck):
    score: float


class ExposureCheck(ImageCheck):
    underexposed_percentage: float
    overexposed_percentage: float


class ImageQualityResult(BaseModel):
    overall: Literal["acceptable", "poor"]
    message: str

    resolution: ResolutionCheck
    sharpness: SharpnessCheck
    brightness: BrightnessCheck
    exposure: ExposureCheck


class ReferenceCardResult(BaseModel):
    detected: bool
    calibration_status: Literal[
        "not_started",
        "success",
        "failed"
    ]
    message: str


class TestAnalysisResult(BaseModel):
    success: bool
    test_id: str

    image_quality: ImageQualityResult

    reference_card: ReferenceCardResult

    classification: Optional[
        Literal[
            "positive",
            "negative",
            "inconclusive"
        ]
    ] = None

    classification_reason: Optional[str] = None