from fastapi import FastAPI
from fastapi.responses import FileResponse

from agent.resume_parser import extract_skills
from agent.career_matcher import match_careers
from agent.explainer import explain_career_fit
from agent.pdf_generator import generate_roadmap_pdf  # ✅ FIXED

app = FastAPI(
    title="VidyaGuide AI Agent",
    description="Career Planning & Skill Recommendation System",
    version="1.0"
)

# -------------------------------
# Resume Analysis Endpoint
# -------------------------------
@app.post("/analyze")
def analyze_resume(resume_text: str):

    # 1️⃣ Extract skills
    skills = extract_skills(resume_text)

    # 2️⃣ Match careers
    careers = match_careers(skills)

    # 3️⃣ Add explanations
    for career in careers:
        career["explanation"] = explain_career_fit(
            career["role"],
            skills,
            career["missing_skills"]
        )

    return {
        "skills_found": skills,
        "career_recommendations": careers
    }


# -------------------------------
# Download Learning Roadmap PDF
# -------------------------------
@app.post("/download-roadmap")
def download_roadmap(resume_text: str):

    # 1️⃣ Re-run analysis (IMPORTANT)
    skills = extract_skills(resume_text)
    careers = match_careers(skills)

    for career in careers:
        career["explanation"] = explain_career_fit(
            career["role"],
            skills,
            career["missing_skills"]
        )

    # 2️⃣ Generate PDF
    file_path = generate_roadmap_pdf(
        careers=careers,
        skills=skills
    )

    # 3️⃣ Return file
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="VidyaGuide_Learning_Roadmap.pdf"
    )
