from agents.jd_analyser import analyze_jd
from agents.profile_matcher import match_profile
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
print(jd_analysis)
print()

#Agent 2
print("Running Agent 2 - Profile Matcher...")
try:
    matched = match_profile(profile, jd_analysis)
    print(matched)
except Exception as e:
    print(f"Error: {e}")