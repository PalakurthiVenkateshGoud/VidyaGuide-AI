def explain_career_fit(role, skills, missing_skills):
    if not missing_skills:
        return (
            f"You are a strong fit for the {role} role because your current "
            f"skills align well with the core requirements of this career."
        )

    return (
        f"The {role} role matches your profile based on skills like "
        f"{', '.join(skills[:3])}. To become fully job-ready, you should "
        f"focus on improving {', '.join(missing_skills)}."
    )
