import base64

import cv2
import numpy as np

from .classification import classify_reaction
from .reaction_analysis import (
    detect_reaction_area,
    extract_reaction_colour,
)


# ============================================================
# IMAGE DECODING
# ============================================================

def decode_image(image_data: str):
    """Convert a Base64 image string into an OpenCV image."""

    try:
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]

        image_bytes = base64.b64decode(image_data)

        np_array = np.frombuffer(
            image_bytes,
            np.uint8,
        )

        image = cv2.imdecode(
            np_array,
            cv2.IMREAD_COLOR,
        )

        return image

    except Exception:
        return None


# ============================================================
# REFERENCE COLOUR CONVERSION
# ============================================================

def hex_to_rgb(hex_value: str):
    """Convert HEX colour to RGB."""

    hex_value = hex_value.strip().lstrip("#")

    if len(hex_value) != 6:
        return None

    try:
        return (
            int(hex_value[0:2], 16),
            int(hex_value[2:4], 16),
            int(hex_value[4:6], 16),
        )

    except ValueError:
        return None


# ============================================================
# RGB → HSV
# ============================================================

def rgb_to_hsv(red: int, green: int, blue: int):
    """Convert RGB values to OpenCV HSV."""

    pixel = np.uint8(
        [[[red, green, blue]]]
    )

    hsv_pixel = cv2.cvtColor(
        pixel,
        cv2.COLOR_RGB2HSV,
    )

    hue, saturation, value = hsv_pixel[0][0]

    return {
        "h": int(hue),
        "s": int(saturation),
        "v": int(value),
    }


# ============================================================
# SAMPLE CENTRE COLOUR
# ============================================================

def sample_centre_colour(image):
    """
    Prototype centre-colour sampling.

    Kept as a separate helper for compatibility.
    The main pipeline uses reaction-area detection instead.
    """

    height, width = image.shape[:2]

    sample_size = min(
        width,
        height,
    ) // 8

    center_x = width // 2
    center_y = height // 2

    x1 = max(
        0,
        center_x - sample_size,
    )

    x2 = min(
        width,
        center_x + sample_size,
    )

    y1 = max(
        0,
        center_y - sample_size,
    )

    y2 = min(
        height,
        center_y + sample_size,
    )

    region = image[y1:y2, x1:x2]

    if region.size == 0:
        return None

    average_bgr = np.mean(
        region,
        axis=(0, 1),
    )

    return {
        "r": int(average_bgr[2]),
        "g": int(average_bgr[1]),
        "b": int(average_bgr[0]),
    }


# ============================================================
# COLOUR DISTANCE
# ============================================================

def calculate_colour_distance(
    image_rgb,
    reference_rgb,
):
    """Calculate Euclidean RGB colour distance."""

    image_vector = np.array(
        image_rgb,
        dtype=float,
    )

    reference_vector = np.array(
        reference_rgb,
        dtype=float,
    )

    distance = np.linalg.norm(
        image_vector - reference_vector,
    )

    return round(
        float(distance),
        2,
    )


# ============================================================
# RGB CALIBRATION
# ============================================================

def calculate_rgb_calibration(
    expected_rgb,
    measured_rgb,
):
    """Calculate per-channel RGB correction factors."""

    expected = np.array(
        expected_rgb,
        dtype=float,
    )

    measured = np.array(
        measured_rgb,
        dtype=float,
    )

    measured = np.maximum(
        measured,
        1.0,
    )

    correction = expected / measured

    return {
        "r": round(float(correction[0]), 4),
        "g": round(float(correction[1]), 4),
        "b": round(float(correction[2]), 4),
    }


# ============================================================
# APPLY RGB CALIBRATION
# ============================================================

def apply_rgb_calibration(
    image_rgb,
    calibration,
):
    """Apply RGB calibration factors."""

    image = np.array(
        image_rgb,
        dtype=float,
    )

    correction = np.array(
        [
            calibration["r"],
            calibration["g"],
            calibration["b"],
        ],
        dtype=float,
    )

    calibrated = image * correction

    calibrated = np.clip(
        calibrated,
        0,
        255,
    )

    return {
        "r": int(round(calibrated[0])),
        "g": int(round(calibrated[1])),
        "b": int(round(calibrated[2])),
    }


