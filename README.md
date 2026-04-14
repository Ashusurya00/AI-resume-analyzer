# ◈ NEXUS · Resume Intelligence Platform

> **Enterprise-grade AI-powered resume analyzer** with skill gap analysis,
> ATS scoring, structured LLM feedback, and branded PDF export.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red?style=flat-square)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green?style=flat-square)

---

## What It Does

Upload a resume PDF + paste a job description → NEXUS delivers:

| Feature | Description |
|---------|-------------|
| **Skill Match Score** | % of JD-required skills found in the resume |
| **ATS Score** | AI-estimated ATS compatibility (0–100) |
| **Job Fit Level** | Strong / Moderate / Weak Fit classification |
| **Category Breakdown** | Skills analyzed across 8 categories (AI, Cloud, Web, DB…) |
| **Section Audit** | Detects presence of Experience, Education, Skills, Projects, etc. |
| **Strengths & Weaknesses** | 4 strengths + 3 gaps identified by GPT |
| **Improvement Suggestions** | 5 specific, actionable resume improvements |
| **Bullet Rewrites** | 2+ before/after rewrites with stronger verbs & metrics |
| **Final Recommendation** | Hiring recommendation with next steps |
| **PDF Export** | Branded multi-section report downloadable as PDF |

---

## Architecture

```
resume-analyzer/
├── app.py                     # Premium Streamlit UI
├── requirements.txt
├── .env.example
│
├── config/
│   └── settings.py            # Pydantic settings + .env loader
│
├── utils/
│   ├── skills.py              # 300+ skills across 8 categories
│   ├── parser.py              # PDF extractor (pdfplumber + pypdf fallback)
│   ├── matcher.py             # Skill extractor + category-aware matcher
│   ├── llm_analyzer.py        # GPT analysis → structured JSON (9 dimensions)
│   └── pdf_generator.py       # Branded ReportLab PDF report
│
└── outputs/                   # Auto-saved PDF reports
```

---

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env → add your OPENAI_API_KEY

# 3. Run
streamlit run app.py
```

---

## Skills Database

300+ skills organized across 8 categories:

- **Programming Languages** — Python, Java, TypeScript, Go, Rust, Kotlin…
- **Web & Frontend** — React, Vue, Next.js, Tailwind, GraphQL…
- **Backend & Cloud** — Django, FastAPI, Docker, Kubernetes, AWS, Azure…
- **Data & AI** — ML, DL, NLP, PyTorch, LangChain, Spark, Airflow…
- **Databases** — PostgreSQL, MongoDB, Snowflake, Elasticsearch…
- **Tools & Practices** — Git, Agile, CI/CD, TDD, Pytest…
- **Soft Skills** — Leadership, Communication, Stakeholder Management…
- **Domain & Business** — Product Management, Cybersecurity, Flutter…

---

## UI Features

- 🎨 Premium dark design — Fraunces serif + DM Sans + JetBrains Mono
- 📊 4-stat dashboard (Match %, ATS, Skills, Experience)
- 🏷️ Color-coded skill tags (teal = matched, rose = missing, sky = extra)
- 📈 Per-category progress bars with matched/missing breakdown
- ✏️ Before/after bullet rewrite cards
- 📂 Session history in sidebar
- ⬇️ One-click PDF generation and download

---

## License

MIT © 2025 NEXUS Intelligence Platform
