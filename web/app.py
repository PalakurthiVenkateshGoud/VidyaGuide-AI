from flask import Flask, render_template_string, request, send_file
import requests
import io

app = Flask(__name__)

# 🔗 Your deployed FastAPI backend
BACKEND_URL = "https://vidyaguide-backend.onrender.com"

# -------------------------------
# HTML TEMPLATE (INLINE FOR SPEED)
# -------------------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>VidyaGuide AI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
            padding: 40px;
        }
        h1 { color: #38bdf8; }
        textarea {
            width: 100%;
            height: 180px;
            padding: 12px;
            font-size: 14px;
            border-radius: 8px;
        }
        button {
            margin-top: 12px;
            padding: 12px 20px;
            font-size: 15px;
            background: #38bdf8;
            border: none;
            border-radius: 6px;
            cursor: pointer;
        }
        .card {
            background: #020617;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .info {
            background: #1e3a8a;
            padding: 12px;
            border-radius: 6px;
            margin-top: 10px;
        }
        .warning {
            background: #78350f;
            padding: 12px;
            border-radius: 6px;
            margin-top: 10px;
        }
        .success {
            background: #064e3b;
            padding: 12px;
            border-radius: 6px;
            margin-top: 10px;
        }
        a {
            color: #38bdf8;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>

<body>

<h1>🎓 VidyaGuide AI Agent</h1>
<p>Your personal career planning & skill mentor</p>

<form method="POST">
    <textarea name="resume_text" placeholder="Paste your resume or skills here...">{{ resume_text }}</textarea>
    <br>
    <button type="submit">🔍 Analyze Career Path</button>
</form>

{% if error %}
    <div class="warning">{{ error }}</div>
{% endif %}

{% if skills %}
    <div class="card">
        <h2>🧠 Skills Identified</h2>
        <p>{{ skills | join(", ") if skills else "No clear skills detected." }}</p>
    </div>
{% endif %}

{% if careers %}
    <div class="card">
        <h2>🎯 Career Recommendations</h2>

        {% for c in careers %}
            <h3>{{ c.role }} — {{ c.match_score }}%</h3>

            {% if c.missing_skills %}
                <p>❌ Missing: {{ c.missing_skills | join(", ") }}</p>
            {% else %}
                <p>✅ Fully matched</p>
            {% endif %}

            <div class="info">{{ c.explanation }}</div>
            <hr>
        {% endfor %}
    </div>

    <div class="card">
        <h2>⬇️ Download Learning Roadmap</h2>
        <a href="/download">📄 Download PDF Roadmap</a>
    </div>
{% endif %}

<footer style="margin-top:40px; opacity:0.7;">
    Powered by VidyaGuide AI 🚀
</footer>

</body>
</html>
"""

# -------------------------------
# ROUTES
# -------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    resume_text = ""
    skills = []
    careers = []
    error = None

    if request.method == "POST":
        resume_text = request.form.get("resume_text", "").strip()

        if not resume_text:
            error = "Please paste your resume or skills."
        else:
            try:
                res = requests.post(
                    f"{BACKEND_URL}/analyze",
                    params={"resume_text": resume_text},
                    timeout=60
                )
                res.raise_for_status()
                data = res.json()
                skills = data.get("skills_found", [])
                careers = data.get("career_recommendations", [])

            except Exception:
                error = "Backend is not reachable. Please try again later."

    return render_template_string(
        HTML,
        resume_text=resume_text,
        skills=skills,
        careers=careers,
        error=error
    )

# -------------------------------
# PDF DOWNLOAD
# -------------------------------
@app.route("/download")
def download():
    resume_text = request.args.get("resume_text", "")

    try:
        res = requests.post(
            f"{BACKEND_URL}/download-roadmap",
            params={"resume_text": resume_text},
            timeout=60
        )
        res.raise_for_status()

        return send_file(
            io.BytesIO(res.content),
            mimetype="application/pdf",
            as_attachment=True,
            download_name="VidyaGuide_Learning_Roadmap.pdf"
        )

    except Exception:
        return "PDF generation failed.", 500


# -------------------------------
# RUN SERVER (IMPORTANT)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
