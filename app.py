import streamlit as st
import json
import os
from agents.jd_analyser import analyze_jd
from agents.profile_matcher import match_profile
from agents.resume_builder import build_resume
from pdf_generator import generate_pdf
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="centered")

if "profile" not in st.session_state:
    st.session_state.profile = None
if "page" not in st.session_state:
    st.session_state.page = "login"


def login_page():
    st.title("📄 AI Resume Builder")
    st.markdown("Enter your email to load your profile or create a new one.")

    email = st.text_input("Email Address")

    if st.button("Continue", type="primary"):
        if not email.strip():
            st.warning("Please enter your email.")
        else:
            result = supabase.table("resume").select("*").eq("email", email).execute()
            if result.data:
                profile = json.loads(result.data[0]["profile_data"])
                st.session_state.profile = profile
                st.session_state.email = email
                st.session_state.page = "resume"
                st.rerun()
            else:
                st.session_state.email = email
                st.session_state.page = "profile"
                st.rerun()


def profile_page():
    st.title("👤 Set Up Your Profile")
    st.markdown("Fill in your details once. We'll save them for next time.")

    p = st.session_state.profile or {}
    h = p.get("header", {})

    with st.form("profile_form"):
        st.subheader("Basic Info")
        name = st.text_input("Full Name", value=h.get("name", ""))
        email = st.text_input("Email", value=st.session_state.get("email", ""))
        phone = st.text_input("Phone", value=h.get("phone", ""))
        location = st.text_input("Location", value=h.get("location", ""))
        linkedin = st.text_input("LinkedIn URL (optional)", value=h.get("linkedin", ""))
        github = st.text_input("GitHub URL (optional)", value=h.get("github", ""))
        summary = st.text_area("Career Summary / Objective", value=p.get("summary", ""), height=100)

        st.subheader("Skills")
        existing_skills = ", ".join(p.get("skills", []))
        languages = st.text_input("Programming Languages (comma separated)", value=existing_skills)
        frameworks = st.text_input("Frameworks & Libraries (comma separated)")
        tools = st.text_input("Tools & Platforms (comma separated)")

        st.subheader("Education")
        edu = p.get("education", [{}])[0] if p.get("education") else {}
        degree = st.text_input("Degree", value=edu.get("degree", ""))
        institution = st.text_input("Institution", value=edu.get("institution", ""))
        edu_year = st.text_input("Year (e.g. 2024 - 2028)", value=edu.get("year", ""))

        st.subheader("Experience / Projects")
        st.markdown("Format: **Title | Date | bullet1; bullet2 | Tech1, Tech2 | https://github.com/...**")

        # Pre-fill WITH tech and github
        existing_projects = ""
        for proj in p.get("projects", []):
            bullets = "; ".join(proj.get("bullets", []))
            tech = ", ".join(proj.get("tech", []))
            github_link = proj.get("github", "")
            existing_projects += f'{proj["name"]} | {proj.get("date", "")} | {bullets} | {tech} | {github_link}\n'

        projects_raw = st.text_area("Projects & Experience", value=existing_projects.strip(), height=200)

        submitted = st.form_submit_button("Save Profile & Continue", type="primary")

        if submitted:
            if not name or not email:
                st.warning("Please fill in at least your name and email.")
            else:
                all_skills = []
                if languages:
                    all_skills += [s.strip() for s in languages.split(",")]
                if frameworks:
                    all_skills += [s.strip() for s in frameworks.split(",")]
                if tools:
                    all_skills += [s.strip() for s in tools.split(",")]

                projects = []
                experience = []
                if projects_raw:
                    for line in projects_raw.strip().split("\n"):
                        parts = line.split("|")
                        if len(parts) >= 3:
                            title = parts[0].strip()
                            date = parts[1].strip()
                            bullets = [b.strip() for b in parts[2].split(";")]
                            tech = [t.strip() for t in parts[3].split(",")] if len(parts) >= 4 else []
                            github_link = parts[4].strip() if len(parts) >= 5 else ""
                            projects.append({
                                "name": title,
                                "date": date,
                                "tech": tech,
                                "bullets": bullets,
                                "github": github_link
                            })
                            experience.append({
                                "title": title,
                                "duration": date,
                                "bullets": bullets
                            })

                profile = {
                    "header": {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "location": location,
                        "linkedin": linkedin,
                        "github": github
                    },
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

                existing = supabase.table("resume").select("*").eq("email", email).execute()
                if existing.data:
                    supabase.table("resume").update({
                        "profile_data": json.dumps(profile)
                    }).eq("email", email).execute()
                else:
                    supabase.table("resume").insert({
                        "email": email,
                        "profile_data": json.dumps(profile)
                    }).execute()

                st.session_state.profile = profile
                st.session_state.email = email
                st.session_state.page = "resume"
                st.rerun()


def resume_page():
    st.title("📄 AI Resume Builder")
    st.markdown("Paste a job description and get a tailored resume in seconds.")

    with st.sidebar:
        st.markdown(f"👤 **{st.session_state.profile['header']['name']}**")
        st.markdown(f"📧 {st.session_state.email}")
        if st.button("Edit Profile"):
            st.session_state.page = "profile"
            st.rerun()
        if st.button("Logout"):
            st.session_state.profile = None
            st.session_state.page = "login"
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

                # Restore github links from original profile
                profile_projects = {p["name"].lower().strip(): p.get("github", "") for p in st.session_state.profile.get("projects", [])}
                for proj in resume.get("projects", []):
                    proj_name_lower = proj["name"].lower().strip()
                    if proj_name_lower in profile_projects:
                        proj["github"] = profile_projects[proj_name_lower]
                    else:
                        for key, link in profile_projects.items():
                            if key in proj_name_lower or proj_name_lower in key:
                                proj["github"] = link
                                break
                        else:
                            proj["github"] = ""

                # Debug
                for proj in resume.get("projects", []):
                    print(f"{proj['name']} -> {proj.get('github', 'EMPTY')}")

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


if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "profile":
    profile_page()
else:
    resume_page()