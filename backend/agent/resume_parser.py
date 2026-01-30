from backend.data.skills_data import SKILL_LIST

def extract_skills(resume_text: str):
    text = resume_text.lower()
    return [skill for skill in SKILL_LIST if skill in text]
from backend.data.skills_data import SKILL_LIST

def extract_skills(resume_text: str):
    text = resume_text.lower()
    return [skill for skill in SKILL_LIST if skill in text]
