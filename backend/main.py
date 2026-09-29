from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from image_optimizer import optimize_image

from analysis.image_quality import analyze_image_quality
from analysis.color_analysis import analyze_colour


# ==================================================
# FASTAPI APPLICATION
# ==================================================

app = FastAPI()


# ==================================================
# CORS
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================================================
# REQUEST MODEL
# ==================================================

class ImagePayload(BaseModel):

    image_data: str

    # Optional colour-analysis information.
    # Keeping these optional preserves compatibility
    # with the existing frontend workflow.

    reference_color: str | None = None
    reference_shade: str | None = None
    reference_color_value: str | None = None


# ==================================================
# ANALYZE ENDPOINT
# ==================================================

@app.post("/api/analyze")
def analyze_image(payload: ImagePayload):

    # --------------------------------------------------
    # EXISTING IMAGE QUALITY ANALYSIS
    # --------------------------------------------------

    quality_result = analyze_image_quality(
        payload.image_data
    )


    # --------------------------------------------------
    # BACKWARD-COMPATIBLE RESPONSE
    # --------------------------------------------------

    response = quality_result


    # --------------------------------------------------
    # COLOUR ANALYSIS
    # --------------------------------------------------
    # Only run colour analysis when a reference colour
    # value has been supplied.
    #
    # This prevents the existing frontend workflow
    # from being broken.

    if payload.reference_color_value:

        colour_result = analyze_colour(

            image_data=payload.image_data,

            reference_color=payload.reference_color,

            reference_shade=payload.reference_shade,

            reference_color_value=payload.reference_color_value,

        )

        response["color_analysis"] = colour_result


    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return response


# ==================================================
# OPTIMIZE ENDPOINT
# ==================================================

@app.post("/api/optimize")
def optimize_image_endpoint(payload: ImagePayload):

    return optimize_image(
        payload.image_data
    )