# ============================================================
# CALIBRATED COLOUR ANALYSIS
# ============================================================

def analyze_calibrated_colour(
    reaction_rgb,
    expected_reference_rgb,
    measured_reference_rgb,
):
    """Calibrate reaction colour using the measured reference."""

    calibration = calculate_rgb_calibration(
        expected_reference_rgb,
        measured_reference_rgb,
    )

    calibrated_reaction = apply_rgb_calibration(
        reaction_rgb,
        calibration,
    )

    calibrated_hsv = rgb_to_hsv(
        calibrated_reaction["r"],
        calibrated_reaction["g"],
        calibrated_reaction["b"],
    )

    expected_reference_hsv = rgb_to_hsv(
        expected_reference_rgb[0],
        expected_reference_rgb[1],
        expected_reference_rgb[2],
    )

    calibrated_distance = calculate_colour_distance(
        (
            calibrated_reaction["r"],
            calibrated_reaction["g"],
            calibrated_reaction["b"],
        ),
        expected_reference_rgb,
    )

    return {
        "calibration": {
            "expected_reference_rgb": {
                "r": expected_reference_rgb[0],
                "g": expected_reference_rgb[1],
                "b": expected_reference_rgb[2],
            },
            "measured_reference_rgb": {
                "r": measured_reference_rgb[0],
                "g": measured_reference_rgb[1],
                "b": measured_reference_rgb[2],
            },
            "correction_factors": calibration,
        },

        "reaction": {
            "original_rgb": {
                "r": reaction_rgb[0],
                "g": reaction_rgb[1],
                "b": reaction_rgb[2],
            },
            "calibrated_rgb": calibrated_reaction,
            "calibrated_hsv": calibrated_hsv,
        },

        "comparison": {
            "reference_hsv": expected_reference_hsv,
            "calibrated_rgb_distance": calibrated_distance,
        },
    }


# ============================================================
# REFERENCE-CARD GEOMETRY
# ============================================================

def calculate_shape_score(
    contour,
    width,
    height,
    area,
):
    """Calculate how closely a contour resembles a card."""

    if area <= 0 or width <= 0 or height <= 0:
        return 0.0

    contour_area = cv2.contourArea(contour)

    rectangle_area = float(
        width * height
    )

    if rectangle_area <= 0:
        return 0.0

    rectangularity = contour_area / rectangle_area

    rectangularity = min(
        max(rectangularity, 0.0),
        1.0,
    )

    aspect_ratio = width / float(height)

    if 1.20 <= aspect_ratio <= 1.80:
        aspect_score = 1.0
    elif 1.05 <= aspect_ratio <= 2.00:
        aspect_score = 0.70
    else:
        aspect_score = 0.0

    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)

    if hull_area > 0:
        solidity = contour_area / hull_area
    else:
        solidity = 0.0

    solidity = min(
        max(solidity, 0.0),
        1.0,
    )

    score = (
        rectangularity * 0.45
        + aspect_score * 0.25
        + solidity * 0.30
    )

    return round(
        float(score),
        3,
    )


# ============================================================
# REFERENCE INNER COLOUR SAMPLING
# ============================================================

