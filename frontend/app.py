import streamlit as st
import requests

# --------------------------------
# CONFIG
# --------------------------------
BACKEND_URL = "https://vidyaguide-backend.onrender.com"

st.set_page_config(
    page_title="VidyaGuide AI Agent",
    layout="centered"
)

# --------------------------------
# HEADER
# --------------------------------
st.title("🎓 VidyaGuide AI Agent")
st.caption("Your personal career planning & skill mentor")
st.markdown("---")

# --------------------------------
# RESUME INPUT
# --------------------------------
resume_text = st.text_area(
    "📄 Paste your resume text below",
    height=220,
    placeholder="Example: I have experience in Python, SQL, Excel, data analysis..."
)

# --------------------------------
# ANALYZE BUTTON
# --------------------------------
if st.button("🔍 Analyze Career Path"):

    if not resume_text.strip():
        st.warning("Please paste your resume text.")
        st.stop()

    with st.spinner("Analyzing your profile..."):
        try:
            response = requests.post(
                f"{BACKEND_URL}/analyze",
                params={"resume_text": resume_text},
                timeout=60
            )
            response.raise_for_status()
            data = response.json()

        except requests.exceptions.RequestException:
            st.error("❌ Backend is not reachable. Please try again later.")
            st.stop()

    # --------------------------------
    # RESULTS
    # --------------------------------
    st.success("Analysis Complete!")
    st.markdown("---")

    # --------------------------------
    # SKILLS IDENTIFIED
    # --------------------------------
    st.subheader("🧠 Skills Identified")

    skills = data.get("skills_found", [])
    if skills:
        st.write(", ".join(skills))
    else:
        st.write("No clear skills detected.")

    st.markdown("---")

    # --------------------------------
    # CAREER RECOMMENDATIONS
    # --------------------------------
    st.subheader("🎯 Career Recommendations")

    careers = data.get("career_recommendations", [])

    if not careers:
        st.warning("No career recommendations found.")
    else:
        for career in careers:
            st.markdown(f"### {career['role']}")

            score = career.get("match_score", 0)
            st.progress(score / 100)
            st.write(f"Match Score: **{score}%**")

            missing = career.get("missing_skills", [])
            if missing:
                st.write("❌ Missing Skills:", ", ".join(missing))
            else:
                st.write("✅ Fully matched for this role")

            # Explainable AI (blue info box)
            explanation = career.get("explanation", "")
            if explanation:
                st.info(explanation)

            st.markdown("---")

    # --------------------------------
    # DOWNLOAD PDF ROADMAP
    # --------------------------------
    st.subheader("⬇️ Download Learning Roadmap")

    try:
        pdf_response = requests.post(
            f"{BACKEND_URL}/download-roadmap",
            params={"resume_text": resume_text},
            timeout=60
        )
        pdf_response.raise_for_status()

        st.download_button(
            label="📄 Download Personalized PDF Roadmap",
            data=pdf_response.content,
            file_name="VidyaGuide_Learning_Roadmap.pdf",
            mime="application/pdf"
        )

    except requests.exceptions.RequestException:
        st.error("❌ Could not generate PDF at the moment.")

# --------------------------------
# FOOTER
# --------------------------------
st.caption("Powered by VidyaGuide AI Agent 🚀")
