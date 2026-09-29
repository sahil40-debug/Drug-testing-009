# Digital Companion for Field Drug Testing

This project is being developed as part of **Smart India Hackathon (SIH) 2026**, based on Problem Statement **PS-231 – Digital Companion for Field Drug Testing**.

The project focuses on building a digital system around existing **colour-change field drug testing kits**. The goal is to make field-test capture, colour analysis, result classification, and digital record management more organized, consistent, and reliable.

The system is being developed as a modular application so that each part of the workflow can be developed and tested independently without breaking previously completed components.

---

## What We've Done So Far

The project has now progressed beyond the initial application setup. The camera capture, image-quality analysis, image optimization, reference-card detection, reaction-area detection, colour calibration, and initial classification pipeline are working together in the backend.

---

## Frontend

The frontend is built using **React + TypeScript + Vite + Tailwind CSS**.

### Application structure

* Set up the frontend using **React + TypeScript + Vite**.
* Added routing for the main application pages.
* Created the login page.
* Created the dashboard structure.
* Added a sidebar for navigation between application sections.
* Started building the field-test capture workflow.
* Separated the capture functionality into reusable components instead of keeping everything in one file.
* Started using **Tailwind CSS** for the interface.

### Camera and image capture

* Added browser-based camera access.
* Added live camera preview.
* Added image capture functionality.
* Added image retake functionality.
* Added support for uploading an existing image.
* Added captured-image preview.
* Fixed the camera preview/captured-image mirroring issue.
* Added handling for starting a new image capture.

### Image quality workflow

The frontend now communicates with the backend to perform image-quality analysis.

The system can check:

* Image resolution
* Image sharpness
* Brightness
* Exposure

The user can see the quality result before continuing with the analysis workflow.

### Image optimization

An optimization workflow has also been added.

The system:

* Keeps the original captured image unchanged.
* Creates a separate optimized copy when required.
* Allows the user to compare/select between the original and optimized image.
* Never overwrites the original evidence image with the optimized version.

This keeps the original captured image available for evidence and record-keeping purposes.

### Reference colour selection

The capture workflow now includes selection of the reference colour information used for calibration.

The reference colour system contains:

* Colour groups
* Individual shades
* Expected colour values for the selected shade

The selected reference colour is passed into the backend colour-analysis pipeline.

---

# Backend

The backend is built using:

* **Python**
* **FastAPI**
* **OpenCV**
* **NumPy**

The backend receives image data from the frontend as Base64 and processes it through multiple analysis stages.

---

## Image Analysis Pipeline

The current backend analysis pipeline is:

```text
Captured / Uploaded Image
          ↓
Image Decode
          ↓
Image Quality Analysis
          ↓
Reference Colour Selection
          ↓
Reference Card Detection
          ↓
Reference Colour Measurement
          ↓
Reaction Area Detection
          ↓
Reaction Colour Extraction
          ↓
Colour Calibration
          ↓
RGB / HSV Analysis
          ↓
Deterministic Classification
          ↓
Positive / Negative / Inconclusive