def sample_reference_region(
    image,
    x,
    y,
    width,
    height,
):
    """Sample only the inner part of a reference candidate."""

    if image is None:
        return None

    image_height, image_width = image.shape[:2]

    margin_x = max(
        int(width * 0.15),
        2,
    )

    margin_y = max(
        int(height * 0.15),
        2,
    )

    x1 = max(
        x + margin_x,
        0,
    )

    y1 = max(
        y + margin_y,
        0,
    )

    x2 = min(
        x + width - margin_x,
        image_width,
    )

    y2 = min(
        y + height - margin_y,
        image_height,
    )

    if x2 <= x1 or y2 <= y1:
        return None

    region = image[
        y1:y2,
        x1:x2,
    ]

    if region.size == 0:
        return None

    region_rgb = cv2.cvtColor(
        region,
        cv2.COLOR_BGR2RGB,
    )

    pixels = region_rgb.reshape(
        -1,
        3,
    ).astype(np.float32)

    if len(pixels) == 0:
        return None

    median_rgb = np.median(
        pixels,
        axis=0,
    )

    measured_rgb = (
        int(round(median_rgb[0])),
        int(round(median_rgb[1])),
        int(round(median_rgb[2])),
    )

    centre = np.mean(
        pixels,
        axis=0,
    )

    pixel_distances = np.linalg.norm(
        pixels - centre,
        axis=1,
    )

    spread = float(
        np.std(pixel_distances)
    )

    consistency = 1.0 - min(
        spread / 40.0,
        1.0,
    )

    return {
        "rgb": measured_rgb,
        "colour_consistency": round(
            float(consistency),
            3,
        ),
    }


# ============================================================
# REFERENCE COLOUR SCORE
# ============================================================

def calculate_reference_colour_score(
    measured_rgb,
    expected_rgb,
):
    """Convert RGB distance into similarity."""

    distance = calculate_colour_distance(
        measured_rgb,
        expected_rgb,
    )

    score = 1.0 - (
        distance / 180.0
    )

    score = min(
        max(score, 0.0),
        1.0,
    )

    return (
        round(float(score), 3),
        distance,
    )


# ============================================================
# REFERENCE SIZE SCORE
# ============================================================

def calculate_reference_size_score(
    area_ratio,
):
    """Calculate candidate size suitability."""

    if area_ratio < 0.05:
        return 0.0

    if 0.05 <= area_ratio <= 0.35:
        return 1.0

    if area_ratio <= 0.50:
        return 0.65

    return 0.30


# ============================================================
# REFERENCE DETECTION — ATTEMPT 1
# ============================================================

def _attempt_one_colour_shape(
    image,
    expected_rgb,
):
    """Attempt 1: colour + rectangular geometry + size."""

    image_height, image_width = image.shape[:2]

    image_area = float(
        image_width * image_height
    )

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV,
    )

    expected_pixel = np.uint8(
        [[[
            expected_rgb[0],
            expected_rgb[1],
            expected_rgb[2],
        ]]]
    )

    expected_hsv = cv2.cvtColor(
        expected_pixel,
        cv2.COLOR_RGB2HSV,
    )[0][0]

    expected_hue = int(expected_hsv[0])
    expected_saturation = int(expected_hsv[1])
    expected_value = int(expected_hsv[2])

    hue_tolerance = 12

    saturation_tolerance = max(
        45,
        int(expected_saturation * 0.35),
    )

    value_tolerance = max(
        50,
        int(expected_value * 0.30),
    )

    lower_h = max(
        0,
        expected_hue - hue_tolerance,
    )

    upper_h = min(
        179,
        expected_hue + hue_tolerance,
    )

    lower_s = max(
        0,
        expected_saturation - saturation_tolerance,
    )

    upper_s = min(
        255,
        expected_saturation + saturation_tolerance,
    )

    lower_v = max(
        0,
        expected_value - value_tolerance,
    )

    upper_v = min(
        255,
        expected_value + value_tolerance,
    )

    mask = cv2.inRange(
        hsv,
        np.array(
            [lower_h, lower_s, lower_v],
            dtype=np.uint8,
        ),
        np.array(
            [upper_h, upper_s, upper_v],
            dtype=np.uint8,
        ),
    )

    kernel = np.ones(
        (5, 5),
        np.uint8,
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel,
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel,
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    candidates = []

    for contour in contours:

        area = cv2.contourArea(contour)

        if area <= 0:
            continue

        x, y, width, height = cv2.boundingRect(
            contour
        )

        if width <= 0 or height <= 0:
            continue

        area_ratio = area / image_area

        if area_ratio < 0.05:
            continue

        shape_score = calculate_shape_score(
            contour,
            width,
            height,
            area,
        )

        if shape_score < 0.95:
            continue

        sample = sample_reference_region(
            image,
            x,
            y,
            width,
            height,
        )

        if sample is None:
            continue

        measured_rgb = sample["rgb"]
        colour_consistency = sample[
            "colour_consistency"
        ]

        colour_score, colour_distance = (
            calculate_reference_colour_score(
                measured_rgb,
                expected_rgb,
            )
        )

        if colour_distance > 45:
            continue

        if colour_consistency < 0.90:
            continue

        size_score = calculate_reference_size_score(
            area_ratio
        )

        if size_score <= 0:
            continue

        final_score = (
            colour_score * 0.35
            + shape_score * 0.25
            + colour_consistency * 0.25
            + size_score * 0.15
        )

        candidates.append({
            "area": round(float(area), 2),
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height),
            "aspect_ratio": round(
                width / float(height),
                3,
            ),
            "measured_rgb": {
                "r": measured_rgb[0],
                "g": measured_rgb[1],
                "b": measured_rgb[2],
            },
            "colour_distance": round(
                float(colour_distance),
                2,
            ),
            "colour_score": colour_score,
            "shape_score": shape_score,
            "colour_consistency": colour_consistency,
            "size_score": round(
                float(size_score),
                3,
            ),
            "final_score": round(
                float(final_score),
                3,
            ),
        })

    candidates.sort(
        key=lambda item: item["final_score"],
        reverse=True,
    )

    if not candidates:
        return None, []

    best = candidates[0]

    if best["final_score"] < 0.82:
        return None, candidates

    return best, candidates


