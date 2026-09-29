import { useEffect, useRef, useState } from "react";


// --------------------------------------------------
// PROPS
// --------------------------------------------------

interface CameraPreviewProps {
  capturedImage: string | null;
  setCapturedImage: (image: string | null) => void;
}


// --------------------------------------------------
// CAMERA PREVIEW
// --------------------------------------------------

function CameraPreview({
  capturedImage,
  setCapturedImage,
}: CameraPreviewProps) {

  // --------------------------------------------------
  // CAMERA REFERENCES
  // --------------------------------------------------

  const videoRef =
    useRef<HTMLVideoElement | null>(null);

  const streamRef =
    useRef<MediaStream | null>(null);


  // --------------------------------------------------
  // CAMERA STATE
  // --------------------------------------------------

  const [cameraState, setCameraState] = useState<
    "loading" | "ready" | "denied" | "error"
  >("loading");


  // --------------------------------------------------
  // START CAMERA
  // --------------------------------------------------

  const startCamera = async () => {

    try {

      setCameraState("loading");


      // Stop any existing camera stream.
      if (streamRef.current) {

        streamRef.current
          .getTracks()
          .forEach((track) => track.stop());

        streamRef.current = null;
      }


      const stream =
        await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });


      streamRef.current = stream;


      const video =
        videoRef.current;


      if (!video) {

        console.error(
          "Video element not available."
        );

        stream
          .getTracks()
          .forEach((track) => track.stop());

        setCameraState("error");

        return;
      }


      video.srcObject = stream;


      video.onloadedmetadata = async () => {

        try {

          await video.play();

          setCameraState("ready");

        } catch (error) {

          console.error(
            "Video playback error:",
            error
          );

          setCameraState("error");
        }
      };

    } catch (error) {

      console.error(
        "Camera error:",
        error
      );


      if (
        error instanceof DOMException &&
        (
          error.name === "NotAllowedError" ||
          error.name === "PermissionDeniedError"
        )
      ) {

        setCameraState("denied");

      } else {

        setCameraState("error");
      }
    }
  };


  // --------------------------------------------------
  // STOP CAMERA
  // --------------------------------------------------

  const stopCamera = () => {

    if (streamRef.current) {

      streamRef.current
        .getTracks()
        .forEach((track) => track.stop());

      streamRef.current = null;
    }


    if (videoRef.current) {

      videoRef.current.srcObject = null;
    }
  };


  // --------------------------------------------------
  // INITIAL CAMERA START
  // --------------------------------------------------

  useEffect(() => {

    startCamera();


    return () => {

      stopCamera();

    };

  }, []);


  // --------------------------------------------------
  // CAPTURE IMAGE
  // --------------------------------------------------

  const captureImage = () => {

    const video =
      videoRef.current;


    if (
      !video ||
      video.videoWidth === 0 ||
      video.videoHeight === 0
    ) {

      console.warn(
        "Camera frame is not ready."
      );

      return;
    }


    const canvas =
      document.createElement("canvas");


    canvas.width =
      video.videoWidth;

    canvas.height =
      video.videoHeight;


    const context =
      canvas.getContext("2d");


    if (!context) {
      return;
    }


    // --------------------------------------------------
    // MIRROR CORRECTION
    // --------------------------------------------------

    context.translate(
      canvas.width,
      0
    );

    context.scale(-1, 1);


    context.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    );


    context.setTransform(
      1,
      0,
      0,
      1,
      0,
      0
    );


    // --------------------------------------------------
    // CREATE ORIGINAL IMAGE
    // --------------------------------------------------

    const image =
      canvas.toDataURL(
        "image/jpeg",
        0.9
      );


    // Send the newly captured image
    // back to the Capture page.
    setCapturedImage(image);


    // Camera is no longer needed
    // after capturing.
    stopCamera();
  };


  // --------------------------------------------------
  // RETAKE IMAGE
  // --------------------------------------------------

  const retakeImage = async () => {

    // Clear the currently selected image.
    setCapturedImage(null);


    // Small delay so React can update
    // the interface before restarting camera.
    await new Promise(
      (resolve) =>
        setTimeout(resolve, 100)
    );


    await startCamera();
  };


  // --------------------------------------------------
  // UI
  // --------------------------------------------------

  return (

    <div className="relative aspect-video w-full overflow-hidden rounded-xl bg-slate-950">


      {/* --------------------------------------------------
          LIVE CAMERA
      -------------------------------------------------- */}

      <video

        ref={videoRef}

        autoPlay

        playsInline

        muted

        className={`h-full w-full object-cover scale-x-[-1] ${
          capturedImage
            ? "hidden"
            : ""
        }`}

      />


      {/* --------------------------------------------------
          CAMERA LOADING
      -------------------------------------------------- */}

      {!capturedImage &&
        cameraState === "loading" && (

          <div className="absolute inset-0 flex items-center justify-center">

            <div className="text-center">

              <div className="mx-auto mb-3 h-8 w-8 animate-spin rounded-full border-2 border-slate-600 border-t-white" />

              <p className="text-sm font-medium text-white">
                Starting camera...
              </p>

              <p className="mt-1 text-xs text-slate-400">
                Please wait.
              </p>

            </div>

          </div>
        )}


      {/* --------------------------------------------------
          CAMERA READY
      -------------------------------------------------- */}

      {!capturedImage &&
        cameraState === "ready" && (

          <>

            <div className="absolute inset-6 rounded-lg border-2 border-dashed border-white/50" />


            <div className="absolute left-4 top-4 rounded-md bg-slate-900/80 px-3 py-2">

              <p className="text-xs text-slate-300">

                Camera{" "}

                <span className="text-slate-500">
                  •
                </span>{" "}

                <span className="text-green-400">
                  Ready
                </span>

              </p>

            </div>


            <div className="absolute bottom-4 right-4 rounded-md bg-slate-900/80 px-3 py-2">

              <p className="text-xs text-slate-300">

                Reference card:{" "}

                <span className="text-amber-400">
                  Not detected
                </span>

              </p>

            </div>


            <button

              type="button"

              onClick={
                captureImage
              }

              className="absolute bottom-4 left-1/2 -translate-x-1/2 rounded-full bg-white px-6 py-3 text-sm font-semibold text-slate-900 shadow-lg transition hover:bg-slate-100"

            >

              Capture

            </button>

          </>
        )}


      {/* --------------------------------------------------
          CAPTURED / SELECTED IMAGE
      -------------------------------------------------- */}

      {capturedImage && (

        <>

          <img

            src={
              capturedImage
            }

            alt="Selected field test"

            className="h-full w-full object-contain"

          />


          <div className="absolute left-4 top-4 rounded-md bg-slate-900/80 px-3 py-2">

            <p className="text-xs text-white">
              Image selected
            </p>

          </div>


          <button

            type="button"

            onClick={
              retakeImage
            }

            className="absolute bottom-4 right-4 rounded-lg bg-white px-4 py-2 text-sm font-medium text-slate-800 shadow-md transition hover:bg-slate-100"

          >

            Retake

          </button>

        </>

      )}


      {/* --------------------------------------------------
          CAMERA DENIED
      -------------------------------------------------- */}

      {!capturedImage &&
        cameraState === "denied" && (

          <div className="absolute inset-0 flex items-center justify-center px-6">

            <div className="max-w-md text-center">

              <div className="mb-3 text-4xl">
                🚫
              </div>

              <h3 className="text-sm font-semibold text-white">
                Camera access was denied
              </h3>

              <p className="mt-2 text-xs leading-5 text-slate-400">
                Allow camera access in your browser
                settings and try again.
              </p>

              <button

                type="button"

                onClick={
                  startCamera
                }

                className="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-xs font-medium text-white transition hover:bg-blue-700"

              >

                Try Again

              </button>

            </div>

          </div>

        )}


      {/* --------------------------------------------------
          CAMERA ERROR
      -------------------------------------------------- */}

      {!capturedImage &&
        cameraState === "error" && (

          <div className="absolute inset-0 flex items-center justify-center px-6">

            <div className="max-w-md text-center">

              <div className="mb-3 text-4xl">
                📷
              </div>

              <h3 className="text-sm font-semibold text-white">
                Camera unavailable
              </h3>

              <p className="mt-2 text-xs leading-5 text-slate-400">
                We couldn't access a camera on this device.
              </p>

              <button

                type="button"

                onClick={
                  startCamera
                }

                className="mt-4 rounded-lg bg-blue-600 px-4 py-2 text-xs font-medium text-white transition hover:bg-blue-700"

              >

                Try Again

              </button>

            </div>

          </div>

        )}

    </div>
  );
}


export default CameraPreview;