import cv2
import numpy as np
import base64


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


def analyze_image_quality(image_data: str):

    img = decode_image(image_data)

    if img is None:
        return {
            "success": False,
            "quality": "poor",
            "quality_score": 0,
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
    # Quality score
    # ----------------------------------------------
    # These are initial weights.
    # We will calibrate them later using real images.

    resolution_score = 20 if resolution_ok else 0
    sharpness_score = 30 if sharpness_ok else 0
    brightness_quality_score = 20 if brightness_ok else 0
    exposure_score = 30 if exposure_ok else 0

    quality_score = (
        resolution_score
        + sharpness_score
        + brightness_quality_score
        + exposure_score
    )

    # ----------------------------------------------
    # Overall quality
    # ----------------------------------------------

    if quality_score >= 80:
        quality = "good"
    elif quality_score >= 60:
        quality = "acceptable"
    else:
        quality = "poor"

    # ----------------------------------------------
    # User message
    # ----------------------------------------------

    if quality == "good":

        message = (
            "Image quality is good and suitable "
            "for further analysis."
        )

    elif quality == "acceptable":

        message = (
            "Image quality is acceptable, but "
            "improvement may increase reliability."
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
        "quality_score": quality_score,
        "message": message,

        "checks": {
            "resolution": {
                "passed": resolution_ok,
                "score": resolution_score,
                "width": width,
                "height": height,
            },

            "sharpness": {
                "passed": sharpness_ok,
                "score": round(blur_score, 1),
                "quality_points": sharpness_score,
            },

            "brightness": {
                "passed": brightness_ok,
                "score": round(brightness_score, 1),
                "quality_points": brightness_quality_score,
            },

            "exposure": {
                "passed": exposure_ok,
                "underexposed_percentage": round(
                    underexposed_pixels * 100, 1
                ),
                "overexposed_percentage": round(
                    overexposed_pixels * 100, 1
                ),
                "quality_points": exposure_score,
            },
        },
    }