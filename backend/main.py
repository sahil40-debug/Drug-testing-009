from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from analysis.image_quality import analyze_image_quality


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
# Analyze endpoint
# --------------------------------------------------

@app.post("/api/analyze")
def analyze_image(payload: ImagePayload):

    return analyze_image_quality(
        payload.image_data
    )