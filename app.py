import streamlit as st
import json
import os
from agents.jd_analyser import analyze_jd
from agents.profile_matcher import match_profile
from agents.resume_builder import build_resume
from pdf_generator import generate_pdf

st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="centered")

# --- SESSION STATE INIT ---
if "profile" not in st.session_state:
    st.session_state.profile = None
if "page" not in st.session_state:
    st.session_state.page = "profile"

def profile_page():
    st.title("👤 Set Up Your Profile")
    st.markdown("Fill in your details once. We'll use this to tailor your resume every time.")

    with st.form("profile_form"):
        st.subheader("Basic Info")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        location = st.text_input("Location")
        linkedin = st.text_input("LinkedIn URL (optional)")
        github = st.text_input("GitHub URL (optional)")
        summary = st.text_area("Career Summary / Objective", height=100)

        st.subheader("Skills")
        languages = st.text_input("Programming Languages (comma separated)", placeholder="Python, Java, JavaScript")
        frameworks = st.text_input("Frameworks & Libraries (comma separated)", placeholder="LangGraph, FastAPI, React")
        tools = st.text_input("Tools & Platforms (comma separated)", placeholder="Git, Docker, VS Code")

        st.subheader("Education")
        degree = st.text_input("Degree")
        institution = st.text_input("Institution")
        edu_year = st.text_input("Year (e.g. 2024 - 2028)")

        st.subheader("Experience / Projects")
        st.markdown("Add your projects and experience as bullet points. Format: **Title | Date | bullet1; bullet2; bullet3**")
        projects_raw = st.text_area("Projects & Experience", height=200, placeholder="Leaderbolt AI | Jul 2026 | Built a LangGraph pipeline; Used Groq API; Deployed on cloud\nHaven | Jun 2026 - Present | Built AI companion; Used LLMs; Integrated mood tracking")

        submitted = st.form_submit_button("Save Profile & Continue", type="primary")

        if submitted:
            if not name or not email:
                st.warning("Please fill in at least your name and email.")
            else:
                # Parse skills
                all_skills = []
                if languages:
                    all_skills += [s.strip() for s in languages.split(",")]
                if frameworks:
                    all_skills += [s.strip() for s in frameworks.split(",")]
                if tools:
                    all_skills += [s.strip() for s in tools.split(",")]

                # Parse projects
                projects = []
                experience = []
                if projects_raw:
                    for line in projects_raw.strip().split("\n"):
                        parts = line.split("|")
                        if len(parts) >= 3:
                            title = parts[0].strip()
                            date = parts[1].strip()
                            bullets = [b.strip() for b in parts[2].split(";")]
                            projects.append({
                                "name": title,
                                "date": date,
                                "tech": [],
                                "bullets": bullets
                            })
                            experience.append({
                                "title": title,
                                "duration": date,
                                "bullets": bullets
                            })

                # Build profile
                profile = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "linkedin": linkedin,
                    "github": github,
                    "summary": summary,
                    "skills": all_skills,
                    "education": [{
                        "degree": degree,
                        "institution": institution,
                        "year": edu_year
                    }],
                    "experience": experience,
                    "projects": projects,
                    "certifications": []
                }

                st.session_state.profile = profile
                st.session_state.page = "resume"
                st.rerun()

def resume_page():
    st.title("📄 AI Resume Builder")
    st.markdown("Paste a job description and get a tailored resume in seconds.")

    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.profile['name']}**")
        if st.button("Edit Profile"):
            st.session_state.page = "profile"
            st.rerun()

    jd = st.text_area("Job Description", placeholder="Paste the job description here...", height=250)

    template = st.selectbox(
        "Choose a resume template",
        options=["classic", "modern", "minimal"],
        format_func=lambda x: x.capitalize()
    )

    if st.button("Generate Resume", type="primary"):
        if not jd.strip():
            st.warning("Please paste a job description first.")
        else:
            with st.spinner("Agent 1 — Analyzing job description..."):
                jd_analysis = analyze_jd(jd)

            with st.spinner("Agent 2 — Matching your profile..."):
                matched = match_profile(st.session_state.profile, jd_analysis)

            with st.spinner("Agent 3 — Building your resume..."):
                resume = build_resume(st.session_state.profile, matched)

            with st.spinner("Generating PDF..."):
                generate_pdf(resume, template=template)

            st.success("Resume generated!")

            with open("output/resume.pdf", "rb") as f:
                st.download_button(
                    label="⬇️ Download Resume PDF",
                    data=f,
                    file_name=f"resume_{template}.pdf",
                    mime="application/pdf"
                )

if st.session_state.page == "profile":
    profile_page()
else:
    resume_page()