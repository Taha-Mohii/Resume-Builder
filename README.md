# 📄 AI Resume Builder

An AI-powered resume tailoring system that generates personalized, job-specific resumes using a multi-agent LangGraph pipeline. Paste a job description, and get a tailored PDF resume in seconds.

🔗 **Live Demo:** https://resume-builder-c7dwxex9sndthdcncpzu7s.streamlit.app/  
💻 **GitHub:** [https://github.com/Taha-Mohii/resume-builder](https://github.com/Taha-Mohii/resume-builder)

---

## ✨ Features

- **Multi-agent pipeline** — 3 LangGraph agents work in sequence to analyze, match, and build your resume
- **Job-tailored output** — every resume is customized to the specific job description
- **3 resume templates** — Classic, Modern, and Minimal styles
- **PDF download** — one-click download of your tailored resume
- **Persistent profiles** — user profiles saved to Supabase, no re-entering data
- **Clickable links** — LinkedIn, GitHub, and project links embedded in the PDF
- **Live deployment** — accessible from any device via Streamlit Cloud

---

## 🤖 How It Works

```
User Profile (stored in Supabase)
        +
Job Description (pasted by user)
        ↓
Agent 1 — JD Analyzer
→ Extracts required skills, keywords, tone, role focus
        ↓
Agent 2 — Profile Matcher
→ Selects and reframes your experiences to match the JD
        ↓
Agent 3 — Resume Builder
→ Assembles a structured resume JSON
        ↓
PDF Generator
→ Renders the resume using your chosen template
        ↓
Download Ready ✅
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Agents | LangGraph + LangChain |
| LLM | Groq API (LLaMA 3.3 70B) |
| UI | Streamlit |
| Database | Supabase |
| PDF Generation | xhtml2pdf + Jinja2 |
| Deployment | Streamlit Cloud |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Taha-Mohii/resume-builder.git
cd resume-builder
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root:
```
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 4. Set up Supabase
Create a table called `resume` in your Supabase project with these columns:
- `id` — int8, primary key
- `email` — text, unique
- `profile_data` — text
- `created_at` — timestamp, default `now()`

### 5. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
resume-builder/
├── agents/
│   ├── jd_analyser.py       # Agent 1 — analyzes job description
│   ├── profile_matcher.py   # Agent 2 — matches profile to JD
│   └── resume_builder.py    # Agent 3 — builds resume JSON
├── templates/
│   ├── classic.html         # Classic resume template
│   ├── modern.html          # Modern resume template
│   └── minimal.html         # Minimal resume template
├── output/                  # Generated PDFs saved here
├── app.py                   # Main Streamlit app
├── pdf_generator.py         # PDF generation router
└── requirements.txt
```

---

## 📸 Templates

| Classic | Modern | Minimal |
|---------|--------|---------|
| Traditional serif style | Dark navy header band | Clean left-aligned layout |
| Blue section headers | Teal accent colors | Grey section headers |
| ATS-friendly | ATS-friendly | ATS-friendly |

---

## 🔑 Getting API Keys

- **Groq API** — [console.groq.com](https://console.groq.com)
- **Supabase** — [supabase.com](https://supabase.com)

---

## 👤 Author

**Taha Mohi Ud Din Rather**  
B.Tech CSE @ College of Engineering Trivandrum  
[GitHub](https://github.com/Taha-Mohii) | [LinkedIn](https://www.linkedin.com/in/taha-mohi-ud-din-rather-507b8a362/)