# ============================================================
# REFERENCE DETECTION — BOUNDARY SCORE
# ============================================================

def _calculate_boundary_score(
    image,
    x,
    y,
    width,
    height,
):
    """Check for a meaningful boundary around the candidate."""

    image_height, image_width = image.shape[:2]

    if width < 20 or height < 20:
        return 0.0

    margin = 4

    x1 = max(0, x)
    y1 = max(0, y)

    x2 = min(
        image_width,
        x + width,
    )

    y2 = min(
        image_height,
        y + height,
    )

    if x2 <= x1 or y2 <= y1:
        return 0.0

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY,
    )

    inside_values = []
    outside_values = []

    if y1 - margin >= 0:

        inside = gray[
            y1:y1 + margin,
            x1:x2,
        ]

        outside = gray[
            y1 - margin:y1,
            x1:x2,
        ]

        if inside.size and outside.size:
            inside_values.append(
                float(np.mean(inside))
            )

            outside_values.append(
                float(np.mean(outside))
            )

    if y2 + margin <= image_height:

        inside = gray[
            y2 - margin:y2,
            x1:x2,
        ]

        outside = gray[
            y2:y2 + margin,
            x1:x2,
        ]

        if inside.size and outside.size:
            inside_values.append(
                float(np.mean(inside))
            )

            outside_values.append(
                float(np.mean(outside))
            )

    if x1 - margin >= 0:

        inside = gray[
            y1:y2,
            x1:x1 + margin,
        ]

        outside = gray[
            y1:y2,
            x1 - margin:x1,
        ]

        if inside.size and outside.size:
            inside_values.append(
                float(np.mean(inside))
            )

            outside_values.append(
                float(np.mean(outside))
            )

    if x2 + margin <= image_width:

        inside = gray[
            y1:y2,
            x2 - margin:x2,
        ]

        outside = gray[
            y1:y2,
            x2:x2 + margin,
        ]

        if inside.size and outside.size:
            inside_values.append(
                float(np.mean(inside))
            )

            outside_values.append(
                float(np.mean(outside))
            )

    if not inside_values:
        return 0.0

    differences = [
        abs(a - b)
        for a, b in zip(
            inside_values,
            outside_values,
        )
    ]

    average_difference = float(
        np.mean(differences)
    )

    score = min(
        average_difference / 40.0,
        1.0,
    )

    return round(
        float(score),
        3,
    )


