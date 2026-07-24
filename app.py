import streamlit as st
import json
from agents.jd_analyser import analyze_jd
from agents.profile_matcher import match_profile
from agents.resume_builder import build_resume
from pdf_generator import generate_pdf

with open("data/profile.json", "r") as f:
    profile = json.load(f)

st.set_page_config(page_title="Resume Builder", page_icon="📄", layout="centered")

st.title("📄 AI Resume Builder")
st.markdown("Paste a job description below and get a tailored resume in seconds.")

# --- INPUT ---
jd = st.text_area("Job Description", placeholder="Paste the job description here...", height=250)

if st.button("Generate Resume", type="primary"):
    if not jd.strip():
        st.warning("Please paste a job description first.")

    else:
        with st.spinner("Agent 1 — Analyzing job description..."):
            jd_analysis = analyze_jd(jd)

        with st.spinner("Agent 2 — Matching your profile..."):
            matched = match_profile(profile, jd_analysis)

        with st.spinner("Agent 3 — Building your resume..."):
            resume = build_resume(profile, matched)

        with st.spinner("Generating PDF..."):
            generate_pdf(resume)
        st.success("Resume Generated..!")


        with open("output/resume.pdf", "rb")as f:
            st.download_button(
                label="Download Resume PDF.",
                data=f,
                file_name="tailored_resume.pdf",
                mime="application/pdf"
            )