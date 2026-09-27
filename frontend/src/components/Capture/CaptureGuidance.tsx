function CaptureStatus() {
  return (
    <div className="rounded-lg border border-amber-200 bg-amber-50 px-4 py-3">
      <div className="flex gap-3">
        <span className="text-sm">!</span>

        <div>
          <p className="text-sm font-medium text-amber-800">
            Ready to capture
          </p>

          <p className="mt-0.5 text-xs text-amber-700">
            Make sure the test kit and reference colour card are visible.
          </p>
        </div>
      </div>
    </div>
  );
}

export default CaptureStatus;