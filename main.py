from agents.jd_analyser import analyze_jd
from agents.profile_matcher import match_profile
from agents.resume_builder import build_resume
from pdf_generator import generate_pdf
import json

with open("data/profile.json", "r") as f:
    profile = json.load(f)

jd = """
We are looking for a Python developer with experience in REST APIs, 
machine learning, and cloud deployment. The candidate should be familiar 
with FastAPI, Docker, and have good communication skills. Experience with 
LLMs or AI pipelines is a plus.
"""

#agent 1

print("Running Agent 1 - JD Analyzer...")
jd_analysis = analyze_jd(jd)
print("Done.")
print()

#Agent 2
print("Running Agent 2 - Profile Matcher...")
matched = match_profile(profile, jd_analysis)
print("Done.")
print()

#Agent 3
print("Running Agent 3 - Resume Builder...")
resume = build_resume(profile, matched)
print("Done.")

print("Generating PDF...")
try:
    generate_pdf(resume)
except Exception as e:
    print(f"pdf error: {e}")