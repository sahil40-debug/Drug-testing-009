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

function Capture() {
  const [capturedImage, setCapturedImage] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null);
  const [selectedColor, setSelectedColor] =
  useState<ReferenceColor | null>(null);

  // This function sends the image to our FastAPI backend
  const handleAnalyze = async () => {
    if (!capturedImage) {
      alert("Please capture or upload an image first.");
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
  image_data: capturedImage,
  reference_color: selectedGroup,
  reference_shade: selectedColor?.name ?? null,
  reference_color_value: selectedColor?.value ?? null,
}),
      });

      const data = await response.json();
      console.log("Backend response:", data);
      
      // Temporary alert to prove it worked!
      alert(data.message);
      
    } catch (error) {
      console.error("Error sending image to backend:", error);
      alert("Failed to connect to the backend server.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100">
      <Sidebar />

      <main className="ml-64 min-h-screen p-8">
        <div className="mb-8">
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <span>Dashboard</span>
            <span>/</span>
            <span className="text-slate-700">New Field Test</span>
          </div>

          <h1 className="mt-3 text-3xl font-bold text-slate-900">
            New Field Test
          </h1>

          <p className="mt-1 text-slate-500">
            Capture and validate the field test image before classification.
          </p>
        </div>

        <div className="mb-6">
          <TestInformation />
        </div>
        <div className="mb-6">
          <ReferenceColorSelector
          selectedGroup={selectedGroup}
          selectedColor={selectedColor}
          setSelectedGroup={setSelectedGroup}
          setSelectedColor={setSelectedColor} 
          />
        </div>

        <div className="grid grid-cols-1 gap-6 xl:grid-cols-3">
          <section className="xl:col-span-2">
            <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="mb-5">
                <h2 className="text-lg font-semibold text-slate-900">
                  Capture Test Image
                </h2>
                <p className="mt-1 text-sm text-slate-500">
                  Position the test kit and reference card clearly inside the camera frame.
                </p>
              </div>

              <CameraPreview 
                capturedImage={capturedImage} 
                setCapturedImage={setCapturedImage} 
              />

              <div className="mt-5">
                <CaptureControls setCapturedImage={setCapturedImage} />
              </div>

              <div className="mt-4">
                <CaptureStatus />
              </div>
            </div>
          </section>

          <aside className="space-y-6">
            <ImageQualityPanel />
            <CaptureGuidance />
          </aside>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            type="button"
            onClick={handleAnalyze}
            disabled={!capturedImage || isAnalyzing}
            className="rounded-lg bg-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? "Analyzing..." : "Continue to Analysis →"}
          </button>
        </div>
      </main>
    </div>
  );
}

export default Capture;