import streamlit as st
import requests

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="VidyaGuide AI Agent",
    layout="centered"
)

# --------------------------------
# Header
# --------------------------------
st.title("🎓 VidyaGuide AI Agent")
st.caption("Your personal career planning & skill mentor")

st.markdown("---")

# --------------------------------
# Resume Input
# --------------------------------
resume_text = st.text_area(
    "📄 Paste your resume text below",
    height=200,
    placeholder="Example: I have experience in Python, SQL, Excel..."
)

# --------------------------------
# Analyze Button
# --------------------------------
if st.button("🔍 Analyze Career Path"):

    if resume_text.strip() == "":
        st.warning("Please paste your resume text.")
    else:
        with st.spinner("Analyzing your profile..."):
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                params={"resume_text": resume_text}
            )

        data = response.json()

        st.success("Analysis Complete!")
        st.markdown("---")

        # --------------------------------
        # Skills Identified
        # --------------------------------
        st.subheader("🧠 Skills Identified")
        st.write(", ".join(data["skills_found"]))

        st.markdown("---")

        # --------------------------------
        # Career Recommendations
        # --------------------------------
        st.subheader("🎯 Career Recommendations")

        for career in data["career_recommendations"]:
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
        # Download PDF Roadmap (BEST PRACTICE)
        # --------------------------------
        st.subheader("⬇️ Download Learning Roadmap")

        pdf_response = requests.post(
            "http://127.0.0.1:8000/download-roadmap",
            params={"resume_text": resume_text}
        )

        st.download_button(
            label="📄 Download Personalized PDF Roadmap",
            data=pdf_response.content,
            file_name="VidyaGuide_Learning_Roadmap.pdf",
            mime="application/pdf"
        )

        

# --------------------------------
# Footer
# --------------------------------
st.caption("Powered by VidyaGuide AI Agent")
