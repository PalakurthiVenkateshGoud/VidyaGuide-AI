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

    if resume_text.strip() == "":
        st.warning("Please paste your resume text.")
    else:
        with st.spinner("Analyzing your profile..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/analyze",
                    params={"resume_text": resume_text},
                    timeout=60
                )
                response.raise_for_status()
                data = response.json()

            except Exception as e:
                st.error("Backend is not reachable. Please try again later.")
                st.stop()

        # --------------------------------
        # RESULTS
        # --------------------------------
        st.success("Analysis Complete!")
        st.markdown("---")

        # --------------------------------
        # SKILLS
        # --------------------------------
        st.subheader("🧠 Skills Identified")
        st.write(", ".join(data.get("skills_found", [])))

        st.markdown("---")

        # --------------------------------
        # CAREER RECOMMENDATIONS
        # --------------------------------
        st.subheader("🎯 Career Recommendations")

        for career in data.get("career_recommendations", []):

            st.markdown(f"### {career['role']}")
            st.progress(career["match_score"] / 100)
            st.write(f"Match Score: **{career['match_score']}%**")

            if career["missing_skills"]:
                st.write("❌ Missing Skills:", ", ".join(career["missing_skills"]))
            else:
                st.write("✅ Fully matched for this role")

            # Explainable AI (blue box)
            st.info(career["explanation"])
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

        except Exception:
            st.error("Could not generate PDF at the moment.")

# --------------------------------
# FOOTER
# --------------------------------
st.caption("Powered by VidyaGuide AI Agent 🚀")
