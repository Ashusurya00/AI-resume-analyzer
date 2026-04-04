import streamlit as st
from utils.parser import extract_text_from_pdf
from utils.skills import extract_skills
from utils.matcher import calculate_match
from utils.llm_analyzer import analyze_resume
from utils.pdf_generator import generate_pdf

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #00ADB5;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
.metric-card {
    background-color: #222831;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ---------------- #
st.markdown('<p class="main-title">📄 AI Resume Analyzer</p>', unsafe_allow_html=True)
st.caption("🚀 Analyze resumes with AI-powered insights & matching")

st.divider()

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.header("⚙️ Settings")
    show_skills = st.toggle("Show Skills Breakdown", True)
    show_ai = st.toggle("Show AI Feedback", True)

    st.markdown("---")
    st.subheader("💡 Tips")
    st.write("• Use real job descriptions")
    st.write("• Upload clean resume PDFs")

# ---------------- INPUT SECTION ---------------- #
col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"])

with col2:
    job_description = st.text_area("📝 Paste Job Description")

# ---------------- BUTTON ---------------- #
analyze_btn = st.button("🚀 Analyze Resume", use_container_width=True)

# ---------------- MAIN LOGIC ---------------- #
if analyze_btn:

    if resume_file and job_description:

        with st.spinner("🤖 AI is analyzing your resume..."):

            resume_text = extract_text_from_pdf(resume_file)

            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(job_description)

            score, matched = calculate_match(resume_skills, jd_skills)
            missing = list(set(jd_skills) - set(resume_skills))

            analysis = analyze_resume(resume_text, job_description)

        st.success("✅ Analysis Complete")

        # ---------------- TABS ---------------- #
        tab1, tab2 = st.tabs(["📊 Dashboard", "🤖 AI Feedback"])

        # ---------------- DASHBOARD TAB ---------------- #
        with tab1:

            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Match Score", f"{score}%")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.metric("Skills Found", len(matched))
                st.markdown('</div>', unsafe_allow_html=True)

            if show_skills:
                st.markdown("### ✅ Matched Skills")
                st.markdown(f'<div class="card">{", ".join(matched) if matched else "No matching skills"}</div>', unsafe_allow_html=True)

                st.markdown("### ❌ Missing Skills")
                st.markdown(f'<div class="card">{", ".join(missing) if missing else "No missing skills"}</div>', unsafe_allow_html=True)

        # ---------------- AI TAB ---------------- #
        with tab2:
            if show_ai:
                st.markdown("### 🤖 AI Feedback")
                st.markdown(f'<div class="card">{analysis}</div>', unsafe_allow_html=True)

                # PDF Download
                pdf_file = generate_pdf(analysis)

                with open(pdf_file, "rb") as f:
                    st.download_button(
                        label="📥 Download Report",
                        data=f,
                        file_name="AI_Resume_Report.pdf",
                        mime="application/pdf"
                    )

    else:
        st.warning("⚠️ Please upload resume and enter job description")