# ============================================================
# REFERENCE DETECTION — ATTEMPT 2
# ============================================================

def _attempt_two_boundary(
    image,
    candidates,
):
    """Attempt 2: add independent boundary evidence."""

    if not candidates:
        return None, []

    verified = []

    for candidate in candidates:

        boundary_score = _calculate_boundary_score(
            image,
            candidate["x"],
            candidate["y"],
            candidate["width"],
            candidate["height"],
        )

        score = (
            candidate["final_score"] * 0.70
            + boundary_score * 0.30
        )

        updated = dict(candidate)

        updated["boundary_score"] = boundary_score

        updated["attempt_2_score"] = round(
            float(score),
            3,
        )

        verified.append(updated)

    verified.sort(
        key=lambda item: item["attempt_2_score"],
        reverse=True,
    )

    best = verified[0]

    if (
        best["attempt_2_score"] >= 0.84
        and best["boundary_score"] >= 0.20
    ):
        return best, verified

    return None, verified


# ============================================================
# REFERENCE DETECTION — ATTEMPT 3
# ============================================================

def _multi_region_consistency(
    image,
    x,
    y,
    width,
    height,
    expected_rgb,
):
    """Check colour consistency across multiple card regions."""

    if width < 30 or height < 30:
        return 0.0, None

    margin_x = int(width * 0.20)
    margin_y = int(height * 0.20)

    x1 = x + margin_x
    x2 = x + width - margin_x

    y1 = y + margin_y
    y2 = y + height - margin_y

    if x2 <= x1 or y2 <= y1:
        return 0.0, None

    half_width = (x2 - x1) // 2
    half_height = (y2 - y1) // 2

    points = [
        (
            x1,
            y1,
            x1 + half_width,
            y1 + half_height,
        ),
        (
            x1 + half_width,
            y1,
            x2,
            y1 + half_height,
        ),
        (
            x1,
            y1 + half_height,
            x1 + half_width,
            y2,
        ),
        (
            x1 + half_width,
            y1 + half_height,
            x2,
            y2,
        ),
        (
            x1,
            y1,
            x2,
            y2,
        ),
    ]

    measurements = []

    for px1, py1, px2, py2 in points:

        region = image[
            py1:py2,
            px1:px2,
        ]

        if region.size == 0:
            continue

        region_rgb = cv2.cvtColor(
            region,
            cv2.COLOR_BGR2RGB,
        )

        median = np.median(
            region_rgb.reshape(-1, 3),
            axis=0,
        )

        rgb = (
            int(round(median[0])),
            int(round(median[1])),
            int(round(median[2])),
        )

        distance = calculate_colour_distance(
            rgb,
            expected_rgb,
        )

        measurements.append({
            "rgb": rgb,
            "distance": distance,
        })

    if len(measurements) < 4:
        return 0.0, measurements

    distances = [
        item["distance"]
        for item in measurements
    ]

    mean_distance = float(
        np.mean(distances)
    )

    spread = float(
        np.std(distances)
    )

    distance_score = max(
        0.0,
        1.0 - mean_distance / 60.0,
    )

    spread_score = max(
        0.0,
        1.0 - spread / 30.0,
    )

    consistency = (
        distance_score * 0.60
        + spread_score * 0.40
    )

    return (
        round(float(consistency), 3),
        measurements,
    )


