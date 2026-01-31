from fastapi import FastAPI
from fastapi.responses import FileResponse

from agent.resume_parser import extract_skills
from agent.career_matcher import match_careers
from agent.explainer import explain_career_fit
from agent.pdf_generator import generate_roadmap_pdf  # ✅ FIXED

import random

NO_SKILL_QUOTES = [
    "Everyone starts somewhere. Skills are built, not born.",
    "Your journey hasn’t failed — it just hasn’t started yet.",
    "Lack of skills today is the best place to begin learning tomorrow.",
    "No skills detected yet, but potential is unlimited.",
    "Every expert was once a beginner."
]

NO_MATCH_QUOTES = [
    "Your current skills are a starting point, not a limitation.",
    "Upskilling is the bridge between where you are and where you want to be.",
    "Careers are built step by step — learning is your next step.",
    "Your profile shows curiosity. Now it’s time to build depth.",
    "The best investment you can make right now is learning."
]

def get_no_skill_message():
    return {
        "title": "No skills detected yet",
        "quote": random.choice(NO_SKILL_QUOTES),
        "suggestion": "Start by learning foundational skills like Python, Excel, Communication, or Problem Solving."
    }

def get_no_match_message(skills):
    return {
        "title": "Skills detected, but no strong career match yet",
        "quote": random.choice(NO_MATCH_QUOTES),
        "suggestion": f"Based on your skills ({', '.join(skills)}), we recommend focused upskilling to unlock career paths."
    }


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
    skills = extract_skills(resume_text)

    # ❗ No skills found at all
    if not skills:
        return {
            "skills_found": [],
            "career_recommendations": [],
            "message": get_no_skill_message()
        }

    careers = match_careers(skills)

    # ❗ Skills exist but no career matches
    if not careers:
        return {
            "skills_found": skills,
            "career_recommendations": [],
            "message": get_no_match_message(skills)
        }

    for career in careers:
        career["explanation"] = explain_career_fit(
            career["role"],
            skills,
            career["missing_skills"]
        )

    return {
        "skills_found": skills,
        "career_recommendations": careers,
        "message": None
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
