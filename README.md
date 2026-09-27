# Digital Companion for Field Drug Testing

This project is being developed as part of **Smart India Hackathon (SIH) 2026**, based on Problem Statement **PS-231 – Digital Companion for Field Drug Testing**.

The main idea is to make the process of recording and managing field drug tests more organized and reliable. The system is being designed around the existing colour-change field testing kits, so the focus is not on creating new testing hardware but on building a digital system around the testing process.

## What We've done so far

The project is still under development, but the basic application structure is now in place.

### Frontend

* Set up the frontend using **React + TypeScript + Vite**.
* Added routing for the main pages of the application.
* Created the login page and basic dashboard structure.
* Added a sidebar for navigating between different sections.
* Started building the field test capture page.
* Added a camera preview using the browser camera.
* Added image capture and retake functionality.
* Added an option to upload an existing image instead of using the camera.
* Fixed the camera preview/captured-image mirroring issue.
* Added separate components for the different parts of the capture page instead of keeping everything in one file.
* Started using **Tailwind CSS** for the interface.

### Backend

* Set up the backend using **Python + FastAPI**.
* Added CORS configuration so the React frontend can communicate with the backend locally.
* Added an image analysis endpoint:
  `/api/analyze`
* Added the first image-quality check using **OpenCV**.
* The current backend checks the sharpness of a captured image before allowing it to move further in the workflow.
* Added handling for images sent from the frontend as Base64 data.
* Tested the complete frontend → backend request and fixed the JSON serialization issue caused by NumPy boolean values.

## Current workflow

At the moment, the basic flow is:

```text
Open Field Test
      ↓
Camera / Upload Image
      ↓
Capture Image
      ↓
Send Image to Backend
      ↓
OpenCV Image Quality Check
      ↓
Quality Result
```

This is only the beginning of the complete system.

## Planned development

The next stages will include:

* Better image-quality checks
* Reference colour card detection
* Lighting/colour calibration
* Field-test colour analysis
* Positive / Negative / Inconclusive classification
* Test result screen
* Test history and searchable records
* Tamper-evident digital records
* Image hashing
* Timestamp and operator information
* Cryptographic signing and verification
* Verification page for checking the integrity of stored test records
* Better error handling and user feedback
* Final UI/UX improvements

The system is intended to provide a **digital record and decision-support workflow for presumptive field testing**. It is not intended to replace laboratory confirmation.

## Tech Stack

**Frontend**

* React
* TypeScript
* Vite
* Tailwind CSS

**Backend**

* Python
* FastAPI
* OpenCV
* NumPy

**Development**

* Git
* GitHub

## Project Status

🚧 **Work in Progress**

I'm building this step by step rather than trying to implement the entire system at once. The goal is to keep the project modular so that new features can be added without breaking the parts that are already working.
