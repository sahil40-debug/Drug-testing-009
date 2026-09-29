import cv2
import numpy as np
import base64

from analysis.color_analysis import analyze_colour


# ==================================================
# CREATE SYNTHETIC TEST IMAGE
# ==================================================

def create_test_image():
    image = np.full(
        (600, 900, 3),
        (245, 245, 245),
        dtype=np.uint8
    )

    # Field-test surface
    cv2.rectangle(
    image,
    (500, 170),
    (830, 400),
    (120, 220, 240),
    -1
)

    # Reference card
    # BGR -> RGB = (240, 220, 120)
    cv2.rectangle(
        image,
        (450, 170),
        (780, 400),
        (120, 220, 240),
        -1
    )

    # Reaction area
    cv2.rectangle(
        image,
        (170, 180),
        (330, 300),
        (115, 205, 220),
        -1
    )

    return image


# ==================================================
# CONVERT IMAGE TO BASE64
# ==================================================

def image_to_base64(image):
    # PNG keeps the synthetic colours exact.
    success, buffer = cv2.imencode(
        ".png",
        image
    )

    if not success:
        raise RuntimeError(
            "Could not encode synthetic image."
        )

    encoded = base64.b64encode(
        buffer.tobytes()
    ).decode("utf-8")

    return encoded


# ==================================================
# MAIN TEST
# ==================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("INTEGRATED COLOUR ANALYSIS TEST")
    print("=" * 70)

    # Create synthetic image
    image = create_test_image()

    # Save image for visual inspection
    cv2.imwrite(
        "integrated_colour_test.jpg",
        image
    )

    print()
    print("Saved: integrated_colour_test.jpg")

    # Convert image to Base64
    image_data = image_to_base64(image)

    print()
    print("Base64 image data created:", bool(image_data))
    print("Base64 length:", len(image_data))
    print("Expected reference RGB:", (240, 220, 120))

    # Run complete colour-analysis pipeline
    result = analyze_colour(
        image_data=image_data,
        reference_color="Yellow",
        reference_shade="Shade 1",
        reference_color_value="#F0DC78",
    )

    print()
    print("Analysis result:")
    print(result)

    # ==================================================
    # VALIDATION
    # ==================================================

    print()
    print("=" * 70)
    print("VALIDATION")
    print("=" * 70)

    if not result.get("success", False):

        print()
        print("FAIL — Integrated analysis failed.")
        print()
        print("Stage:", result.get("stage"))
        print("Message:", result.get("message"))

    else:

        print()
        print("PASS — Integrated analysis completed.")

        reference_detection = result.get(
            "reference_detection",
            {}
        )

        reference = result.get(
            "reference",
            {}
        )

        reaction = result.get(
            "reaction",
            {}
        )

        calibration = result.get(
            "calibration",
            {}
        )

        print()
        print("Reference detection:")
        print("Attempt:", reference_detection.get("attempt"))
        print("Confidence:", reference_detection.get("confidence"))

        print()
        print("Measured reference RGB:")
        print(reference.get("measured_rgb"))

        print()
        print("Original reaction RGB:")
        print(reaction.get("original_rgb"))

        print()
        print("Calibrated reaction RGB:")
        print(reaction.get("calibrated_rgb"))

        print()
        print("Original RGB distance:")
        print(reaction.get("original_rgb_distance"))

        print()
        print("Calibrated RGB distance:")
        print(reaction.get("calibrated_rgb_distance"))

        print()
        print("Correction factors:")
        print(calibration.get("correction_factors"))

    print()
    print("=" * 70)