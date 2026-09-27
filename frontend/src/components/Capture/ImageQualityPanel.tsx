function ImageQualityPanel() {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4">
        <h2 className="text-base font-semibold text-slate-900">
          Image Quality
        </h2>

        <p className="mt-1 text-xs text-slate-500">
          Image checks will run automatically after capture.
        </p>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">
            Reference card
          </span>

          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-500">
            Waiting
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">
            Image sharpness
          </span>

          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-500">
            Waiting
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">
            Lighting
          </span>

          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-500">
            Waiting
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">
            Glare / shadows
          </span>

          <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-500">
            Waiting
          </span>
        </div>
      </div>
    </section>
  );
}

export default ImageQualityPanel;