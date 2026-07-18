from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json
import os

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

def analyze_jd(jd_text: str) -> dict:
    prompt = f"""
    Analyze this job description and extract the following in JSON format only:
    - required_skills: list of technical skills mentioned
    - keywords: important keywords to include in a resume
    - tone: formal/startup/technical
    - role_focus: what the job mainly involves in one sentence

    Job Description:
    {jd_text}

    Return ONLY valid JSON, no explanation, no markdown, no backticks.
    """

    response = llm.invoke(prompt)
    return json.loads(response.content)