from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_roadmap_pdf(careers, skills, filename="learning_roadmap.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 40

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, y, "VidyaGuide AI – Career Roadmap")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(40, y, f"Skills Identified: {', '.join(skills)}")
    y -= 30

    # Career Recommendations
    for idx, career in enumerate(careers[:5], start=1):
        if y < 120:
            c.showPage()
            y = height - 40
            c.setFont("Helvetica", 11)

        c.setFont("Helvetica-Bold", 13)
        c.drawString(40, y, f"{idx}. {career['role']}")
        y -= 18

        c.setFont("Helvetica", 11)
        c.drawString(60, y, f"Match Score: {career['match_score']}%")
        y -= 15

        if career["missing_skills"]:
            c.drawString(
                60,
                y,
                f"Skills to Improve: {', '.join(career['missing_skills'])}"
            )
            y -= 15
        else:
            c.drawString(60, y, "Fully matched for this role")
            y -= 15

        y -= 10

    c.save()
    return filename
