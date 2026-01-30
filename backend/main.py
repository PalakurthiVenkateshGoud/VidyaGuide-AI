from fastapi import FastAPI
from fastapi.responses import FileResponse

from backend.agent.resume_parser import extract_skills
from backend.agent.career_matcher import match_careers
from backend.agent.explainer import explain_career_fit
from backend.agent.pdf_generator import generate_roadmap_pdf

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
    # Extract skills from resume
    skills = extract_skills(resume_text)

    # Match careers based on skills
    careers = match_careers(skills)

    # Add explainable AI reasoning
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
    skills = extract_skills(resume_text)
    careers = match_careers(skills)

    for career in careers:
        career["explanation"] = explain_career_fit(
            career["role"],
            skills,
            career["missing_skills"]
        )

    file_path = generate_roadmap_pdf(careers, skills)

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="VidyaGuide_Learning_Roadmap.pdf"
    )
