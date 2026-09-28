import { useState } from "react";

export interface ReferenceColor {
  name: string;
  value: string;
}

interface ColorGroup {
  name: string;
  shades: ReferenceColor[];
}
interface ReferenceColorSelectorProps {
  selectedGroup: string | null;
  selectedColor: ReferenceColor | null;
  setSelectedGroup: (group: string | null) => void;
  setSelectedColor: (color: ReferenceColor | null) => void;
}

function ReferenceColorSelector({
  selectedGroup,
  selectedColor,
  setSelectedGroup,
  setSelectedColor,
}: ReferenceColorSelectorProps) {
  const [showInfo, setShowInfo] = useState(false);
  const [isConfirmed, setIsConfirmed] = useState(false);

const colorGroups: ColorGroup[] = [
  {
    name: "Red",
    shades: [
      { name: "Very Pale Red", value: "#FEE2E2" },
      { name: "Pale Red", value: "#FECACA" },
      { name: "Light Red", value: "#FCA5A5" },
      { name: "Soft Red", value: "#F87171" },
      { name: "Red", value: "#EF4444" },
      { name: "Strong Red", value: "#DC2626" },
      { name: "Dark Red", value: "#B91C1C" },
      { name: "Deep Red", value: "#7F1D1D" },
    ],
  },
  {
    name: "Orange",
    shades: [
      { name: "Very Pale Orange", value: "#FFF7ED" },
      { name: "Pale Orange", value: "#FFEDD5" },
      { name: "Light Orange", value: "#FED7AA" },
      { name: "Soft Orange", value: "#FDBA74" },
      { name: "Orange", value: "#F97316" },
      { name: "Strong Orange", value: "#EA580C" },
      { name: "Dark Orange", value: "#C2410C" },
      { name: "Deep Orange", value: "#7C2D12" },
    ],
  },
  {
    name: "Yellow",
    shades: [
      { name: "Very Pale Yellow", value: "#FEFCE8" },
      { name: "Pale Yellow", value: "#FEF9C3" },
      { name: "Light Yellow", value: "#FEF08A" },
      { name: "Soft Yellow", value: "#FDE047" },
      { name: "Yellow", value: "#EAB308" },
      { name: "Strong Yellow", value: "#CA8A04" },
      { name: "Dark Yellow", value: "#A16207" },
      { name: "Deep Yellow", value: "#713F12" },
    ],
  },
  {
    name: "Green",
    shades: [
      { name: "Very Pale Green", value: "#F0FDF4" },
      { name: "Pale Green", value: "#DCFCE7" },
      { name: "Light Green", value: "#BBF7D0" },
      { name: "Soft Green", value: "#86EFAC" },
      { name: "Green", value: "#22C55E" },
      { name: "Strong Green", value: "#16A34A" },
      { name: "Dark Green", value: "#15803D" },
      { name: "Deep Green", value: "#14532D" },
    ],
  },
  {
    name: "Cyan",
    shades: [
      { name: "Very Pale Cyan", value: "#ECFEFF" },
      { name: "Pale Cyan", value: "#CFFAFE" },
      { name: "Light Cyan", value: "#A5F3FC" },
      { name: "Soft Cyan", value: "#67E8F9" },
      { name: "Cyan", value: "#06B6D4" },
      { name: "Strong Cyan", value: "#0891B2" },
      { name: "Dark Cyan", value: "#0E7490" },
      { name: "Deep Cyan", value: "#164E63" },
    ],
  },
  {
    name: "Blue",
    shades: [
      { name: "Very Pale Blue", value: "#EFF6FF" },
      { name: "Pale Blue", value: "#DBEAFE" },
      { name: "Light Blue", value: "#BFDBFE" },
      { name: "Soft Blue", value: "#93C5FD" },
      { name: "Blue", value: "#3B82F6" },
      { name: "Strong Blue", value: "#2563EB" },
      { name: "Dark Blue", value: "#1D4ED8" },
      { name: "Deep Blue", value: "#1E3A8A" },
    ],
  },
  {
    name: "Purple",
    shades: [
      { name: "Very Pale Purple", value: "#FAF5FF" },
      { name: "Pale Purple", value: "#F3E8FF" },
      { name: "Light Purple", value: "#E9D5FF" },
      { name: "Soft Purple", value: "#D8B4FE" },
      { name: "Purple", value: "#A855F7" },
      { name: "Strong Purple", value: "#9333EA" },
      { name: "Dark Purple", value: "#7E22CE" },
      { name: "Deep Purple", value: "#581C87" },
    ],
  },
  {
    name: "Pink",
    shades: [
      { name: "Very Pale Pink", value: "#FDF2F8" },
      { name: "Pale Pink", value: "#FCE7F3" },
      { name: "Light Pink", value: "#FBCFE8" },
      { name: "Soft Pink", value: "#F9A8D4" },
      { name: "Pink", value: "#EC4899" },
      { name: "Strong Pink", value: "#DB2777" },
      { name: "Dark Pink", value: "#BE185D" },
      { name: "Deep Pink", value: "#831843" },
    ],
  },
  {
    name: "Brown",
    shades: [
      { name: "Very Light Brown", value: "#F5E6D3" },
      { name: "Light Brown", value: "#E7C9A9" },
      { name: "Soft Brown", value: "#D6A77A" },
      { name: "Medium Brown", value: "#B7794B" },
      { name: "Brown", value: "#92400E" },
      { name: "Strong Brown", value: "#854D0E" },
      { name: "Dark Brown", value: "#78350F" },
      { name: "Deep Brown", value: "#451A03" },
    ],
  },
  {
    name: "Gray",
    shades: [
      { name: "Very Light Gray", value: "#F8FAFC" },
      { name: "Pale Gray", value: "#F1F5F9" },
      { name: "Light Gray", value: "#E2E8F0" },
      { name: "Soft Gray", value: "#CBD5E1" },
      { name: "Gray", value: "#94A3B8" },
      { name: "Strong Gray", value: "#64748B" },
      { name: "Dark Gray", value: "#475569" },
      { name: "Deep Gray", value: "#1E293B" },
    ],
  },
  {
    name: "Black",
    shades: [
      { name: "Near White", value: "#F8FAFC" },
      { name: "Very Light Black", value: "#E2E8F0" },
      { name: "Light Black", value: "#CBD5E1" },
      { name: "Soft Black", value: "#64748B" },
      { name: "Dark Gray", value: "#475569" },
      { name: "Very Dark Gray", value: "#334155" },
      { name: "Near Black", value: "#1F2937" },
      { name: "Black", value: "#111827" },
    ],
  },
  {
    name: "White",
    shades: [
      { name: "Warm White", value: "#FFFBEB" },
      { name: "Cream White", value: "#FEFCE8" },
      { name: "Soft White", value: "#F8FAFC" },
      { name: "Cool White", value: "#F1F5F9" },
      { name: "White", value: "#FFFFFF" },
      { name: "Bright White", value: "#FEFEFE" },
      { name: "Pure White", value: "#FFFFFF" },
      { name: "Neutral White", value: "#FAFAFA" },
    ],
  },
];


  const group = colorGroups.find(
    (item) => item.name === selectedGroup
  );

  const handleDone = () => {
  if (!selectedColor || !selectedGroup) return;

  console.log("Reference colour confirmed:", {
    colorGroup: selectedGroup,
    shade: selectedColor.name,
    value: selectedColor.value,
  });

  setIsConfirmed(true);
};

  const changeColour = () => {
  setSelectedGroup(null);
  setSelectedColor(null);
  setIsConfirmed(false);
};

  const changeShade = () => {
  setSelectedColor(null);
  setIsConfirmed(false);
};

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      {/* Header */}
      <div className="mb-5 flex items-start justify-between gap-4">
        <div>
          <h2 className="text-base font-semibold text-slate-900">
            Reference Colour Card
          </h2>

          <p className="mt-1 text-xs leading-5 text-slate-500">
            Select the colour family and then choose the closest matching
            reference shade.
          </p>
        </div>

        <button
          type="button"
          onClick={() => setShowInfo(!showInfo)}
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-slate-200 text-sm font-semibold text-slate-500 transition hover:border-blue-300 hover:bg-blue-50 hover:text-blue-600"
          title="About reference colour cards"
        >
          i
        </button>
      </div>

      {/* Information panel */}
      {showInfo && (
        <div className="mb-5 rounded-lg border border-blue-100 bg-blue-50 p-4">
          <h3 className="text-sm font-semibold text-blue-900">
            Why use a reference colour card?
          </h3>

          <div className="mt-2 space-y-2 text-xs leading-5 text-blue-900/80">
            <p>
              Lighting conditions can change how colours appear in a
              photograph. A reference colour card provides known colour
              references inside the captured frame.
            </p>

            <p>
              The system can later use these references to estimate colour
              differences caused by the camera and lighting conditions before
              analysing the test reaction.
            </p>

            <p>
              The selected reference colour and shade are stored with the test
              information so the analysis pipeline knows which reference was
              selected.
            </p>

            <p>
              The reference card is used as a calibration aid. It does not
              itself determine whether a test is positive or negative.
            </p>
          </div>
        </div>
      )}

      {/* Colour family selection */}
      {!selectedGroup && (
        <div>
          <div className="mb-3">
            <p className="text-sm font-medium text-slate-700">
              1. Choose a colour
            </p>
            <p className="mt-1 text-xs text-slate-500">
              Select the colour family closest to the reference shade.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-6">
            {colorGroups.map((color) => {
              const previewColor = color.shades[
                Math.floor(color.shades.length / 2)
              ].value;

              return (
                <button
                  key={color.name}
                  type="button"
                  onClick={() => setSelectedGroup(color.name)}
                  className="overflow-hidden rounded-lg border border-slate-200 bg-white text-left transition hover:border-blue-400 hover:shadow-sm"
                >
                  <div
                    className="h-12 w-full"
                    style={{ backgroundColor: previewColor }}
                  />

                  <div className="p-2.5">
                    <p className="text-xs font-medium text-slate-700">
                      {color.name}
                    </p>
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Shade selection */}
      {selectedGroup && !selectedColor && group && (
        <div>
          <div className="mb-4 flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-700">
                2. Choose the exact shade
              </p>

              <p className="mt-1 text-xs text-slate-500">
                {selectedGroup} — select the shade that most closely matches
                your reference.
              </p>
            </div>

            <button
              type="button"
              onClick={changeColour}
              className="text-xs font-medium text-blue-600 hover:text-blue-700"
            >
              Change Colour
            </button>
          </div>

          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5">
            {group.shades.map((shade) => (
              <button
                key={shade.name}
                type="button"
                onClick={() => setSelectedColor(shade)}
                className="overflow-hidden rounded-lg border border-slate-200 bg-white text-left transition hover:border-blue-400 hover:shadow-sm"
              >
                <div
                  className="h-20 w-full"
                  style={{ backgroundColor: shade.value }}
                />

                <div className="p-2.5">
                  <p className="text-xs font-medium text-slate-700">
                    {shade.name}
                  </p>

                  <p className="mt-1 font-mono text-[10px] text-slate-400">
                    {shade.value}
                  </p>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Selected shade */}
      {selectedColor && selectedGroup && (
        <div>
          <div className="mb-4 flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-700">
                Selected reference
              </p>
            </div>

            <span className="rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700">
              Selected
            </span>
          </div>

          <div className="flex items-center gap-4 rounded-lg border border-slate-200 bg-slate-50 p-4">
            <div
              className="h-16 w-16 shrink-0 rounded-lg border border-slate-300 shadow-sm"
              style={{ backgroundColor: selectedColor.value }}
            />

            <div className="min-w-0">
              <p className="text-sm font-semibold text-slate-900">
                {selectedGroup}
              </p>

              <p className="mt-1 text-sm text-slate-600">
                {selectedColor.name}
              </p>

              <p className="mt-1 font-mono text-xs text-slate-400">
                {selectedColor.value}
              </p>
            </div>
          </div>

          <div className="mt-4 flex gap-3">
            <button
              type="button"
              onClick={changeColour}
              className="flex-1 rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              Change Colour
            </button>

            <button
              type="button"
              onClick={changeShade}
              className="flex-1 rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              Change Shade
            </button>

            <button
              type="button"
              onClick={handleDone}
              className="flex-1 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700"
            >
                {isConfirmed ? "Confirmed ✓" : "Done"}
            </button>
          </div>
        </div>
      )}
    </section>
  );
}

export default ReferenceColorSelector;