import cv2
import numpy as np


# ==================================================
# REACTION AREA DETECTION
# ==================================================

def _colour_distance_rgb(colour_a, colour_b):
    a = np.array(colour_a, dtype=float)
    b = np.array(colour_b, dtype=float)

    return float(np.linalg.norm(a - b))


def _average_rgb(region):
    if region is None or region.size == 0:
        return None

    average_bgr = np.mean(region, axis=(0, 1))

    return (
        int(round(average_bgr[2])),
        int(round(average_bgr[1])),
        int(round(average_bgr[0])),
    )


def _region_uniformity(region):
    """
    Measures how consistent the colour is inside a region.

    1.0 = very uniform
    0.0 = highly variable
    """

    if region is None or region.size == 0:
        return 0.0

    pixels = region.reshape(-1, 3).astype(np.float32)

    mean = np.mean(pixels, axis=0)
    distances = np.linalg.norm(pixels - mean, axis=1)

    average_distance = float(np.mean(distances))

    uniformity = 1.0 - min(
        average_distance / 100.0,
        1.0
    )

    return round(float(uniformity), 3)


def _rectangle_score(contour):
    """
    Estimate how rectangular a contour is.
    """

    perimeter = cv2.arcLength(contour, True)

    if perimeter <= 0:
        return 0.0

    approximation = cv2.approxPolyDP(
        contour,
        0.04 * perimeter,
        True
    )

    points = len(approximation)

    if points == 4:
        return 1.0

    if points == 5:
        return 0.85

    if points == 6:
        return 0.70

    return 0.45


def _aspect_ratio_score(width, height):
    """
    Reaction/test areas are normally rectangular.
    Accept portrait and landscape orientations.
    """

    if width <= 0 or height <= 0:
        return 0.0

    ratio = max(width / height, height / width)

    if 1.1 <= ratio <= 2.5:
        return 1.0

    if 1.0 <= ratio <= 3.0:
        return 0.75

    if 0.8 <= ratio <= 3.5:
        return 0.50

    return 0.20


def _inside_score(x, y, width, height, image_width, image_height):
    """
    Avoid regions touching the image border.
    """

    margin_x = image_width * 0.03
    margin_y = image_height * 0.03

    if (
        x >= margin_x
        and y >= margin_y
        and x + width <= image_width - margin_x
        and y + height <= image_height - margin_y
    ):
        return 1.0

    return 0.5


def _build_candidate(
    contour,
    image,
    reference_box=None,
    min_area=0
):
    x, y, width, height = cv2.boundingRect(contour)

    area = float(cv2.contourArea(contour))

    if area < min_area:
        return None

    image_height, image_width = image.shape[:2]

    if width < image_width * 0.12:
        return None

    if height < image_height * 0.10:
        return None

    box_area = width * height

    if box_area <= 0:
        return None

    fill_ratio = area / box_area

    if fill_ratio < 0.45:
        return None

    rectangle_score = _rectangle_score(contour)

    aspect_score = _aspect_ratio_score(
        width,
        height
    )

    inside_score = _inside_score(
        x,
        y,
        width,
        height,
        image_width,
        image_height
    )

    region = image[
        y:y + height,
        x:x + width
    ]

    rgb = _average_rgb(region)

    if rgb is None:
        return None

    uniformity = _region_uniformity(region)

    reference_overlap = 0.0

    if reference_box:
        rx = reference_box["x"]
        ry = reference_box["y"]
        rw = reference_box["width"]
        rh = reference_box["height"]

        x_left = max(x, rx)
        y_top = max(y, ry)
        x_right = min(x + width, rx + rw)
        y_bottom = min(y + height, ry + rh)

        overlap_width = max(
            0,
            x_right - x_left
        )

        overlap_height = max(
            0,
            y_bottom - y_top
        )

        overlap_area = (
            overlap_width *
            overlap_height
        )

        reference_overlap = (
            overlap_area /
            max(box_area, 1)
        )

    return {
        "bounding_box": {
            "x": int(x),
            "y": int(y),
            "width": int(width),
            "height": int(height),
        },
        "area": round(area, 2),
        "fill_ratio": round(fill_ratio, 3),
        "rectangle_score": round(rectangle_score, 3),
        "aspect_ratio_score": round(aspect_score, 3),
        "inside_score": round(inside_score, 3),
        "uniformity": round(uniformity, 3),
        "reference_overlap": round(
            reference_overlap,
            3
        ),
        "measured_rgb": {
            "r": rgb[0],
            "g": rgb[1],
            "b": rgb[2],
        },
    }


def _score_candidate(candidate):
    """
    Final reaction-area confidence.

    Reference overlap is deliberately penalized because
    the reference card must not become the reaction area.
    """

    score = (
        candidate["rectangle_score"] * 0.25
        + candidate["aspect_ratio_score"] * 0.20
        + candidate["fill_ratio"] * 0.15
        + candidate["uniformity"] * 0.25
        + candidate["inside_score"] * 0.15
    )

    score -= candidate["reference_overlap"] * 0.60

    return max(
        0.0,
        min(
            1.0,
            score
        )
    )


# ==================================================
# ATTEMPT 1
# ==================================================

