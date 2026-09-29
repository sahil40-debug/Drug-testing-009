from analysis.classification import classify_reaction


def run_test(name, distance, reaction_hue, reference_hue, confidence=0.95, uniformity=0.90):
    result = classify_reaction(
        calibrated_rgb_distance=distance,
        reaction_hsv={
            "h": reaction_hue,
            "s": 120,
            "v": 220,
        },
        reference_hsv={
            "h": reference_hue,
            "s": 128,
            "v": 240,
        },
        reaction_confidence=confidence,
        reaction_uniformity=uniformity,
    )

    print(f"\n{name}")
    print("-" * 50)
    print(result)

    return result


print("=" * 60)
print("CLASSIFICATION TEST")
print("=" * 60)


# 1. Clear negative
negative = run_test(
    "TEST 1 — CLEAR NEGATIVE",
    distance=10,
    reaction_hue=27,
    reference_hue=25,
)


# 2. Clear positive
positive = run_test(
    "TEST 2 — CLEAR POSITIVE",
    distance=70,
    reaction_hue=45,
    reference_hue=25,
)


# 3. Borderline result
inconclusive = run_test(
    "TEST 3 — BORDERLINE / INCONCLUSIVE",
    distance=35,
    reaction_hue=32,
    reference_hue=25,
)


# 4. Poor reaction detection
poor_quality = run_test(
    "TEST 4 — POOR REACTION DETECTION",
    distance=70,
    reaction_hue=45,
    reference_hue=25,
    confidence=0.40,
    uniformity=0.90,
)


# 5. Poor colour uniformity
poor_uniformity = run_test(
    "TEST 5 — POOR COLOUR UNIFORMITY",
    distance=70,
    reaction_hue=45,
    reference_hue=25,
    confidence=0.95,
    uniformity=0.30,
)


print("\n")
print("=" * 60)
print("VALIDATION")
print("=" * 60)

tests_passed = 0

if negative["classification"] == "Negative":
    print("PASS — Clear negative classified correctly.")
    tests_passed += 1
else:
    print("FAIL — Clear negative.")

if positive["classification"] == "Positive":
    print("PASS — Clear positive classified correctly.")
    tests_passed += 1
else:
    print("FAIL — Clear positive.")

if inconclusive["classification"] == "Inconclusive":
    print("PASS — Borderline case classified as inconclusive.")
    tests_passed += 1
else:
    print("FAIL — Borderline case.")

if poor_quality["classification"] == "Inconclusive":
    print("PASS — Poor detection confidence rejected.")
    tests_passed += 1
else:
    print("FAIL — Poor detection confidence.")

if poor_uniformity["classification"] == "Inconclusive":
    print("PASS — Poor colour uniformity rejected.")
    tests_passed += 1
else:
    print("FAIL — Poor colour uniformity.")


print()
print(f"Tests passed: {tests_passed}/5")

if tests_passed == 5:
    print("PASS — Classification engine is working correctly.")
else:
    print("WARNING — One or more classification tests failed.")