function CaptureGuidance() {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-base font-semibold text-slate-900">
        Capture Guidelines
      </h2>

      <div className="mt-4 space-y-4">
        <div className="flex gap-3">
          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-slate-100 text-xs font-semibold text-slate-700">
            1
          </span>

          <p className="text-sm leading-5 text-slate-600">
            Place the test kit on a stable surface.
          </p>
        </div>

        <div className="flex gap-3">
          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-slate-100 text-xs font-semibold text-slate-700">
            2
          </span>

          <p className="text-sm leading-5 text-slate-600">
            Include the complete reference colour card.
          </p>
        </div>

        <div className="flex gap-3">
          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-slate-100 text-xs font-semibold text-slate-700">
            3
          </span>

          <p className="text-sm leading-5 text-slate-600">
            Avoid strong glare, shadows and reflections.
          </p>
        </div>

        <div className="flex gap-3">
          <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-slate-100 text-xs font-semibold text-slate-700">
            4
          </span>

          <p className="text-sm leading-5 text-slate-600">
            Keep the camera steady while capturing.
          </p>
        </div>
      </div>
    </section>
  );
}

export default CaptureGuidance;