def _detect_reaction_attempt_1(
    image,
    reference_box=None
):
    """
    Standard edge/contour based detection.
    """

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    blurred = cv2.GaussianBlur(
        gray,
        (5, 5),
        0
    )

    edges = cv2.Canny(
        blurred,
        50,
        150
    )

    kernel = np.ones(
        (7, 7),
        np.uint8
    )

    edges = cv2.morphologyEx(
        edges,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    image_area = image.shape[0] * image.shape[1]

    candidates = []

    for contour in contours:

        candidate = _build_candidate(
            contour,
            image,
            reference_box=reference_box,
            min_area=image_area * 0.03
        )

        if candidate is None:
            continue

        candidate["score"] = round(
            _score_candidate(candidate),
            3
        )

        candidates.append(candidate)

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return candidates


# ==================================================
# ATTEMPT 2
# ==================================================

def _detect_reaction_attempt_2(
    image,
    reference_box=None
):
    """
    More tolerant HSV/brightness segmentation.

    Useful when the reaction area has weak edges.
    """

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    mask = cv2.inRange(
        saturation,
        15,
        245
    )

    bright_mask = cv2.inRange(
        value,
        40,
        250
    )

    mask = cv2.bitwise_and(
        mask,
        bright_mask
    )

    kernel = np.ones(
        (11, 11),
        np.uint8
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    image_area = image.shape[0] * image.shape[1]

    candidates = []

    for contour in contours:

        candidate = _build_candidate(
            contour,
            image,
            reference_box=reference_box,
            min_area=image_area * 0.04
        )

        if candidate is None:
            continue

        candidate["score"] = round(
            _score_candidate(candidate),
            3
        )

        candidates.append(candidate)

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return candidates


# ==================================================
# ATTEMPT 3
# ==================================================

def _detect_reaction_attempt_3(
    image,
    reference_box=None
):
    """
    Strong fallback.

    Searches large connected regions and evaluates
    internal colour consistency and geometry.
    """

    blurred = cv2.GaussianBlur(
        image,
        (9, 9),
        0
    )

    gray = cv2.cvtColor(
        blurred,
        cv2.COLOR_BGR2GRAY
    )

    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        51,
        5
    )

    threshold = cv2.bitwise_not(
        threshold
    )

    kernel = np.ones(
        (13, 13),
        np.uint8
    )

    threshold = cv2.morphologyEx(
        threshold,
        cv2.MORPH_CLOSE,
        kernel
    )

    contours, _ = cv2.findContours(
        threshold,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    image_area = image.shape[0] * image.shape[1]

    candidates = []

    for contour in contours:

        candidate = _build_candidate(
            contour,
            image,
            reference_box=reference_box,
            min_area=image_area * 0.05
        )

        if candidate is None:
            continue

        candidate["score"] = round(
            _score_candidate(candidate),
            3
        )

        candidates.append(candidate)

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return candidates


# ==================================================
# FINAL REACTION DETECTOR
# ==================================================

def detect_reaction_area(
    image,
    reference_box=None
):
    """
    Three-stage reaction-area detector.

    A candidate is accepted only when confidence
    reaches the required threshold.

    The detector does NOT alter the image.
    """

    attempts = [
        _detect_reaction_attempt_1(
            image,
            reference_box
        ),
        _detect_reaction_attempt_2(
            image,
            reference_box
        ),
        _detect_reaction_attempt_3(
            image,
            reference_box
        ),
    ]

    confidence_threshold = 0.62

    for attempt_number, candidates in enumerate(
        attempts,
        start=1
    ):

        if not candidates:
            continue

        best = candidates[0]

        # Do not accept a region that overlaps
        # substantially with the reference card.
        if best["reference_overlap"] > 0.35:
            continue

        if best["score"] < confidence_threshold:
            continue

        return {
            "success": True,
            "attempt": attempt_number,
            "message": (
                "Reaction area successfully detected."
            ),
            "reaction_area": {
                "bounding_box": best["bounding_box"],
                "area": best["area"],
                "confidence": best["score"],
                "uniformity": best["uniformity"],
                "measured_rgb": best["measured_rgb"],
            },
            "candidates": candidates[:5],
        }

    return {
        "success": False,
        "attempt": 3,
        "message": (
            "Reaction area could not be reliably "
            "detected after three detection attempts."
        ),
        "candidates": [
            candidate
            for candidates in attempts
            for candidate in candidates[:3]
        ][:9],
    }


# ==================================================
# REACTION COLOUR EXTRACTION
# ==================================================

def extract_reaction_colour(
    image,
    reaction_box
):
    """
    Extract the reaction colour from the detected
    reaction area.

    Uses an inner region rather than the complete
    bounding box so borders/background are excluded.
    """

    x = reaction_box["x"]
    y = reaction_box["y"]
    width = reaction_box["width"]
    height = reaction_box["height"]

    margin_x = max(
        2,
        int(width * 0.12)
    )

    margin_y = max(
        2,
        int(height * 0.12)
    )

    x1 = max(
        0,
        x + margin_x
    )

    y1 = max(
        0,
        y + margin_y
    )

    x2 = min(
        image.shape[1],
        x + width - margin_x
    )

    y2 = min(
        image.shape[0],
        y + height - margin_y
    )

    region = image[
        y1:y2,
        x1:x2
    ]

    if region.size == 0:
        return None

    # Remove extreme pixels caused by highlights,
    # glare and dark borders.
    pixels = region.reshape(
        -1,
        3
    ).astype(np.float32)

    median_bgr = np.median(
        pixels,
        axis=0
    )

    distances = np.linalg.norm(
        pixels - median_bgr,
        axis=1
    )

    keep = distances <= np.percentile(
        distances,
        80
    )

    if np.sum(keep) < 10:
        return None

    filtered = pixels[keep]

    average_bgr = np.mean(
        filtered,
        axis=0
    )

    return {
        "r": int(round(average_bgr[2])),
        "g": int(round(average_bgr[1])),
        "b": int(round(average_bgr[0])),
    }