from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

def match_profile(profile: dict, jd_analysis: dict) ->dict:
    prompt = f"""
    You are a resume expert. Given a candidate's profile and a job analysis,
    select and reframe the most relevant experiences and skills.

    Candidate Profile:
    {json.dumps(profile, indent=2)}

    Job Analysis:
    {json.dumps(jd_analysis, indent=2)}

    Return a JSON with exactly these keys:
    - selected_skills: list of most relevant skills to highlight
    - reframed_experience: list of projects rewritten to match the job, each with "title" and "bullets"
    - suggested_summary: a 2-line professional summary tailored to this specific role

    Return ONLY valid JSON, no explanation, no markdown, no backticks.
    """
    response = llm.invoke(prompt)
    return json.loads(response.content)