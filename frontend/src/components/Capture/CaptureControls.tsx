import { useRef } from "react";

interface CaptureControlsProps {
  setCapturedImage: (image: string | null) => void;
}

function CaptureControls({ setCapturedImage }: CaptureControlsProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setCapturedImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <div>
      <input
        type="file"
        accept="image/*"
        ref={fileInputRef}
        className="hidden"
        onChange={handleFileChange}
      />

      <button
        type="button"
        onClick={handleUploadClick}
        className="w-full rounded-lg border border-slate-300 bg-white px-5 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
      >
        Upload Image Instead
      </button>

      <p className="mt-2 text-center text-xs text-slate-400">
        You can upload an existing test image if camera capture is not available.
      </p>
    </div>
  );
}

export default CaptureControls;