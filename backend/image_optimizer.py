import cv2
import numpy as np
import base64


def decode_image(image_data: str):
    try:
        if "," in image_data:
            image_data = image_data.split(",", 1)[1]

        img_bytes = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_bytes, np.uint8)

        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    except Exception:
        return None


def encode_image(img):
    success, buffer = cv2.imencode(".jpg", img, [
        cv2.IMWRITE_JPEG_QUALITY,
        95,
    ])

    if not success:
        return None

    encoded = base64.b64encode(buffer).decode("utf-8")

    return f"data:image/jpeg;base64,{encoded}"


def optimize_image(image_data: str):

    img = decode_image(image_data)

    if img is None:
        return {
            "success": False,
            "message": "Could not read image for optimization.",
        }

    original = img.copy()

    # ----------------------------------------------
    # 1. Mild denoising
    # ----------------------------------------------

    denoised = cv2.fastNlMeansDenoisingColored(
        img,
        None,
        3,
        3,
        7,
        21,
    )

    # ----------------------------------------------
    # 2. Controlled brightness/contrast correction
    # ----------------------------------------------

    lab = cv2.cvtColor(
        denoised,
        cv2.COLOR_BGR2LAB,
    )

    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=1.5,
        tileGridSize=(8, 8),
    )

    l_corrected = clahe.apply(l_channel)

    corrected_lab = cv2.merge(
        (l_corrected, a_channel, b_channel)
    )

    corrected = cv2.cvtColor(
        corrected_lab,
        cv2.COLOR_LAB2BGR,
    )

    # ----------------------------------------------
    # 3. Very mild sharpening
    # ----------------------------------------------

    blurred = cv2.GaussianBlur(
        corrected,
        (0, 0),
        1.0,
    )

    optimized = cv2.addWeighted(
        corrected,
        1.15,
        blurred,
        -0.15,
        0,
    )

    # ----------------------------------------------
    # Safety check
    # ----------------------------------------------

    if optimized is None:
        optimized = original

    optimized_image = encode_image(optimized)

    if optimized_image is None:
        return {
            "success": False,
            "message": "Could not encode optimized image.",
        }

    return {
        "success": True,
        "message": (
            "A controlled copy of the image was created "
            "without modifying the original image."
        ),
        "original_image": image_data,
        "optimized_image": optimized_image,
    }