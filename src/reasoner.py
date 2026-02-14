# Root Cause Decider
def analyze_root_cause(inspection_obs, thermal_obs):

    conclusions = []

    inspection_text = " ".join(inspection_obs).lower()
    thermal_text = " ".join(thermal_obs).lower()

    # ---- Moisture / Seepage ----
    if ("leak" in inspection_text or "damp" in inspection_text) and \
       ("moisture" in thermal_text or "air leakage" in thermal_text):
        conclusions.append(
            ("Water Seepage Likely",
             "Moisture patterns in thermal imaging align with leakage observed during inspection.")
        )

    # ---- Electrical Fault ----
    if ("hot" in inspection_text or "overheating" in inspection_text) and \
       ("energy loss" not in thermal_text):
        conclusions.append(
            ("Electrical Loose Connection",
             "Hot spots indicate probable loose electrical termination or overload condition.")
        )

    # ---- Insulation Failure ----
    if "insulation failure" in thermal_text or "thermal bridging" in thermal_text:
        conclusions.append(
            ("Building Insulation Deficiency",
             "Thermal imaging indicates heat transfer through building envelope due to insulation gaps.")
        )

    # ---- Window / Envelope Loss ----
    if "window" in thermal_text or "energy loss" in thermal_text:
        conclusions.append(
            ("Building Envelope Energy Loss",
             "Heat escaping through openings such as windows/doors suggests sealing inefficiency.")
        )

    if not conclusions:
        conclusions.append(
            ("Inconclusive",
             "Available information insufficient to determine a confident root cause.")
        )

    return conclusions


def assess_severity(root_causes):

    severity_rank = 0
    reasoning = "Minor defects with limited immediate impact."

    for cause, _ in root_causes:

        # HIGH RISK
        if "Electrical" in cause:
            severity_rank = max(severity_rank, 3)
            reasoning = "Electrical faults pose fire and safety hazards."

        # MEDIUM RISK
        elif "Seepage" in cause:
            severity_rank = max(severity_rank, 2)
            reasoning = "Water ingress can weaken materials and cause mold growth."

        elif "Insulation" in cause:
            severity_rank = max(severity_rank, 2)
            reasoning = "Insulation defects indicate building envelope deterioration."

        # LOW RISK
        elif "Energy Loss" in cause:
            severity_rank = max(severity_rank, 1)
            reasoning = "Energy inefficiency impacts comfort but not structural safety."

    if severity_rank == 3:
        return "High", reasoning
    elif severity_rank == 2:
        return "Medium", reasoning
    else:
        return "Low", reasoning