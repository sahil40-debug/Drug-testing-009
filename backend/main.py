import cv2
import numpy as np
import base64

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class ImagePayload(BaseModel):
    image_data: str


# --------------------------------------------------
# Decode Base64 image
# --------------------------------------------------

def decode_image(image_data: str):
    try:
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]

        img_bytes = base64.b64decode(image_data)

        np_arr = np.frombuffer(img_bytes, np.uint8)

        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        return img

    except Exception:
        return None


# --------------------------------------------------
# Image quality analysis
# --------------------------------------------------

def analyze_image_quality(image_data: str):

    img = decode_image(image_data)

    if img is None:
        return {
            "success": False,
            "quality": "poor",
            "message": "Could not read image file.",
        }

    # ----------------------------------------------
    # Resolution
    # ----------------------------------------------

    height, width = img.shape[:2]

    minimum_width = 640
    minimum_height = 480

    resolution_ok = bool(
        width >= minimum_width and
        height >= minimum_height
    )

    # ----------------------------------------------
    # Sharpness
    # ----------------------------------------------

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur_score = cv2.Laplacian(
        gray,
        cv2.CV_64F
    ).var()

    sharpness_ok = bool(blur_score >= 100.0)

    # ----------------------------------------------
    # Brightness
    # ----------------------------------------------

    brightness_score = float(np.mean(gray))

    brightness_ok = bool(
        40 <= brightness_score <= 220
    )

    # ----------------------------------------------
    # Exposure
    # ----------------------------------------------

    underexposed_pixels = np.mean(gray < 30)
    overexposed_pixels = np.mean(gray > 245)

    exposure_ok = bool(
        underexposed_pixels < 0.25 and
        overexposed_pixels < 0.25
    )

    # ----------------------------------------------
    # Overall quality
    # ----------------------------------------------

    checks = {
        "resolution": resolution_ok,
        "sharpness": sharpness_ok,
        "brightness": brightness_ok,
        "exposure": exposure_ok,
    }

    passed_checks = sum(checks.values())

    quality = "acceptable" if passed_checks == 4 else "poor"

    # ----------------------------------------------
    # User message
    # ----------------------------------------------

    if quality == "acceptable":

        message = (
            "Image quality is good and suitable "
            "for further analysis."
        )

    else:

        problems = []

        if not resolution_ok:
            problems.append("resolution")

        if not sharpness_ok:
            problems.append("sharpness")

        if not brightness_ok:
            problems.append("brightness")

        if not exposure_ok:
            problems.append("exposure")

        message = (
            "Image quality needs improvement. "
            "Check: " + ", ".join(problems) + "."
        )

    # ----------------------------------------------
    # Response
    # ----------------------------------------------

    return {
        "success": True,
        "quality": quality,
        "message": message,

        "checks": {
            "resolution": {
                "passed": resolution_ok,
                "width": width,
                "height": height,
            },

            "sharpness": {
                "passed": sharpness_ok,
                "score": round(blur_score, 1),
            },

            "brightness": {
                "passed": brightness_ok,
                "score": round(brightness_score, 1),
            },

            "exposure": {
                "passed": exposure_ok,
                "underexposed_percentage": round(
                    underexposed_pixels * 100, 1
                ),
                "overexposed_percentage": round(
                    overexposed_pixels * 100, 1
                ),
            },
        },
    }


# --------------------------------------------------
# Analyze endpoint
# --------------------------------------------------

@app.post("/api/analyze")
def analyze_image(payload: ImagePayload):

    return analyze_image_quality(
        payload.image_data
    )