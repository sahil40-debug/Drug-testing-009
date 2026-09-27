function ReferenceCardGuide() {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-base font-semibold text-slate-900">
            Reference Colour Card
          </h2>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            Keep the complete reference card visible in the camera frame.
            It will be used to compensate for lighting conditions.
          </p>
        </div>

        <span className="ml-3 rounded-full bg-amber-50 px-2.5 py-1 text-xs font-medium text-amber-700">
          Required
        </span>
      </div>

      <div className="mt-4 rounded-lg border border-dashed border-slate-300 bg-slate-50 p-4">
        <div className="grid grid-cols-5 gap-1.5">
          <div className="h-7 rounded bg-slate-200" />
          <div className="h-7 rounded bg-slate-300" />
          <div className="h-7 rounded bg-slate-400" />
          <div className="h-7 rounded bg-slate-500" />
          <div className="h-7 rounded bg-slate-600" />
        </div>

        <p className="mt-3 text-center text-xs text-slate-500">
          Reference card preview
        </p>
      </div>
    </section>
  );
}

export default ReferenceCardGuide;