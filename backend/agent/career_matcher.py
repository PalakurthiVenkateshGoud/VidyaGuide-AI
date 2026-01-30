def match_careers(skills):
    careers = []

    skill_set = set(skills)

    def add(role, required, optional=None):
        optional = optional or []
        matched = len(skill_set.intersection(required))
        score = int((matched / len(required)) * 100)
        missing = list(set(required) - skill_set)

        careers.append({
            "role": role,
            "match_score": score,
            "missing_skills": missing
        })

    # -------- TECH CAREERS --------
    add("Data Analyst",
        {"python", "sql", "excel", "data analysis"})

    add("Data Scientist",
        {"python", "machine learning", "statistics", "data analysis"})

    add("ML Engineer",
        {"python", "machine learning", "deep learning"})

    add("Software Developer (SDE)",
        {"python", "java", "data structures", "algorithms"})

    add("Frontend Developer",
        {"html", "css", "javascript", "react"})

    add("Backend Developer",
        {"python", "fastapi", "sql"})

    add("Full Stack Developer",
        {"html", "css", "javascript", "python", "sql"})

    # -------- BUSINESS CAREERS --------
    add("Business Analyst",
        {"business analysis", "excel", "sql"})

    add("Product Manager",
        {"product management", "strategy", "communication"})

    add("Marketing Analyst",
        {"marketing", "data analysis", "excel"})

    add("Sales Analyst",
        {"sales", "communication", "excel"})

    # -------- CIVIL / CORE --------
    add("Civil Engineer",
        {"autocad", "construction planning", "structural design"})

    add("Site Engineer",
        {"surveying", "autocad", "construction planning"})

    # -------- CREATIVE --------
    add("Video Editor",
        {"video editing", "content creation"})

    add("Photo Editor",
        {"photo editing", "graphic design"})

    add("Photographer",
        {"photography", "photo editing"})

    add("UI/UX Designer",
        {"ui ux", "graphic design"})

    add("Content Creator",
        {"content writing", "marketing"})
    
    careers = sorted(careers, key=lambda x: x["match_score"], reverse=True)


    return careers
