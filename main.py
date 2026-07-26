
from agents.jd_analyser import analyze_jd
from agents.profile_matcher import match_profile
from agents.resume_builder import build_resume
from pdf_generator import generate_pdf
import json

# Load profile
with open("data/profile.json", "r") as f:
    profile = json.load(f)

jd = """
We are seeking a Machine Learning Engineer Intern to join our AI team. 
The ideal candidate should have experience with Python, LLMs, and building 
AI pipelines. Familiarity with LangChain or LangGraph is a strong plus. 
You will be working on developing and deploying NLP models, integrating 
REST APIs, and contributing to our health-tech AI products.
"""

print("Running agents...")
jd_analysis = analyze_jd(jd)
matched = match_profile(profile, jd_analysis)
resume = build_resume(profile, matched)

print("Generating modern PDF...")
generate_pdf(resume, template="minimal")