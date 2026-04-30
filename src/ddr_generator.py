# ---------------- IMPORTS ---------------- #
from src.reasoner import analyze_root_cause, assess_severity


# ---------------- PROPERTY SUMMARY ---------------- #
def generate_summary(inspection_obs, thermal_obs):
    if not inspection_obs and not thermal_obs:
        return "Not Available"

    summary = "The property inspection and thermal imaging survey identified multiple building performance concerns. "

    if inspection_obs:
        summary += f"{len(inspection_obs)} visible issues were recorded during the site inspection. "

    if thermal_obs:
        summary += f"Thermal imaging further detected {len(thermal_obs)} hidden performance anomalies within the structure. "

    summary += "These findings indicate underlying performance deficiencies that may affect durability and energy efficiency."

    return summary


# ---------------- AREA OBSERVATIONS ---------------- #
def generate_area_observations(inspection_obs):
    """
    Input:
    [
        {
            "page": int,
            "observation": str,
            "images": list
        }
    ]

    Output:
    [
        {
            "text": str,
            "images": list
        }
    ]
    """

    if not inspection_obs:
        return [{
            "text": "Not Available",
            "images": ["Image Not Available"]
        }]

    area_obs = []

    for obs in inspection_obs:
        text = obs.get("observation", "Not Available")
        images = obs.get("images", ["Image Not Available"])
        page = obs.get("page", "N/A")

        area_obs.append({
            "text": f"(Page {page}) {text[:1].upper() + text[1:]}",
            "images": images if images else ["Image Not Available"]
        })

    return area_obs


# ---------------- ROOT CAUSE ---------------- #
def generate_root_cause(inspection_obs, thermal_obs):
    if not inspection_obs and not thermal_obs:
        return ["Not Available"]

    root_causes = analyze_root_cause(inspection_obs, thermal_obs)

    if not root_causes:
        return ["Not Available"]

    return root_causes


# ---------------- SEVERITY ---------------- #
def generate_severity(root_causes):
    if not root_causes or root_causes == ["Not Available"]:
        return "Not Available", "Insufficient data for severity assessment"

    severity, reason = assess_severity(root_causes)

    return severity, reason


# ---------------- RECOMMENDATIONS ---------------- #
def generate_recommendations(root_causes):
    if not root_causes or root_causes == ["Not Available"]:
        return ["Further inspection required due to insufficient data."]

    actions = []

    for cause, _ in root_causes:

        if "Seepage" in cause:
            actions.append(
                "Inspect external walls and plumbing lines for leakage sources and seal all water entry points."
            )

        if "Electrical" in cause:
            actions.append(
                "Immediately inspect electrical panels and tighten or replace loose connections to prevent overheating risk."
            )

        if "Insulation" in cause:
            actions.append(
                "Install or repair insulation in affected wall/roof areas to prevent heat transfer."
            )

        if "Energy Loss" in cause:
            actions.append(
                "Seal window and door gaps and consider energy-efficient glazing solutions."
            )

    if not actions:
        actions.append(
            "Further professional inspection is recommended due to insufficient diagnostic evidence."
        )

    return list(set(actions))


# ---------------- ADDITIONAL NOTES ---------------- #
def generate_additional_notes():
    return [
        "This report is based only on the provided inspection and thermal documents.",
        "Hidden structural conditions may exist that were not visible during the inspection.",
        "Periodic monitoring is recommended."
    ]


# ---------------- MISSING INFO ---------------- #
def generate_missing_info(inspection_obs, thermal_obs):
    missing = []

    if not inspection_obs:
        missing.append("Detailed site inspection observations: Not Available")

    if not thermal_obs:
        missing.append("Thermal imaging data: Not Available")

    if not missing:
        return ["None"]

    return missing


# ---------------- FULL DDR BUILDER ---------------- #
def build_ddr(inspection_obs, thermal_obs):
    """
    Combines all sections into final structured DDR dictionary
    """

    summary = generate_summary(inspection_obs, thermal_obs)
    area_obs = generate_area_observations(inspection_obs)
    root_causes = generate_root_cause(inspection_obs, thermal_obs)
    severity, severity_reason = generate_severity(root_causes)
    recommendations = generate_recommendations(root_causes)
    notes = generate_additional_notes()
    missing_info = generate_missing_info(inspection_obs, thermal_obs)

    return {
        "summary": summary,
        "area_observations": area_obs,
        "root_causes": root_causes,
        "severity": {
            "level": severity,
            "reason": severity_reason
        },
        "recommendations": recommendations,
        "additional_notes": notes,
        "missing_info": missing_info
    }