def _attempt_three_verification(
    image,
    candidates,
    expected_rgb,
):
    """Attempt 3: final multi-region verification."""

    if not candidates:
        return None, []

    verified = []

    for candidate in candidates:

        consistency, measurements = (
            _multi_region_consistency(
                image,
                candidate["x"],
                candidate["y"],
                candidate["width"],
                candidate["height"],
                expected_rgb,
            )
        )

        boundary_score = candidate.get(
            "boundary_score",
            0.0,
        )

        score = (
            candidate.get(
                "attempt_2_score",
                candidate["final_score"],
            ) * 0.45
            + consistency * 0.35
            + boundary_score * 0.20
        )

        updated = dict(candidate)

        updated["multi_region_consistency"] = consistency

        updated["multi_region_samples"] = measurements

        updated["final_verification_score"] = round(
            float(score),
            3,
        )

        verified.append(updated)

    verified.sort(
        key=lambda item: item[
            "final_verification_score"
        ],
        reverse=True,
    )

    best = verified[0]

    if (
        best["final_verification_score"] >= 0.84
        and best["multi_region_consistency"] >= 0.78
        and best.get("boundary_score", 0.0) >= 0.20
    ):
        return best, verified

    return None, verified


# ============================================================
# PUBLIC REFERENCE-CARD DETECTOR
# ============================================================

def detect_reference_card(
    image,
    expected_rgb,
):
    """
    Three-stage reference-card verification.

    Stage 1:
        Colour + shape + size.

    Stage 2:
        Stage 1 + boundary evidence.

    Stage 3:
        Stage 2 + multi-region consistency.

    The reference card is accepted only after
    the verification pipeline succeeds.
    """

    if image is None:
        return {
            "success": False,
            "attempt": 0,
            "message": "Invalid image.",
        }

    if not expected_rgb:
        return {
            "success": False,
            "attempt": 0,
            "message": "Expected reference colour is required.",
        }

    if len(expected_rgb) != 3:
        return {
            "success": False,
            "attempt": 0,
            "message": "Reference RGB must contain three values.",
        }

    # --------------------------------------------------------
    # ATTEMPT 1
    # --------------------------------------------------------

    best_1, candidates_1 = _attempt_one_colour_shape(
        image,
        expected_rgb,
    )

    if best_1 is None:
        return {
            "success": False,
            "attempt": 1,
            "message": (
                "Reference card was not confidently detected "
                "during Attempt 1."
            ),
            "candidates": candidates_1,
        }

    # --------------------------------------------------------
    # ATTEMPT 2
    # --------------------------------------------------------

    best_2, candidates_2 = _attempt_two_boundary(
        image,
        candidates_1,
    )

    if best_2 is None:
        return {
            "success": False,
            "attempt": 2,
            "message": (
                "Attempt 1 found a candidate, but boundary "
                "verification was insufficient."
            ),
            "candidates": candidates_2,
        }

    # --------------------------------------------------------
    # ATTEMPT 3
    # --------------------------------------------------------

    best_3, candidates_3 = _attempt_three_verification(
        image,
        candidates_2,
        expected_rgb,
    )

    if best_3 is None:
        return {
            "success": False,
            "attempt": 3,
            "message": (
                "Candidate passed earlier checks but failed "
                "final multi-region verification."
            ),
            "candidates": candidates_3,
        }

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    return {
        "success": True,
        "attempt": 3,
        "message": (
            "Reference card successfully verified "
            "after three-stage detection."
        ),
        "reference_card": {
            "bounding_box": {
                "x": best_3["x"],
                "y": best_3["y"],
                "width": best_3["width"],
                "height": best_3["height"],
            },
            "area": best_3["area"],
            "measured_rgb": best_3["measured_rgb"],
            "colour_distance": best_3["colour_distance"],
            "confidence": best_3[
                "final_verification_score"
            ],
            "boundary_score": best_3[
                "boundary_score"
            ],
            "multi_region_consistency": best_3[
                "multi_region_consistency"
            ],
        },
        "candidates": candidates_3,
    }


# ============================================================
# MAIN COLOUR ANALYSIS PIPELINE
# ============================================================

