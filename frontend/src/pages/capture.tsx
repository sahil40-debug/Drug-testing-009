import { useState } from "react";
import Sidebar from "../components/Sidebar";

import TestInformation from "../components/Capture/TestInformation";
import CameraPreview from "../components/Capture/CameraPreview";
import CaptureControls from "../components/Capture/CaptureControls";
import ImageQualityPanel from "../components/Capture/ImageQualityPanel";
import CaptureStatus from "../components/Capture/CaptureStatus";
import CaptureGuidance from "../components/Capture/CaptureGuidance";
import ReferenceColorSelector from "../components/Capture/ReferenceColorSelector";
import type { ReferenceColor } from "../components/Capture/ReferenceColorSelector";


// --------------------------------------------------
// CAPTURE PAGE
// --------------------------------------------------

function Capture() {


  // --------------------------------------------------
  // IMAGE STATE
  // --------------------------------------------------

  // Original image captured by the camera.
  // This image is NEVER modified.
  const [originalImage, setOriginalImage] =
    useState<string | null>(null);

  // Optimized copy created by the backend.
  const [optimizedImage, setOptimizedImage] =
    useState<string | null>(null);

  // Image currently selected for analysis.
  const [capturedImage, setCapturedImage] =
    useState<string | null>(null);

  // Which version is currently selected.
  const [selectedImageVersion, setSelectedImageVersion] =
    useState<"original" | "optimized">("original");


  // --------------------------------------------------
  // REFERENCE COLOUR STATE
  // --------------------------------------------------

  const [selectedGroup, setSelectedGroup] =
    useState<string | null>(null);

  const [selectedColor, setSelectedColor] =
    useState<ReferenceColor | null>(null);


  // --------------------------------------------------
  // QUALITY RESULT STATE
  // --------------------------------------------------

  // Result currently displayed in ImageQualityPanel.
  const [qualityResult, setQualityResult] =
    useState<any>(null);

  // Quality result for original image.
  const [originalQualityResult, setOriginalQualityResult] =
    useState<any>(null);

  // Quality result for optimized image.
  const [optimizedQualityResult, setOptimizedQualityResult] =
    useState<any>(null);


  // --------------------------------------------------
  // LOADING STATE
  // --------------------------------------------------

  const [isAnalyzing, setIsAnalyzing] =
    useState(false);

  const [isOptimizing, setIsOptimizing] =
    useState(false);


  // --------------------------------------------------
  // HANDLE NEW CAPTURE
  // --------------------------------------------------

  const handleNewImage = (image: string | null) => {

    // Save the newly captured image as the original.
    setOriginalImage(image);

    // The newly captured image becomes the
    // currently selected image.
    setCapturedImage(image);

    // New captures always start as original.
    setSelectedImageVersion("original");

    // Remove any previous optimized image.
    setOptimizedImage(null);

    // Remove previous quality results.
    setQualityResult(null);
    setOriginalQualityResult(null);
    setOptimizedQualityResult(null);
  };


  // --------------------------------------------------
  // ANALYZE IMAGE
  // --------------------------------------------------

  const analyzeImage = async (
    image: string,
    imageVersion: "original" | "optimized"
  ) => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/analyze",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({

            image_data: image,

            reference_color:
              selectedGroup,

            reference_shade:
              selectedColor?.name ?? null,

            reference_color_value:
              selectedColor?.value ?? null,

          }),
        }
      );


      const data = await response.json();


      console.log(
        `${imageVersion} image analysis:`,
        data
      );


      if (!response.ok || !data.success) {

        alert(
          data.message ||
          "Unable to analyze the image."
        );

        return null;
      }


      // Store the result separately depending
      // on which image was analyzed.

      if (imageVersion === "original") {

        setOriginalQualityResult(data);

      } else {

        setOptimizedQualityResult(data);

      }


      // Update the main Image Quality panel.
      setQualityResult(data);


      return data;

    } catch (error) {

      console.error(
        `Error analyzing ${imageVersion} image:`,
        error
      );

      alert(
        "Failed to connect to the backend server."
      );

      return null;
    }
  };


  // --------------------------------------------------
  // CONTINUE TO ANALYSIS
  // --------------------------------------------------

  const handleAnalyze = async () => {

    let imageToAnalyze: string | null = null;


    // Determine which image the user selected.

    if (selectedImageVersion === "optimized") {

      imageToAnalyze = optimizedImage;

    } else {

      imageToAnalyze = originalImage;

    }


    if (!imageToAnalyze) {

      alert(
        "Please capture or upload an image first."
      );

      return;
    }


    // Keep the selected image as the current image.
    setCapturedImage(imageToAnalyze);

    setIsAnalyzing(true);


    try {

      await analyzeImage(
        imageToAnalyze,
        selectedImageVersion
      );

    } finally {

      setIsAnalyzing(false);
    }
  };


  // --------------------------------------------------
  // OPTIMIZE IMAGE
  // --------------------------------------------------

  const handleOptimize = async () => {

    if (!originalImage) {

      alert(
        "Please capture or upload an image first."
      );

      return;
    }


    setIsOptimizing(true);


    try {

      const response = await fetch(
        "http://127.0.0.1:8000/api/optimize",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            image_data: originalImage,
          }),
        }
      );


      const data = await response.json();


      console.log(
        "Optimization response:",
        data
      );


      if (!response.ok || !data.success) {

        alert(
          data.message ||
          "Unable to optimize the image."
        );

        return;
      }


      // Store optimized image separately.
      setOptimizedImage(
        data.optimized_image
      );


      // Automatically analyze the optimized copy.
      setIsAnalyzing(true);

      await analyzeImage(
        data.optimized_image,
        "optimized"
      );

      setIsAnalyzing(false);

    } catch (error) {

      console.error(
        "Error optimizing image:",
        error
      );

      alert(
        "Failed to connect to the backend server."
      );

    } finally {

      setIsOptimizing(false);
      setIsAnalyzing(false);
    }
  };


  // --------------------------------------------------
  // USE OPTIMIZED IMAGE
  // --------------------------------------------------

  const handleUseOptimized = () => {

    if (!optimizedImage) {
      return;
    }


    console.log(
      "Selecting optimized image"
    );


    // Mark optimized as selected.
    setSelectedImageVersion("optimized");


    // Show optimized image in the main capture area.
    setCapturedImage(optimizedImage);


    // Show optimized quality result.
    if (optimizedQualityResult) {

      setQualityResult(
        optimizedQualityResult
      );

    }
  };


  // --------------------------------------------------
  // USE ORIGINAL IMAGE
  // --------------------------------------------------

  const handleKeepOriginal = () => {

    if (!originalImage) {
      return;
    }


    console.log(
      "Selecting original image"
    );


    // Mark original as selected.
    setSelectedImageVersion("original");


    // Restore untouched original image.
    setCapturedImage(originalImage);


    // Show original quality result.
    if (originalQualityResult) {

      setQualityResult(
        originalQualityResult
      );

    }
  };


  // --------------------------------------------------
  // PAGE UI
  // --------------------------------------------------

  return (

    <div className="min-h-screen bg-slate-100">

      <Sidebar />


      <main className="ml-64 min-h-screen p-8">


        {/* --------------------------------------------------
            PAGE HEADER
        -------------------------------------------------- */}

        <div className="mb-8">

          <div className="flex items-center gap-2 text-sm text-slate-500">

            <span>
              Dashboard
            </span>

            <span>
              /
            </span>

            <span className="text-slate-700">
              New Field Test
            </span>

          </div>


          <h1 className="mt-3 text-3xl font-bold text-slate-900">
            New Field Test
          </h1>


          <p className="mt-1 text-slate-500">
            Capture and validate the field test image
            before classification.
          </p>

        </div>


        {/* --------------------------------------------------
            TEST INFORMATION
        -------------------------------------------------- */}

        <div className="mb-6">

          <TestInformation />

        </div>


        {/* --------------------------------------------------
            REFERENCE COLOUR SELECTOR
        -------------------------------------------------- */}

        <div className="mb-6">

          <ReferenceColorSelector

            selectedGroup={
              selectedGroup
            }

            selectedColor={
              selectedColor
            }

            setSelectedGroup={
              setSelectedGroup
            }

            setSelectedColor={
              setSelectedColor
            }

          />

        </div>


        {/* --------------------------------------------------
            MAIN CAPTURE AREA
        -------------------------------------------------- */}

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">


          {/* --------------------------------------------------
              CAMERA SECTION
          -------------------------------------------------- */}

          <section className="xl:col-span-2">

            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">


              {/* CAMERA HEADER */}

              <div className="mb-5">

                <h2 className="text-lg font-semibold text-slate-900">
                  Capture Test Image
                </h2>

                <p className="mt-1 text-sm text-slate-500">
                  Position the test kit and reference card
                  clearly inside the camera frame.
                </p>

              </div>


              {/* CAMERA PREVIEW */}

              <CameraPreview

                capturedImage={
                  capturedImage
                }

                setCapturedImage={
                  handleNewImage
                }

              />


              {/* CAPTURE CONTROLS */}

              <div className="mt-5">

                <CaptureControls

                  setCapturedImage={
                    handleNewImage
                  }

                />

              </div>


              {/* CAPTURE STATUS */}

              <div className="mt-4">

                <CaptureStatus />

              </div>


              {/* --------------------------------------------------
                  IMAGE COMPARISON
              -------------------------------------------------- */}

              {optimizedImage && (

                <div className="mt-5 rounded-xl border border-slate-200 bg-slate-50 p-4">


                  {/* COMPARISON HEADER */}

                  <div className="mb-4">

                    <h3 className="text-sm font-semibold text-slate-900">
                      Image Comparison
                    </h3>

                    <p className="mt-1 text-xs text-slate-500">
                      Compare the original capture with the
                      optimized copy before choosing which
                      image to use.
                    </p>

                  </div>


                  {/* CURRENT SELECTION */}

                  <div className="mb-4 rounded-lg border border-blue-200 bg-blue-50 px-4 py-3">

                    <p className="text-xs text-blue-600">
                      Currently selected
                    </p>

                    <p className="mt-1 text-sm font-semibold text-blue-900">

                      {selectedImageVersion === "original"
                        ? "Original Image"
                        : "Optimized Image"}

                    </p>

                  </div>


                  {/* --------------------------------------------------
                      ORIGINAL IMAGE
                  -------------------------------------------------- */}

                  <div
                    className={`mb-5 rounded-lg border-2 bg-white p-3 ${
                      selectedImageVersion === "original"
                        ? "border-blue-500"
                        : "border-slate-200"
                    }`}
                  >

                    <div className="mb-3 flex items-center justify-between">

                      <h4 className="text-sm font-semibold text-slate-900">
                        Original Image
                      </h4>


                      {selectedImageVersion === "original" && (

                        <span className="rounded-full bg-blue-100 px-2.5 py-1 text-xs font-medium text-blue-700">
                          Selected
                        </span>

                      )}

                    </div>


                    <img
                      src={originalImage || ""}
                      alt="Original field test"
                      className="w-full rounded-lg border border-slate-200"
                    />


                    {originalQualityResult && (

                      <div className="mt-3 rounded-lg bg-slate-50 p-3">

                        <p className="text-xs text-slate-500">
                          Original image quality
                        </p>

                        <p className="mt-1 text-lg font-semibold text-slate-900">

                          {originalQualityResult.quality_score ?? "N/A"}
                          /100

                        </p>

                      </div>

                    )}


                    <button

                      type="button"

                      onClick={
                        handleKeepOriginal
                      }

                      className="mt-3 w-full rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"

                    >

                      {selectedImageVersion === "original"
                        ? "Original Image Selected"
                        : "Use Original Image"}

                    </button>

                  </div>


                  {/* --------------------------------------------------
                      OPTIMIZED IMAGE
                  -------------------------------------------------- */}

                  <div
                    className={`rounded-lg border-2 bg-white p-3 ${
                      selectedImageVersion === "optimized"
                        ? "border-green-500"
                        : "border-slate-200"
                    }`}
                  >

                    <div className="mb-3 flex items-center justify-between">

                      <h4 className="text-sm font-semibold text-slate-900">
                        Optimized Image
                      </h4>


                      {selectedImageVersion === "optimized" && (

                        <span className="rounded-full bg-green-100 px-2.5 py-1 text-xs font-medium text-green-700">
                          Selected
                        </span>

                      )}

                    </div>


                    <img
                      src={optimizedImage}
                      alt="Optimized field test"
                      className="w-full rounded-lg border border-slate-200"
                    />


                    {optimizedQualityResult && (

                      <div className="mt-3 rounded-lg bg-slate-50 p-3">

                        <p className="text-xs text-slate-500">
                          Optimized image quality
                        </p>

                        <p className="mt-1 text-lg font-semibold text-slate-900">

                          {optimizedQualityResult.quality_score ?? "N/A"}
                          /100

                        </p>

                      </div>

                    )}


                    <button

                      type="button"

                      onClick={
                        handleUseOptimized
                      }

                      className="mt-3 w-full rounded-lg bg-green-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-green-700"

                    >

                      {selectedImageVersion === "optimized"
                        ? "Optimized Image Selected"
                        : "Use Optimized Image"}

                    </button>

                  </div>


                </div>

              )}


            </div>

          </section>


          {/* --------------------------------------------------
              RIGHT SIDEBAR
          -------------------------------------------------- */}

          <aside className="space-y-6">

            <ImageQualityPanel
              qualityResult={
                qualityResult
              }
            />

            <CaptureGuidance />

          </aside>

        </div>


        {/* --------------------------------------------------
            BOTTOM ACTIONS
        -------------------------------------------------- */}

        <div className="mt-6 flex flex-wrap justify-end gap-3">


          {/* OPTIMIZE IMAGE */}

          <button

            type="button"

            onClick={
              handleOptimize
            }

            disabled={
              !originalImage ||
              isOptimizing
            }

            className="rounded-lg border border-slate-300 bg-white px-6 py-3 text-sm font-semibold text-slate-700 shadow-sm transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"

          >

            {isOptimizing
              ? "Optimizing..."
              : "Optimize Image"}

          </button>


          {/* CONTINUE TO ANALYSIS */}

          <button

            type="button"

            onClick={
              handleAnalyze
            }

            disabled={
              !capturedImage ||
              isAnalyzing
            }

            className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"

          >

            {isAnalyzing
              ? "Analyzing..."
              : "Continue to Analysis →"}

          </button>


        </div>


      </main>

    </div>

  );
}


export default Capture;