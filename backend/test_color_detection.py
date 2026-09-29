import cv2
import numpy as np

from analysis.color_analysis import (
    detect_reference_card
)


# ============================================================
# SYNTHETIC IMAGE CREATION
# ============================================================

def create_normal_test_image():

    image = np.full(
        (600, 900, 3),
        (245, 245, 245),
        dtype=np.uint8
    )


    # ========================================================
    # FAKE FIELD-TEST SURFACE
    # ========================================================

    cv2.rectangle(
        image,
        (70, 90),
        (450, 360),
        (115, 210, 229),
        -1
    )


    # ========================================================
    # REACTION AREA
    # ========================================================

    cv2.rectangle(
        image,
        (170, 180),
        (330, 300),
        (115, 205, 220),
        -1
    )


    # ========================================================
    # REFERENCE COLOUR CARD
    #
    # Expected RGB:
    #
    # R = 240
    # G = 220
    # B = 120
    #
    # OpenCV requires BGR:
    #
    # B = 120
    # G = 220
    # R = 240
    # ========================================================

    # Outer card border

    cv2.rectangle(
        image,
        (450, 170),
        (780, 400),
        (40, 40, 40),
        -1
    )


    # Inner colour area

    cv2.rectangle(
        image,
        (458, 178),
        (772, 392),
        (120, 220, 240),
        -1
    )


    return image


# ============================================================
# TEST 2 — NO REAL REFERENCE CARD
# ============================================================

def create_negative_test_image():

    image = np.full(
        (600, 900, 3),
        (245, 245, 245),
        dtype=np.uint8
    )


    # ========================================================
    # LARGE BACKGROUND REGION
    #
    # Similar colour, but NOT a reference card.
    # ========================================================

    cv2.rectangle(
        image,
        (70, 105),
        (440, 360),
        (135, 201, 221),
        -1
    )


    # ========================================================
    # SMALL FAKE COLOURED OBJECT
    #
    # This should NOT be accepted.
    # ========================================================

    cv2.rectangle(
        image,
        (550, 150),
        (670, 240),
        (130, 210, 230),
        -1
    )


    return image


# ============================================================
# TEST 1
# ============================================================

def run_normal_test():

    print()
    print("=" * 60)
    print("TEST 1 — NORMAL FIELD TEST")
    print("=" * 60)


    image = create_normal_test_image()


    result = detect_reference_card(
        image=image,
        expected_rgb=(240, 220, 120)
    )


    print()
    print("Detection result:")
    print(result)


    cv2.imwrite(
        "synthetic_field_test.jpg",
        image
    )


    print()
    print("Saved: synthetic_field_test.jpg")


    return result


# ============================================================
# TEST 2
# ============================================================

def run_negative_test():

    print()
    print("=" * 60)
    print("TEST 2 — NO REAL REFERENCE CARD")
    print("=" * 60)


    image = create_negative_test_image()


    result = detect_reference_card(
        image=image,
        expected_rgb=(240, 220, 120)
    )


    print()
    print("Detection result:")
    print(result)


    cv2.imwrite(
        "negative_reference_test.jpg",
        image
    )


    print()
    print("Saved: negative_reference_test.jpg")


    return result


# ============================================================
# MAIN TEST RUNNER
# ============================================================

if __name__ == "__main__":

    normal_result = run_normal_test()

    negative_result = run_negative_test()


    print()
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)


    normal_accepted = (
        normal_result.get("success", False)
    )

    negative_accepted = (
        negative_result.get("success", False)
    )


    print()
    print(
        "Normal test accepted:",
        normal_accepted
    )

    print(
        "Negative test accepted:",
        negative_accepted
    )


    print()


    if normal_accepted and not negative_accepted:

        print(
            "PASS — Detector behaves correctly."
        )

    else:

        print(
            "REVIEW REQUIRED — "
            "Detector needs adjustment."
        )


    print()
    print("=" * 60)