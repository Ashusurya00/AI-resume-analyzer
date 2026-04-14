"""
NEXUS · Resume Intelligence Platform
Enterprise-grade resume analyzer with AI-powered insights,
skill gap analysis, ATS scoring, and branded PDF export.
"""

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from utils.parser import extract_text_from_pdf, extract_sections, estimate_experience_years
from utils.matcher import extract_skills, calculate_match
from utils.llm_analyzer import analyze_resume
from utils.pdf_generator import generate_pdf
from config.settings import settings

st.set_page_config(
    page_title="NEXUS · Resume Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@300;600;700;900&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --bg:#08090f;--surface:#0e1018;--elevated:#151722;--hover:#1c1f2e;
  --border:rgba(255,255,255,0.07);--border-hi:rgba(255,255,255,0.15);
  --amber:#f59e0b;--amber-light:#fcd34d;--amber-dim:rgba(245,158,11,0.12);
  --teal:#2dd4bf;--teal-dim:rgba(45,212,191,0.10);
  --rose:#fb7185;--rose-dim:rgba(251,113,133,0.10);
  --sky:#38bdf8;--sky-dim:rgba(56,189,248,0.10);--violet:#a78bfa;
  --text:#f1f0ed;--text-2:#9ca3af;--text-3:#4b5563;
  --font-serif:'Fraunces',Georgia,serif;--font-sans:'DM Sans',sans-serif;
  --font-mono:'JetBrains Mono',monospace;
  --r-sm:8px;--r-md:14px;--r-lg:20px;--shadow:0 4px 24px rgba(0,0,0,0.6);
}
html,body,[class*="css"]{font-family:var(--font-sans)!important;background:var(--bg)!important;color:var(--text)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0 2rem 4rem!important;max-width:1300px!important;}
.stApp{background:var(--bg);}
.stApp::before{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:linear-gradient(rgba(245,158,11,0.025) 1px,transparent 1px),linear-gradient(90deg,rgba(245,158,11,0.025) 1px,transparent 1px);
  background-size:72px 72px;mask-image:radial-gradient(ellipse at 30% 0%,black 30%,transparent 75%);}
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:rgba(245,158,11,0.3);border-radius:3px;}
.topbar{padding:2.25rem 0 1.75rem;border-bottom:1px solid var(--border);margin-bottom:2rem;position:relative;}
.topbar::after{content:'';position:absolute;bottom:-1px;left:0;width:120px;height:2px;background:linear-gradient(90deg,var(--amber),transparent);}
.brand-name{font-family:var(--font-serif)!important;font-size:2rem;font-weight:900;letter-spacing:-0.03em;color:var(--text);line-height:1;}
.brand-tag{font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;color:var(--amber);font-weight:600;margin-top:3px;}
.brand-badge{padding:4px 12px;background:var(--amber-dim);border:1px solid rgba(245,158,11,0.3);border-radius:100px;font-size:0.68rem;font-family:var(--font-mono)!important;color:var(--amber);letter-spacing:0.06em;}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-lg);padding:1.5rem 1.75rem;box-shadow:var(--shadow);margin-bottom:1rem;}
.card-sm{background:var(--elevated);border:1px solid var(--border);border-radius:var(--r-md);padding:1rem 1.25rem;}
.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:0.75rem;margin-bottom:1.5rem;}
.stat-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--r-md);padding:1.1rem 1rem;text-align:center;position:relative;overflow:hidden;}
.stat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.stat-amber::before{background:var(--amber);}.stat-teal::before{background:var(--teal);}
.stat-sky::before{background:var(--sky);}.stat-rose::before{background:var(--rose);}
.stat-num{font-family:var(--font-serif)!important;font-size:2rem;font-weight:900;line-height:1.1;}
.stat-lbl{font-size:0.62rem;text-transform:uppercase;letter-spacing:0.12em;color:var(--text-3);font-weight:600;margin-top:2px;}
.sec-label{font-size:0.65rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--text-3);display:flex;align-items:center;gap:8px;margin-bottom:0.75rem;}
.sec-label::after{content:'';flex:1;height:1px;background:var(--border);}
.fit-badge{display:inline-flex;align-items:center;gap:6px;padding:6px 16px;border-radius:100px;font-size:0.82rem;font-weight:700;letter-spacing:0.04em;}
.fit-strong{background:var(--teal-dim);border:1px solid rgba(45,212,191,0.3);color:var(--teal);}
.fit-moderate{background:var(--amber-dim);border:1px solid rgba(245,158,11,0.3);color:var(--amber);}
.fit-weak{background:var(--rose-dim);border:1px solid rgba(251,113,133,0.3);color:var(--rose);}
.skill-tag{display:inline-flex;align-items:center;padding:3px 10px;border-radius:100px;font-size:0.7rem;font-weight:600;margin:2px 3px;letter-spacing:0.03em;}
.tag-matched{background:var(--teal-dim);border:1px solid rgba(45,212,191,0.3);color:var(--teal);}
.tag-missing{background:var(--rose-dim);border:1px solid rgba(251,113,133,0.25);color:var(--rose);}
.tag-neutral{background:var(--sky-dim);border:1px solid rgba(56,189,248,0.25);color:var(--sky);}
.prog-wrap{margin-bottom:0.6rem;}
.prog-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;}
.prog-name{font-size:0.78rem;font-weight:600;color:var(--text-2);}
.prog-pct{font-size:0.72rem;font-family:var(--font-mono)!important;color:var(--amber);}
.prog-bar{height:5px;background:var(--elevated);border-radius:3px;overflow:hidden;}
.prog-fill{height:100%;border-radius:3px;background:linear-gradient(90deg,var(--amber),var(--teal));}
.rewrite-card{background:var(--elevated);border:1px solid var(--border);border-radius:var(--r-md);padding:1rem 1.2rem;margin-bottom:0.75rem;}
.before-label{font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--rose);margin-bottom:4px;}
.after-label{font-size:0.65rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--teal);margin-top:8px;margin-bottom:4px;}
.before-text{font-size:0.82rem;color:var(--text-2);font-style:italic;line-height:1.5;}
.after-text{font-size:0.82rem;color:var(--text);line-height:1.5;}
.section-check{display:flex;align-items:center;gap:8px;padding:0.5rem 0.75rem;border-radius:var(--r-sm);font-size:0.8rem;font-weight:600;margin-bottom:4px;}
.sec-found{background:var(--teal-dim);color:var(--teal);}
.sec-missing{background:var(--rose-dim);color:var(--rose);opacity:0.7;}
.stTextArea textarea{background:var(--elevated)!important;border:1px solid var(--border)!important;border-radius:var(--r-md)!important;color:var(--text)!important;font-family:var(--font-sans)!important;font-size:0.9rem!important;}
.stTextArea textarea:focus{border-color:var(--amber)!important;box-shadow:0 0 0 3px rgba(245,158,11,0.12)!important;}
.stTextArea label{font-size:0.72rem!important;font-weight:700!important;letter-spacing:0.1em!important;text-transform:uppercase!important;color:var(--text-2)!important;}
[data-testid="stFileUploader"]{background:var(--elevated)!important;border:1px dashed rgba(245,158,11,0.3)!important;border-radius:var(--r-md)!important;}
.stButton>button{background:linear-gradient(135deg,var(--amber),#d97706)!important;border:none!important;border-radius:var(--r-md)!important;color:#0a0700!important;font-family:var(--font-sans)!important;font-weight:700!important;font-size:0.85rem!important;letter-spacing:0.06em!important;text-transform:uppercase!important;padding:0.75rem 1.5rem!important;box-shadow:0 4px 20px rgba(245,158,11,0.3)!important;transition:all 0.2s!important;}
.stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 30px rgba(245,158,11,0.45)!important;}
.stDownloadButton>button{background:var(--elevated)!important;border:1px solid var(--border)!important;color:var(--text-2)!important;font-size:0.78rem!important;padding:0.5rem 1rem!important;border-radius:var(--r-sm)!important;text-transform:none!important;box-shadow:none!important;}
.stDownloadButton>button:hover{border-color:var(--amber)!important;color:var(--amber)!important;transform:none!important;}
[data-testid="stSidebar"]{background:var(--surface)!important;border-right:1px solid var(--border)!important;}
.stTabs [data-baseweb="tab-list"]{background:var(--elevated)!important;border-radius:var(--r-md)!important;padding:4px!important;gap:2px!important;border:1px solid var(--border)!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:var(--text-2)!important;border-radius:10px!important;font-weight:600!important;font-size:0.82rem!important;padding:0.5rem 1.1rem!important;}
.stTabs [aria-selected="true"]{background:var(--amber-dim)!important;color:var(--amber)!important;border:1px solid rgba(245,158,11,0.25)!important;}
.stTabs [data-baseweb="tab-border"]{display:none!important;}
.stSuccess{background:var(--teal-dim)!important;border:1px solid rgba(45,212,191,0.25)!important;color:var(--teal)!important;border-radius:var(--r-md)!important;}
.stWarning{background:var(--amber-dim)!important;border:1px solid rgba(245,158,11,0.2)!important;color:var(--amber)!important;border-radius:var(--r-md)!important;}
.stError{background:var(--rose-dim)!important;border:1px solid rgba(251,113,133,0.2)!important;color:var(--rose)!important;border-radius:var(--r-md)!important;}
.stSpinner>div{border-top-color:var(--amber)!important;}
.streamlit-expanderHeader{background:var(--elevated)!important;border-radius:var(--r-md)!important;color:var(--text)!important;font-weight:600!important;border:1px solid var(--border)!important;}
.streamlit-expanderContent{background:var(--surface)!important;border:1px solid var(--border)!important;border-top:none!important;}
hr{border-color:var(--border)!important;}
.stToggle>label{color:var(--text-2)!important;font-size:0.85rem!important;}
.stSelectbox>div>div{background:var(--elevated)!important;border:1px solid var(--border)!important;color:var(--text)!important;}
.stProgress>div>div>div>div{background:linear-gradient(90deg,var(--amber),var(--teal))!important;}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.fade-up{animation:fadeUp 0.35s ease both;}
</style>
""", unsafe_allow_html=True)

# Session state
for k, v in {"result":None,"analysis":None,"match":None,"resume_text":"","resume_secs":{},"exp_years":0,"history":[],"resume_skills":{},"jd_skills":{}}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def skill_tags(skills, tag_class):
    return "".join(f'<span class="skill-tag {tag_class}">{s}</span>' for s in skills)

def progress_bar(label, pct, color="amber"):
    fill = {"amber":"var(--amber)","teal":"var(--teal)","rose":"var(--rose)","sky":"var(--sky)"}.get(color,"var(--amber)")
    return f'''<div class="prog-wrap"><div class="prog-head"><span class="prog-name">{label}</span><span class="prog-pct">{pct}%</span></div><div class="prog-bar"><div class="prog-fill" style="width:{pct}%;background:{fill}"></div></div></div>'''

def fit_badge(fit):
    cls = "fit-strong" if "Strong" in fit else ("fit-moderate" if "Moderate" in fit else "fit-weak")
    icon = "●" if "Strong" in fit else ("◐" if "Moderate" in fit else "○")
    return f'<span class="fit-badge {cls}">{icon} {fit}</span>'

def sc_color(s):
    return "var(--teal)" if s>=70 else ("var(--amber)" if s>=40 else "var(--rose)")

# Sidebar
with st.sidebar:
    st.markdown('''<div style="padding:0.5rem 0 1.5rem"><div style="font-family:'Fraunces',serif;font-size:1.3rem;font-weight:900;color:#f1f0ed">◈ NEXUS</div><div style="font-size:0.65rem;letter-spacing:0.2em;text-transform:uppercase;color:#f59e0b;margin-top:2px">Resume Intelligence</div></div>''', unsafe_allow_html=True)
    show_skills   = st.toggle("Skills Breakdown", True)
    show_rewrites = st.toggle("Bullet Rewrites", True)
    show_sections = st.toggle("Section Audit", True)
    show_category = st.toggle("Category Analysis", True)
    st.markdown("---")
    model = st.selectbox("AI Model", ["gpt-4o-mini","gpt-4o","gpt-4-turbo"])
    settings.model_name = model
    st.markdown("---")
    for tip in ["Upload a clean text-based PDF","Use the actual job posting","Include quantified achievements","Tailor skills to each role"]:
        st.markdown(f'<div style="font-size:0.78rem;color:#6b7280;padding:3px 0">› {tip}</div>', unsafe_allow_html=True)
    if st.session_state.history:
        st.markdown("---")
        st.markdown('<div style="font-size:0.65rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#4b5563;margin-bottom:0.5rem">📂 History</div>', unsafe_allow_html=True)
        for h in reversed(st.session_state.history[-5:]):
            st.markdown(f'<div style="background:#151722;border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:0.6rem 0.75rem;margin-bottom:4px"><div style="font-size:0.75rem;font-weight:600;color:#f1f0ed;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{h["name"]}</div><div style="font-size:0.65rem;color:#6b7280;margin-top:2px">Score: {h["score"]}%  ·  {h["time"]}</div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<div style="font-size:0.62rem;color:#374151;text-align:center">NEXUS v{settings.app_version}</div>', unsafe_allow_html=True)

# Topbar
st.markdown('''<div class="topbar"><div style="display:flex;align-items:center;justify-content:space-between"><div><div class="brand-name">◈ NEXUS</div><div class="brand-tag">Resume Intelligence Platform</div></div><div class="brand-badge">v2.0 · Enterprise</div></div></div>''', unsafe_allow_html=True)

# Inputs
st.markdown('<div class="sec-label">Upload & Analyze</div>', unsafe_allow_html=True)
col_up, col_jd = st.columns([1,1], gap="large")
with col_up:
    resume_file = st.file_uploader("RESUME PDF", type=["pdf"])
with col_jd:
    job_description = st.text_area("JOB DESCRIPTION", placeholder="Paste the full job posting here…", height=160)

_, btn_col, _ = st.columns([1,2,1])
with btn_col:
    analyze_btn = st.button("◈  Analyze Resume", use_container_width=True)

if analyze_btn:
    if not resume_file:
        st.warning("Please upload a resume PDF.")
    elif not job_description or len(job_description.strip()) < 30:
        st.warning("Please paste a job description (at least 30 characters).")
    else:
        with st.spinner("Analyzing your resume with AI…"):
            import datetime
            resume_text   = extract_text_from_pdf(resume_file)
            resume_secs   = extract_sections(resume_text)
            exp_years     = estimate_experience_years(resume_text)
            resume_skills = extract_skills(resume_text)
            jd_skills     = extract_skills(job_description)
            match         = calculate_match(resume_skills, jd_skills)
            analysis      = analyze_resume(resume_text, job_description)
        st.session_state.update({"result":True,"analysis":analysis,"match":match,"resume_text":resume_text,"resume_secs":resume_secs,"exp_years":exp_years,"resume_skills":resume_skills,"jd_skills":jd_skills})
        st.session_state.history.append({"name":resume_file.name,"score":match["overall_score"],"time":datetime.datetime.now().strftime("%H:%M")})
        st.rerun()

if st.session_state.result:
    analysis      = st.session_state.analysis
    match         = st.session_state.match
    resume_secs   = st.session_state.resume_secs
    exp_years     = st.session_state.exp_years
    resume_skills = st.session_state.resume_skills
    score   = match["overall_score"]
    ats     = analysis.get("ats_score", 0)
    fit     = analysis.get("fit_level","—")
    matched = match["matched_skills"]
    missing = match["missing_skills"]
    priority= match["priority_missing"]
    exp_label = f"{exp_years}+ yrs" if exp_years else "—"

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    st.success("✓ Analysis complete")

    st.markdown(f'''<div class="stat-grid fade-up">
      <div class="stat-card stat-amber"><div class="stat-num" style="color:{sc_color(score)}">{score}%</div><div class="stat-lbl">Skill Match</div></div>
      <div class="stat-card stat-teal"><div class="stat-num" style="color:{sc_color(ats)}">{ats}</div><div class="stat-lbl">ATS Score</div></div>
      <div class="stat-card stat-sky"><div class="stat-num" style="color:var(--sky)">{len(matched)}</div><div class="stat-lbl">Skills Matched</div></div>
      <div class="stat-card stat-rose"><div class="stat-num" style="color:var(--violet)">{exp_label}</div><div class="stat-lbl">Experience</div></div>
    </div>''', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["◈ Overview","◎ Skills Analysis","✦ AI Feedback","⬇ Export"])

    with tab1:
        left, right = st.columns([3,2], gap="large")
        with left:
            impression = analysis.get("overall_impression","")
            st.markdown(f'''<div class="card fade-up"><div class="sec-label">Job Fit Assessment</div>{fit_badge(fit)}<div style="height:1rem"></div><div style="font-size:0.88rem;color:var(--text-2);line-height:1.7">{impression}</div></div>''', unsafe_allow_html=True)
            strengths = analysis.get("strengths",[])
            if strengths:
                items = "".join(f'<div style="display:flex;gap:10px;padding:0.5rem 0;border-bottom:1px solid var(--border)"><span style="color:var(--teal);flex-shrink:0">✓</span><span style="font-size:0.85rem;color:var(--text-2);line-height:1.5">{s}</span></div>' for s in strengths)
                st.markdown(f'<div class="card fade-up"><div class="sec-label">Key Strengths</div>{items}</div>', unsafe_allow_html=True)
            weaknesses = analysis.get("weaknesses",[])
            if weaknesses:
                items = "".join(f'<div style="display:flex;gap:10px;padding:0.5rem 0;border-bottom:1px solid var(--border)"><span style="color:var(--rose);flex-shrink:0">⚠</span><span style="font-size:0.85rem;color:var(--text-2);line-height:1.5">{w}</span></div>' for w in weaknesses)
                st.markdown(f'<div class="card fade-up"><div class="sec-label">Gaps & Weaknesses</div>{items}</div>', unsafe_allow_html=True)
        with right:
            if priority:
                st.markdown(f'<div class="card fade-up"><div class="sec-label">Priority Skills to Add</div><div>{skill_tags(priority,"tag-missing")}</div></div>', unsafe_allow_html=True)
            if show_sections and resume_secs:
                sec_html = "".join(f'<div class="section-check {"sec-found" if found else "sec-missing"}">{"✓" if found else "✗"}  {sec}</div>' for sec,found in resume_secs.items())
                st.markdown(f'<div class="card fade-up"><div class="sec-label">Resume Section Audit</div>{sec_html}</div>', unsafe_allow_html=True)
            suggestions = analysis.get("improvement_suggestions",[])
            if suggestions:
                items = "".join(f'<div style="display:flex;gap:8px;padding:0.45rem 0;border-bottom:1px solid var(--border)"><span style="color:var(--amber);flex-shrink:0;font-size:0.75rem;margin-top:2px">{i+1}</span><span style="font-size:0.8rem;color:var(--text-2);line-height:1.5">{s}</span></div>' for i,s in enumerate(suggestions))
                st.markdown(f'<div class="card fade-up"><div class="sec-label">Improvement Suggestions</div>{items}</div>', unsafe_allow_html=True)

    with tab2:
        if show_skills:
            cat_scores = match.get("category_scores",{})
            st.markdown(f'<div class="card fade-up"><div class="sec-label">Overall Match</div>{progress_bar("Skill Match Score",score)}{progress_bar("ATS Compatibility",ats,"teal")}</div>', unsafe_allow_html=True)
            col_m,col_x = st.columns(2,gap="large")
            with col_m:
                if matched:
                    st.markdown(f'<div class="card fade-up"><div class="sec-label">✓ Matched Skills ({len(matched)})</div><div>{skill_tags(matched,"tag-matched")}</div></div>', unsafe_allow_html=True)
            with col_x:
                if missing:
                    st.markdown(f'<div class="card fade-up"><div class="sec-label">✗ Missing Skills ({len(missing)})</div><div>{skill_tags(missing[:20],"tag-missing")}</div></div>', unsafe_allow_html=True)
            if show_category and cat_scores:
                st.markdown('<div class="sec-label" style="margin-top:1rem">Category Breakdown</div>', unsafe_allow_html=True)
                cols = st.columns(2,gap="large")
                for i,(cat,data) in enumerate(cat_scores.items()):
                    with cols[i%2]:
                        cp = data["score"]
                        color = "teal" if cp>=70 else ("amber" if cp>=40 else "rose")
                        st.markdown(f'<div class="card-sm fade-up" style="margin-bottom:0.75rem">{progress_bar(cat,cp,color)}<div style="margin-top:6px">{skill_tags(data["matched"],"tag-matched")}{skill_tags(data["missing"],"tag-missing")}</div></div>', unsafe_allow_html=True)
            all_extra = [s for cs in st.session_state.resume_skills.values() for s in cs if s not in matched]
            if all_extra:
                st.markdown(f'<div class="card fade-up" style="margin-top:0.5rem"><div class="sec-label">Additional Resume Skills</div><div>{skill_tags(all_extra[:30],"tag-neutral")}</div></div>', unsafe_allow_html=True)

    with tab3:
        rec = analysis.get("final_recommendation","")
        if rec:
            st.markdown(f'<div style="background:var(--amber-dim);border:1px solid rgba(245,158,11,0.25);border-radius:var(--r-lg);padding:1.5rem 1.75rem;margin-bottom:1rem" class="fade-up"><div style="font-size:0.65rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--amber);margin-bottom:0.6rem">◈ Final Recommendation</div><div style="font-size:0.9rem;color:var(--text);line-height:1.7">{rec}</div></div>', unsafe_allow_html=True)
        rewrites = analysis.get("bullet_rewrites",[])
        if show_rewrites and rewrites:
            st.markdown('<div class="sec-label" style="margin-top:1rem">✏ Bullet Point Rewrites</div>', unsafe_allow_html=True)
            for rw in rewrites:
                orig = rw.get("original","").replace("<","&lt;").replace(">","&gt;")
                impr = rw.get("improved","").replace("<","&lt;").replace(">","&gt;")
                if orig and impr:
                    st.markdown(f'<div class="rewrite-card fade-up"><div class="before-label">Before</div><div class="before-text">{orig}</div><div class="after-label">After</div><div class="after-text">{impr}</div></div>', unsafe_allow_html=True)
        with st.expander("📄 Extracted Resume Text"):
            st.code(st.session_state.resume_text[:3000], language=None)

    with tab4:
        st.markdown('<div class="sec-label">Download Report</div>', unsafe_allow_html=True)
        st.markdown('<div class="card fade-up"><div style="font-size:0.88rem;color:var(--text-2);line-height:1.7;margin-bottom:1rem">Export a branded PDF report with all analysis dimensions: fit assessment, skill gap analysis, strengths, weaknesses, improvement suggestions, bullet rewrites, and final recommendation.</div></div>', unsafe_allow_html=True)
        if st.button("◈ Generate PDF Report"):
            with st.spinner("Generating PDF…"):
                pdf_path = generate_pdf(topic="Resume Analysis",analysis=analysis,match_result=match,resume_sections=resume_secs,output_dir="outputs")
            with open(pdf_path,"rb") as f:
                st.download_button(label="⬇  Download PDF Report",data=f,file_name="NEXUS_Resume_Report.pdf",mime="application/pdf",use_container_width=True)

elif not analyze_btn:
    st.markdown('''<div style="text-align:center;padding:3.5rem 2rem;margin-top:1rem" class="fade-up">
      <div style="font-family:'Fraunces',serif;font-size:3rem;color:rgba(245,158,11,0.2);margin-bottom:1rem;font-weight:900">◈</div>
      <div style="font-family:'Fraunces',serif;font-size:1.3rem;font-weight:700;color:#374151;margin-bottom:0.5rem">Ready to Analyze</div>
      <div style="color:#4b5563;font-size:0.85rem;max-width:400px;margin:0 auto;line-height:1.6">Upload your resume PDF and paste a job description to get an AI-powered skill gap analysis, ATS score, and tailored improvement suggestions.</div>
      <div style="margin-top:1.5rem;display:flex;gap:8px;justify-content:center;flex-wrap:wrap">
        <span class="skill-tag tag-neutral">Skill Gap Analysis</span>
        <span class="skill-tag tag-neutral">ATS Score</span>
        <span class="skill-tag tag-neutral">Bullet Rewrites</span>
        <span class="skill-tag tag-neutral">PDF Export</span>
      </div>
    </div>''', unsafe_allow_html=True)