def analyze_colour(
    image_data: str,
    reference_color: str | None,
    reference_shade: str | None,
    reference_color_value: str | None,
):
    """
    Complete colour-analysis pipeline.

    image
        ↓
    reference validation
        ↓
    reference-card detection
        ↓
    reference measurement
        ↓
    reaction-area detection
        ↓
    reaction colour extraction
        ↓
    RGB calibration
        ↓
    deterministic classification
    """

    # --------------------------------------------------------
    # 1. DECODE IMAGE
    # --------------------------------------------------------

    image = decode_image(image_data)

    if image is None:
        return {
            "success": False,
            "stage": "image_decode",
            "message": "Could not read image.",
        }

    # --------------------------------------------------------
    # 2. VALIDATE REFERENCE COLOUR
    # --------------------------------------------------------

    if not reference_color_value:
        return {
            "success": False,
            "stage": "reference_validation",
            "message": (
                "Reference colour shade is required "
                "for colour analysis."
            ),
        }

    reference_rgb = hex_to_rgb(
        reference_color_value
    )

    if reference_rgb is None:
        return {
            "success": False,
            "stage": "reference_validation",
            "message": "Invalid reference colour value.",
        }

    # --------------------------------------------------------
    # 3. REFERENCE HSV
    # --------------------------------------------------------

    reference_hsv = rgb_to_hsv(
        reference_rgb[0],
        reference_rgb[1],
        reference_rgb[2],
    )

    # --------------------------------------------------------
    # 4. REFERENCE CARD DETECTION
    # --------------------------------------------------------

    reference_detection = detect_reference_card(
        image=image,
        expected_rgb=reference_rgb,
    )

    if not reference_detection.get(
        "success",
        False,
    ):
        return {
            "success": False,
            "stage": "reference_detection",
            "message": (
                "Reference card could not be reliably "
                "detected after all detection attempts."
            ),
            "reference_detection": reference_detection,
        }

    # --------------------------------------------------------
    # 5. GET DETECTED REFERENCE
    # --------------------------------------------------------

    detected_reference = (
        reference_detection.get(
            "reference_card"
        )
    )

    if not detected_reference:
        return {
            "success": False,
            "stage": "reference_measurement",
            "message": (
                "Reference card was detected but "
                "its details are unavailable."
            ),
            "reference_detection": reference_detection,
        }

    measured_reference_rgb = (
        detected_reference.get(
            "measured_rgb"
        )
    )

    if not measured_reference_rgb:
        return {
            "success": False,
            "stage": "reference_measurement",
            "message": (
                "Measured reference colour "
                "is unavailable."
            ),
            "reference_detection": reference_detection,
        }

    reference_box = detected_reference.get(
        "bounding_box"
    )

    if not reference_box:
        return {
            "success": False,
            "stage": "reference_detection",
            "message": (
                "Reference card was detected but "
                "its bounding box is unavailable."
            ),
            "reference_detection": reference_detection,
        }

    # --------------------------------------------------------
    # 6. REACTION AREA DETECTION
    # --------------------------------------------------------

    reaction_detection = detect_reaction_area(
        image=image,
        reference_box=reference_box,
    )

    if not reaction_detection.get(
        "success",
        False,
    ):
        return {
            "success": False,
            "stage": "reaction_detection",
            "message": (
                "Reaction area could not be reliably "
                "detected after all detection attempts."
            ),
            "reference_detection": reference_detection,
            "reaction_detection": reaction_detection,
        }

    # IMPORTANT:
    # detect_reaction_area() returns:
    #
    # reaction_detection
    #     └── reaction_area
    #           ├── bounding_box
    #           ├── confidence
    #           └── uniformity

    reaction_area = reaction_detection.get(
        "reaction_area"
    )

    if not reaction_area:
        return {
            "success": False,
            "stage": "reaction_detection",
            "message": (
                "Reaction area was detected but "
                "its details are unavailable."
            ),
            "reference_detection": reference_detection,
            "reaction_detection": reaction_detection,
        }

    reaction_box = reaction_area.get(
        "bounding_box"
    )

    if not reaction_box:
        return {
            "success": False,
            "stage": "reaction_detection",
            "message": (
                "Reaction area was detected but "
                "its bounding box is unavailable."
            ),
            "reference_detection": reference_detection,
            "reaction_detection": reaction_detection,
        }

    # --------------------------------------------------------
    # 7. EXTRACT REACTION COLOUR
    # --------------------------------------------------------

    reaction_rgb = extract_reaction_colour(
        image,
        reaction_box,
    )

    if reaction_rgb is None:
        return {
            "success": False,
            "stage": "reaction_measurement",
            "message": (
                "Unable to measure the reaction colour."
            ),
            "reference_detection": reference_detection,
            "reaction_detection": reaction_detection,
        }

    # --------------------------------------------------------
    # 8. CALIBRATE REACTION COLOUR
    # --------------------------------------------------------

    calibrated_result = analyze_calibrated_colour(
        reaction_rgb=(
            reaction_rgb["r"],
            reaction_rgb["g"],
            reaction_rgb["b"],
        ),
        expected_reference_rgb=reference_rgb,
        measured_reference_rgb=(
            measured_reference_rgb["r"],
            measured_reference_rgb["g"],
            measured_reference_rgb["b"],
        ),
    )

    calibrated_reaction = calibrated_result[
        "reaction"
    ]

    calibrated_hsv = calibrated_reaction[
        "calibrated_hsv"
    ]

    comparison = calibrated_result[
        "comparison"
    ]

    calibrated_distance = comparison[
        "calibrated_rgb_distance"
    ]

    # --------------------------------------------------------
    # 9. CLASSIFICATION
    # --------------------------------------------------------

    classification = classify_reaction(
        calibrated_rgb_distance=calibrated_distance,
        reaction_hsv=calibrated_hsv,
        reference_hsv=reference_hsv,

        # CORRECT DATA PATH:
        # confidence and uniformity live inside
        # reaction_area, not reaction_detection.
        reaction_confidence=reaction_area.get(
            "confidence",
            0.0,
        ),
        reaction_uniformity=reaction_area.get(
            "uniformity",
            0.0,
        ),
    )

    # --------------------------------------------------------
    # 10. FINAL STRUCTURED RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,

        "stage": "classification",

        "reference": {
            "group": reference_color,
            "shade": reference_shade,
            "hex": reference_color_value,

            "expected_rgb": {
                "r": reference_rgb[0],
                "g": reference_rgb[1],
                "b": reference_rgb[2],
            },

            "expected_hsv": reference_hsv,

            "measured_rgb": {
                "r": measured_reference_rgb["r"],
                "g": measured_reference_rgb["g"],
                "b": measured_reference_rgb["b"],
            },
        },

        "reference_detection": {
            "attempt": reference_detection.get(
                "attempt"
            ),

            "confidence": detected_reference.get(
                "confidence"
            ),

            "bounding_box": reference_box,

            "boundary_score": detected_reference.get(
                "boundary_score"
            ),

            "multi_region_consistency": (
                detected_reference.get(
                    "multi_region_consistency"
                )
            ),
        },

        "reaction_detection": {
            "attempt": reaction_detection.get(
                "attempt"
            ),

            # CORRECT PATH
            "confidence": reaction_area.get(
                "confidence"
            ),

            "bounding_box": reaction_box,

            # CORRECT PATH
            "uniformity": reaction_area.get(
                "uniformity"
            ),
        },

        "reaction": {
            "original_rgb": calibrated_reaction[
                "original_rgb"
            ],

            "original_hsv": rgb_to_hsv(
                reaction_rgb["r"],
                reaction_rgb["g"],
                reaction_rgb["b"],
            ),

            "original_rgb_distance": (
                calculate_colour_distance(
                    (
                        reaction_rgb["r"],
                        reaction_rgb["g"],
                        reaction_rgb["b"],
                    ),
                    reference_rgb,
                )
            ),

            "calibrated_rgb": calibrated_reaction[
                "calibrated_rgb"
            ],

            "calibrated_hsv": calibrated_hsv,

            "calibrated_rgb_distance": (
                calibrated_distance
            ),
        },

        "calibration": calibrated_result[
            "calibration"
        ],

        "classification": classification,

        "message": (
            "Reference card, reaction area, colour "
            "calibration, and deterministic "
            "classification completed successfully."
        ),
    }