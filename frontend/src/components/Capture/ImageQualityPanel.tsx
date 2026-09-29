interface ImageQualityPanelProps {
  qualityResult: any;
}

function ImageQualityPanel({
  qualityResult,
}: ImageQualityPanelProps) {
  const getStatus = (
    passed: boolean | undefined,
    hasResult: boolean
  ) => {
    if (!hasResult) {
      return {
        label: "Waiting",
        className:
          "bg-slate-100 text-slate-500",
      };
    }

    return passed
      ? {
          label: "Passed",
          className:
            "bg-green-50 text-green-700",
        }
      : {
          label: "Needs attention",
          className:
            "bg-red-50 text-red-700",
        };
  };

  const hasResult =
    qualityResult?.success === true &&
    qualityResult?.checks;

  const referenceCardStatus = getStatus(
    undefined,
    false
  );

  const sharpnessStatus = getStatus(
    qualityResult?.checks?.sharpness?.passed,
    hasResult
  );

  const lightingStatus = getStatus(
    qualityResult?.checks?.brightness?.passed,
    hasResult
  );

  const exposureStatus = getStatus(
    qualityResult?.checks?.exposure?.passed,
    hasResult
  );

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="mb-4">
        <h2 className="text-base font-semibold text-slate-900">
          Image Quality
        </h2>

        <div className="mt-2 flex items-center gap-2">
  <span className="text-xs text-slate-500">
    Overall quality
  </span>

  <span className="text-sm font-semibold text-slate-900">
    {qualityResult?.quality_score ?? "--"}/100
  </span>

  {qualityResult?.quality && (
    <span
      className={`rounded-full px-2 py-0.5 text-xs font-medium ${
        qualityResult.quality === "good"
          ? "bg-green-50 text-green-700"
          : qualityResult.quality === "acceptable"
          ? "bg-yellow-50 text-yellow-700"
          : "bg-red-50 text-red-700"
      }`}
    >
      {qualityResult.quality}
    </span>
  )}
</div>
      </div>

      <div className="space-y-3">

        {/* Reference card */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">
            Reference card
          </span>

          <span
            className={`rounded-full px-2.5 py-1 text-xs font-medium ${referenceCardStatus.className}`}
          >
            {referenceCardStatus.label}
          </span>
        </div>

        {/* Sharpness */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">
            Image sharpness
          </span>

          <span
            className={`rounded-full px-2.5 py-1 text-xs font-medium ${sharpnessStatus.className}`}
          >
            {sharpnessStatus.label}
          </span>
        </div>

        {/* Lighting */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">
            Lighting
          </span>

          <span
            className={`rounded-full px-2.5 py-1 text-xs font-medium ${lightingStatus.className}`}
          >
            {lightingStatus.label}
          </span>
        </div>

        {/* Exposure / shadows */}
        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-600">
            Exposure
          </span>

          <span
            className={`rounded-full px-2.5 py-1 text-xs font-medium ${exposureStatus.className}`}
          >
            {exposureStatus.label}
          </span>
        </div>

      </div>

      {/* Overall message */}
      {hasResult && (
        <div
          className={`mt-5 rounded-lg p-3 text-xs leading-5 ${
            qualityResult.quality === "acceptable"
              ? "bg-green-50 text-green-700"
              : "bg-red-50 text-red-700"
          }`}
        >
          {qualityResult.message}
        </div>
      )}
    </section>
  );
}

export default ImageQualityPanel;