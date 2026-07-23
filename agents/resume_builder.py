from langchain_groq import ChatGroq
from dotenv import load_dotenv
import json

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

def build_resume(profile: dict, matched_data: dict) -> dict:
    prompt = f"""
    Build a complete resume JSON using this data.

    Base profile: {json.dumps(profile)}
    Tailored content: {json.dumps(matched_data)}

    Return JSON in exactly this structure:
    {{
      "header": {{
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "linkedin": "",
        "github": ""
      }},
      "summary": "",
      "skills": [],
      "experience": [
        {{
          "title": "",
          "duration": "",
          "bullets": []
        }}
      ],
      "education": [
        {{
          "degree": "",
          "institution": "",
          "year": ""
        }}
      ],
      "projects": [
        {{
          "name": "",
          "tech": [],
          "bullets": []
        }}
      ]
    }}

    Return ONLY valid JSON, no explanation, no markdown, no backticks.
    """

    response = llm.invoke(prompt)
    return json.loads(response.content)