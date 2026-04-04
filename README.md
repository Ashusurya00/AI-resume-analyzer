# 📄 AI Resume Analyzer & Job Matcher

## 🚀 Overview

AI Resume Analyzer is a **production-ready AI-powered application** that evaluates a candidate’s resume against a job description and provides:

* 📊 Match Score
* ✅ Skill Match Analysis
* ❌ Missing Skills
* 🤖 AI-driven Improvement Suggestions
* 📥 Downloadable Report (PDF)

The system combines **NLP, rule-based matching, and Large Language Models (LLMs)** to deliver intelligent and actionable feedback.

---

## 🎯 Problem Statement

Job applicants often struggle to understand how well their resume aligns with a job description.

### Challenges:

* Manual comparison is time-consuming
* Important skills are often missed
* Lack of structured feedback
* No clear improvement suggestions

👉 This project solves these problems using **AI-driven analysis and automation**.

---

## 🧠 Solution

The application analyzes both:

* 📄 Resume (PDF input)
* 📝 Job Description

Then it:

1. Extracts text from resume
2. Identifies key skills using NLP
3. Compares with job requirements
4. Calculates a match score
5. Uses an LLM to generate personalized feedback

---

## 🏗️ Architecture

Resume (PDF) → Text Extraction → Skill Extraction
Job Description → Skill Extraction
↓
Matching Engine
↓
LLM Analysis
↓
Dashboard + PDF Report

---

## ⚙️ Tech Stack

### 🧠 Core AI

* Python
* NLP (Regex-based skill extraction)
* LLM via OpenAI API

### 📄 Document Processing

* pdfplumber

### 🖥️ Frontend

* Streamlit

### 📊 Backend Logic

* Custom skill matcher
* Similarity scoring

### 📥 Report Generation

* reportlab

### 🔐 Environment Management

* python-dotenv

---

## 🔥 Key Features

### ✅ Resume Parsing

Extracts text from PDF resumes efficiently.

### ✅ Skill Extraction

Identifies relevant skills using keyword-based NLP.

### ✅ Match Score

Calculates alignment between resume and job description.

### ✅ Skill Gap Analysis

Highlights:

* Matched skills
* Missing skills

### ✅ AI Feedback

Uses LLM to provide:

* Strengths
* Weaknesses
* Improvement suggestions
* Final recommendation

### ✅ PDF Report

Download a structured analysis report.

### ✅ Premium UI

* Modern dashboard
* Tab-based interface
* Interactive components

---

## 📂 Project Structure

```
resume-analyzer/
│
├── app.py
├── utils/
│   ├── parser.py
│   ├── skills.py
│   ├── matcher.py
│   ├── llm_analyzer.py
│   ├── pdf_generator.py
│
├── data/
├── requirements.txt
├── README.md
```

---

## ▶️ How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/resume-analyzer.git
cd resume-analyzer
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Add API Key

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

### 5️⃣ Run Application

```bash
streamlit run app.py
```

---

## 🧪 Example Use Cases

* Resume screening
* Job application optimization
* Skill gap analysis
* Career guidance

---

## ⚠️ Challenges & Solutions

### 🔴 API Key Management

* Problem: API key errors
* Solution: Used environment variables via dotenv

---

### 🔴 PDF Parsing Issues

* Problem: Some PDFs not readable
* Solution: Used pdfplumber for better extraction

---

### 🔴 Skill Matching Limitations

* Problem: Exact keyword matching
* Solution: Improved with LLM-based analysis

---

### 🔴 UI Improvements

* Problem: Basic UI
* Solution: Built modern dashboard with Streamlit

---

## 🚀 Future Improvements

* 🔥 Semantic skill matching (embeddings)
* 🔥 Resume rewriting using AI
* 🔥 ATS keyword optimization
* 🔥 Multi-language support
* 🔥 Cloud deployment

---

## 🏆 Key Learnings

* NLP-based text processing
* LLM integration in real applications
* UI/UX design for AI products
* End-to-end system development

---

## 👨‍💻 Author

**Ashutosh Suryawanshi**

* GitHub: https://github.com/Ashusurya00
* LinkedIn: https://linkedin.com/in/ashutosh-suryawanshi-26aa46378

---

## ⭐ Support

If you like this project, give it a ⭐ and connect with me!

---
