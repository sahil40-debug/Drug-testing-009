import math


# ==================================================
# CLASSIFICATION THRESHOLDS
# ==================================================

# These are prototype thresholds.
# They will be tuned using synthetic and real test images.
#
# Lower distance = reaction colour is closer to
# the selected reference colour.
#
# HSV saturation is also considered because a reaction
# may change colour intensity without changing hue much.

POSITIVE_DISTANCE = 45.0
NEGATIVE_DISTANCE = 25.0

POSITIVE_HUE_TOLERANCE = 12
NEGATIVE_HUE_TOLERANCE = 8


# ==================================================
# HELPERS
# ==================================================

def _hue_distance(hue_a, hue_b):
    """
    Calculate circular HSV hue distance.

    OpenCV hue is represented from 0 to 179,
    so 0 and 179 are close to each other.
    """

    difference = abs(hue_a - hue_b)

    return min(
        difference,
        180 - difference
    )


def _clamp(value, minimum, maximum):
    return max(
        minimum,
        min(
            maximum,
            value
        )
    )


# ==================================================
# CLASSIFICATION
# ==================================================

def classify_reaction(
    calibrated_rgb_distance,
    reaction_hsv,
    reference_hsv,
    reaction_confidence,
    reaction_uniformity,
):
    """
    Deterministically classify the reaction as:

        Positive
        Negative
        Inconclusive

    This is a prototype rule-based classifier.

    It does NOT claim laboratory confirmation.
    """

    if reaction_hsv is None or reference_hsv is None:
        return {
            "classification": "Inconclusive",
            "confidence": 0.0,
            "reason": "Required colour information is unavailable.",
        }

    if calibrated_rgb_distance is None:
        return {
            "classification": "Inconclusive",
            "confidence": 0.0,
            "reason": "Calibrated colour distance is unavailable.",
        }

    # --------------------------------------------------
    # Basic quality protection
    # --------------------------------------------------

    if reaction_confidence < 0.60:
        return {
            "classification": "Inconclusive",
            "confidence": round(
                reaction_confidence,
                3
            ),
            "reason": (
                "Reaction-area detection confidence "
                "is too low for reliable classification."
            ),
        }

    if reaction_uniformity < 0.45:
        return {
            "classification": "Inconclusive",
            "confidence": round(
                reaction_uniformity,
                3
            ),
            "reason": (
                "Reaction area has insufficient colour "
                "uniformity for reliable classification."
            ),
        }

    # --------------------------------------------------
    # Hue comparison
    # --------------------------------------------------

    reaction_hue = reaction_hsv["h"]
    reference_hue = reference_hsv["h"]

    hue_difference = _hue_distance(
        reaction_hue,
        reference_hue
    )

    # --------------------------------------------------
    # Build evidence scores
    # --------------------------------------------------

    # Distance evidence:
    #
    # Very small distance -> weak/no change
    # Larger distance -> stronger colour change
    #
    distance_evidence = _clamp(
        calibrated_rgb_distance / POSITIVE_DISTANCE,
        0.0,
        1.0
    )

    # Hue evidence:
    #
    # Small hue difference means the reaction is
    # still close to the reference hue.
    #
    hue_change_evidence = _clamp(
        hue_difference / POSITIVE_HUE_TOLERANCE,
        0.0,
        1.0
    )

    # --------------------------------------------------
    # Negative condition
    # --------------------------------------------------

    if (
        calibrated_rgb_distance <= NEGATIVE_DISTANCE
        and
        hue_difference <= NEGATIVE_HUE_TOLERANCE
    ):
        confidence = (
            (1.0 - distance_evidence) * 0.65
            +
            (1.0 - hue_change_evidence) * 0.35
        )

        confidence *= (
            0.5 +
            0.5 * reaction_uniformity
        )

        return {
            "classification": "Negative",
            "confidence": round(
                _clamp(confidence, 0.0, 1.0),
                3
            ),
            "reason": (
                "The calibrated reaction colour remains "
                "within the negative similarity range "
                "of the selected reference."
            ),
            "evidence": {
                "rgb_distance": round(
                    calibrated_rgb_distance,
                    3
                ),
                "hue_difference": round(
                    hue_difference,
                    3
                ),
                "reaction_uniformity": round(
                    reaction_uniformity,
                    3
                ),
            },
        }

    # --------------------------------------------------
    # Positive condition
    # --------------------------------------------------

    if (
        calibrated_rgb_distance >= POSITIVE_DISTANCE
        and
        hue_difference >= POSITIVE_HUE_TOLERANCE
    ):
        confidence = (
            distance_evidence * 0.65
            +
            hue_change_evidence * 0.35
        )

        confidence *= (
            0.5 +
            0.5 * reaction_uniformity
        )

        return {
            "classification": "Positive",
            "confidence": round(
                _clamp(confidence, 0.0, 1.0),
                3
            ),
            "reason": (
                "The calibrated reaction colour shows "
                "a measurable change from the selected "
                "reference colour."
            ),
            "evidence": {
                "rgb_distance": round(
                    calibrated_rgb_distance,
                    3
                ),
                "hue_difference": round(
                    hue_difference,
                    3
                ),
                "reaction_uniformity": round(
                    reaction_uniformity,
                    3
                ),
            },
        }

    # --------------------------------------------------
    # Everything between the clear boundaries
    # --------------------------------------------------

    return {
        "classification": "Inconclusive",
        "confidence": 0.5,
        "reason": (
            "The observed colour change falls within "
            "the ambiguous range between clear positive "
            "and clear negative results."
        ),
        "evidence": {
            "rgb_distance": round(
                calibrated_rgb_distance,
                3
            ),
            "hue_difference": round(
                hue_difference,
                3
            ),
            "reaction_uniformity": round(
                reaction_uniformity,
                3
            ),
        },
    }