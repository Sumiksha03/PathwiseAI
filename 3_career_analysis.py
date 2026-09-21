import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.set_page_config(
    page_title="Career Analysis · AI Career Guidance",
    page_icon="🎯",
    layout="wide"
)

# ─── PREMIUM DARK THEME CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=JetBrains+Mono:wght@300;400&display=swap');

:root {
  --bg:        #0c0c0f;
  --bg2:       #13131a;
  --bg3:       #1a1a24;
  --bg4:       #21212e;
  --border:    rgba(255,255,255,0.07);
  --border2:   rgba(255,255,255,0.12);
  --text:      #e8e8f0;
  --text2:     #9898b0;
  --text3:     #5a5a72;
  --accent1:   #7c6af7;
  --accent2:   #3ecfcf;
  --accent3:   #f06292;
  --accent4:   #ffb347;
  --glow1:     rgba(124,106,247,0.3);
  --glow2:     rgba(62,207,207,0.3);
  --glow3:     rgba(240,98,146,0.2);
}

[data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family:var(--font);
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stRadio label { color: var(--text2) !important; font-size:0.86rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }

#MainMenu, footer, header { visibility: hidden; }

/* Page header */
.pg-header {
    padding: 2.5rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.pg-eyebrow {
    font-family:var(--font-mono);
    font-size:0.78rem;
    color: var(--accent2);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.pg-title {
    font-family:var(--font-serif);
    font-size:2.76rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.1;
    margin-bottom: 0.4rem;
}
.pg-title span { color: var(--accent1); }
.pg-sub {
    font-size:1.09rem;
    color: var(--text2);
    font-weight: 300;
}

/* Level badge */
.level-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    font-family:var(--font-mono);
    font-size:0.92rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-weight: 400;
    border: 1px solid;
}
.level-hs   { background: rgba(255,179,71,0.08); border-color: rgba(255,179,71,0.3); color: #ffb347; }
.level-ug   { background: rgba(124,106,247,0.08); border-color: rgba(124,106,247,0.3); color: #7c6af7; }
.level-pg   { background: rgba(62,207,207,0.08); border-color: rgba(62,207,207,0.3); color: #3ecfcf; }
.level-wp   { background: rgba(240,98,146,0.08); border-color: rgba(240,98,146,0.3); color: #f06292; }

/* Section label */
.sec-label {
    font-family:var(--font-mono);
    font-size:0.75rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text3);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.sec-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Career match card */
.cm-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
    height: 100%;
}
.cm-card:hover { border-color: var(--border2); }
.cm-card-accent {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 16px 16px 0 0;
}
.cm-rank {
    font-family:var(--font-serif);
    font-size:3.45rem;
    font-weight: 800;
    line-height: 1;
    opacity: 0.06;
    position: absolute;
    top: 1rem; right: 1.2rem;
}
.cm-title {
    font-family:var(--font-serif);
    font-size:1.32rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.6rem;
    padding-right: 2rem;
    line-height: 1.3;
}
.cm-body {
    font-size:1.01rem;
    color: var(--text2);
    line-height: 1.65;
    font-weight: 300;
}
.cm-tag {
    display: inline-block;
    margin-top: 0.9rem;
    padding: 0.25rem 0.7rem;
    border-radius: 6px;
    font-family:var(--font-mono);
    font-size:0.75rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* Skill pill */
.skill-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.75rem;
    border-radius: 8px;
    font-size:0.92rem;
    margin: 0.2rem;
    font-family:var(--font);
    font-weight: 400;
}
.sp-missing {
    background: rgba(240,98,146,0.08);
    border: 1px solid rgba(240,98,146,0.2);
    color: #f48fa8;
}
.sp-present {
    background: rgba(62,207,207,0.08);
    border: 1px solid rgba(62,207,207,0.2);
    color: #3ecfcf;
}
.sp-dot {
    width: 5px; height: 5px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}

/* Salary band */
.salary-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    margin-top: 0.8rem;
}
.salary-title {
    font-family:var(--font-mono);
    font-size:0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text3);
    margin-bottom: 0.5rem;
}
.salary-value {
    font-family:var(--font-serif);
    font-size:1.61rem;
    font-weight: 700;
    color: var(--accent4);
}
.salary-range {
    font-size:0.92rem;
    color: var(--text2);
    margin-top: 0.2rem;
}

/* Stat chip */
.stat-chip {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.stat-num {
    font-family:var(--font-serif);
    font-size:1.84rem;
    font-weight: 800;
    line-height: 1;
}
.stat-lbl {
    font-size:0.86rem;
    color: var(--text2);
    margin-top: 0.3rem;
}

/* Expander override */
div[data-testid="stExpander"] {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
div[data-testid="stExpander"] summary {
    color: var(--text) !important;
    font-family:var(--font) !important;
}

/* Button */
div.stButton > button {
    background: var(--accent1) !important;
    color: #fff !important;
    font-family:var(--font-serif) !important;
    font-weight: 600 !important;
    font-size:0.94rem !important;
    letter-spacing: 0.06em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.8rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 24px var(--glow1) !important;
}
div.stButton > button:hover {
    box-shadow: 0 0 40px var(--glow1) !important;
    transform: translateY(-1px) !important;
}

/* Select / multiselect / text input */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div {
    background: var(--bg3) !important;
    border-color: var(--border2) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
div[data-testid="stTextInput"] input {
    background: var(--bg3) !important;
    border-color: var(--border2) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}

/* Radio */
div[data-testid="stRadio"] > div { gap: 0.5rem !important; }
div[data-testid="stRadio"] label { color: var(--text2) !important; font-size:1.01rem !important; }

/* Warning */
div[data-testid="stAlert"] {
    background: rgba(255,179,71,0.06) !important;
    border: 1px solid rgba(255,179,71,0.2) !important;
    border-radius: 10px !important;
    color: #ffb347 !important;
}

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent1), var(--accent2)) !important;
    border-radius: 10px !important;
}

/* Multiselect tag */
span[data-baseweb="tag"] {
    background: var(--bg4) !important;
    border: 1px solid var(--border2) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ─── LEVEL CONFIG ─────────────────────────────────────────────────────────────
LEVELS = {
    "Higher Secondary (11th–12th)": {
        "code": "hs",
        "badge_class": "level-hs",
        "label": "Higher Secondary",
        "accent": "#ffb347",
        "accent_glow": "rgba(255,179,71,0.25)",
        "focus": "career paths, stream selection, govt vs private roles, entrance exams",
        "sections": ["career_matches", "stream_guidance", "govt_vs_private", "skill_gap", "roadmap", "entrance_exams"],
        "prompt_extras": """
Also include:
- stream_guidance: { recommended_stream: str, reason: str, alternative_stream: str }
- govt_vs_private: { govt_roles: [list of 3 roles], private_roles: [list of 3 roles], recommendation: str }
- entrance_exams: [{ name: str, description: str, eligibility: str }] (3 relevant exams)
- salary_entry: "Entry level salary range (Indian context)"
"""
    },
    "Undergraduate / College": {
        "code": "ug",
        "badge_class": "level-ug",
        "label": "Undergraduate",
        "accent": "#7c6af7",
        "accent_glow": "rgba(124,106,247,0.25)",
        "focus": "industry trends, internships, skill gaps, course recommendations, placements",
        "sections": ["career_matches", "industry_trends", "internship_guide", "skill_gap", "roadmap", "course_recommendations"],
        "prompt_extras": """
Also include:
- industry_trends: [{ trend: str, impact: str, relevance: str }] (3 trends)
- internship_guide: { platforms: [list of 4], tips: str, timeline: str }
- course_recommendations: [{ name: str, platform: str, duration: str, why: str }] (3 courses)
- salary_entry: "Expected fresher CTC range"
- placement_rate: "Estimated placement rate percentage"
"""
    },
    "Postgraduate": {
        "code": "pg",
        "badge_class": "level-pg",
        "label": "Postgraduate",
        "accent": "#3ecfcf",
        "accent_glow": "rgba(62,207,207,0.25)",
        "focus": "research paths, PhD opportunities, academia vs industry, specialisations, global opportunities",
        "sections": ["career_matches", "academia_vs_industry", "specialisations", "skill_gap", "roadmap", "global_opportunities"],
        "prompt_extras": """
Also include:
- academia_vs_industry: { academia: { pros: [2], cons: [2] }, industry: { pros: [2], cons: [2] }, recommendation: str }
- specialisations: [{ name: str, scope: str, top_institutes: str }] (3 specialisations)
- global_opportunities: [{ country: str, opportunity: str, visa_info: str }] (3 countries)
- salary_entry: "Expected salary range (India + Global)"
- phd_scope: "PhD/research potential in this field"
"""
    },
    "Working Professional": {
        "code": "wp",
        "badge_class": "level-wp",
        "label": "Professional",
        "accent": "#f06292",
        "accent_glow": "rgba(240,98,146,0.25)",
        "focus": "career pivots, upskilling, leadership paths, industry demand, salary negotiation",
        "sections": ["career_matches", "pivot_analysis", "upskilling_plan", "skill_gap", "roadmap", "leadership_paths"],
        "prompt_extras": """
Also include:
- pivot_analysis: { pivot_ease: "Easy/Medium/Hard", reason: str, transition_time: str, risk_level: str }
- upskilling_plan: [{ skill: str, resource: str, time_to_learn: str, priority: "High/Medium/Low" }] (4 items)
- leadership_paths: [{ title: str, timeline: str, requirements: str }] (3 paths)
- salary_entry: "Current market salary range for this role"
- demand_index: "Job market demand score out of 10"
"""
    }
}

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 0.8rem; border-bottom:1px solid rgba(255,255,255,0.06); margin-bottom:1.2rem;">
        <div style="font-family:var(--font-serif); font-size:1.15rem; font-weight:700; color:#e8e8f0;">Career Analysis</div>
        <div style="font-size:0.86rem; color:#5a5a72; margin-top:0.2rem;">Fill your profile to get started</div>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Your Name", placeholder="e.g. Arjun Sharma")

    qualification = st.selectbox("Qualification Level",
        list(LEVELS.keys()),
        index=0
    )

    st.markdown("---")

    existing_profile = st.session_state.get("profile", {})
    form_data = {}

    if qualification == "Higher Secondary (11th–12th)":
        form_data["current_stream"] = st.radio("Current Stream", ["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", "Not decided yet"], index=["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", "Not decided yet"].index(existing_profile.get("current_stream", "Science (PCM)")) if existing_profile.get("current_stream") in ["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", "Not decided yet"] else 0)
        form_data["subjects"] = st.multiselect("Favourite Subjects", ["Mathematics","Physics","Chemistry","Biology","Computer Science","Economics","Psychology","History","Literature","Art","Commerce","Political Science","Statistics","Geography"], default=existing_profile.get("subjects", []))
        form_data["learning_style"] = st.radio("Preferred Learning Style", ["Practical/Hands-on", "Theoretical/Reading", "Visual", "Interactive"], index=["Practical/Hands-on", "Theoretical/Reading", "Visual", "Interactive"].index(existing_profile.get("learning_style", "Practical/Hands-on")) if existing_profile.get("learning_style") in ["Practical/Hands-on", "Theoretical/Reading", "Visual", "Interactive"] else 0)
        form_data["strengths"] = st.multiselect("Key Strengths", ["Logical Reasoning", "Creativity", "Communication", "Memorization", "Problem Solving", "Leadership"], default=existing_profile.get("strengths", []))
        form_data["extracurricular"] = st.multiselect("Extracurricular Interests", ["Sports", "Arts", "Coding", "Debating", "Music", "Volunteering"], default=existing_profile.get("extracurricular", []))
        form_data["career_goal"] = st.radio("Primary Goal after 12th", ["Top University", "Quick Job", "Entrepreneurship", "Govt Job", "Undecided"], index=["Top University", "Quick Job", "Entrepreneurship", "Govt Job", "Undecided"].index(existing_profile.get("career_goal", "Top University")) if existing_profile.get("career_goal") in ["Top University", "Quick Job", "Entrepreneurship", "Govt Job", "Undecided"] else 0)

    elif qualification == "Undergraduate / College":
        form_data["current_course"] = st.text_input("Current Course/Degree", value=existing_profile.get("current_course", ""), placeholder="e.g. B.Tech CSE, BBA...")
        form_data["years_remaining"] = st.radio("Years Remaining", ["3rd Year", "2nd Year", "Final Year", "Just Started"], index=["3rd Year", "2nd Year", "Final Year", "Just Started"].index(existing_profile.get("years_remaining", "3rd Year")) if existing_profile.get("years_remaining") in ["3rd Year", "2nd Year", "Final Year", "Just Started"] else 0)
        form_data["academic_perf"] = st.radio("Academic Performance", ["Excellent", "Average", "Struggling"], index=["Excellent", "Average", "Struggling"].index(existing_profile.get("academic_perf", "Average")) if existing_profile.get("academic_perf") in ["Excellent", "Average", "Struggling"] else 1)
        form_data["practical_exp"] = st.multiselect("Practical Experience", ["Internships", "Projects", "Competitions", "Freelancing", "None yet"], default=existing_profile.get("practical_exp", []))
        form_data["soft_skills"] = st.multiselect("Soft Skills", ["Leadership", "Teamwork", "Problem Solving", "Public Speaking", "Writing"], default=existing_profile.get("soft_skills", []))
        form_data["ideal_setting"] = st.radio("Ideal Work Setting", ["Fast-paced/Startup", "Structured/MNC", "Remote", "Fieldwork"], index=["Fast-paced/Startup", "Structured/MNC", "Remote", "Fieldwork"].index(existing_profile.get("ideal_setting", "Structured/MNC")) if existing_profile.get("ideal_setting") in ["Fast-paced/Startup", "Structured/MNC", "Remote", "Fieldwork"] else 1)
        form_data["career_goal"] = st.radio("Career Goal", ["Corporate Job", "Startup/Founder", "Higher Studies", "Freelancing"], index=["Corporate Job", "Startup/Founder", "Higher Studies", "Freelancing"].index(existing_profile.get("career_goal", "Corporate Job")) if existing_profile.get("career_goal") in ["Corporate Job", "Startup/Founder", "Higher Studies", "Freelancing"] else 0)

    elif qualification == "Postgraduate":
        form_data["pg_specialisation"] = st.text_input("PG Specialisation", value=existing_profile.get("pg_specialisation", ""), placeholder="e.g. M.Tech AI, MBA Finance...")
        form_data["research_interest"] = st.radio("Research Interest", ["High - Want to do PhD", "Medium - Open to it", "Low - Prefer industry"], index=["High - Want to do PhD", "Medium - Open to it", "Low - Prefer industry"].index(existing_profile.get("research_interest", "Medium - Open to it")) if existing_profile.get("research_interest") in ["High - Want to do PhD", "Medium - Open to it", "Low - Prefer industry"] else 1)
        form_data["niche_skills"] = st.text_input("Key Expertise / Niche Skills", value=existing_profile.get("niche_skills", ""), placeholder="e.g. Python, Financial Modeling...")
        form_data["prof_exp"] = st.text_input("Professional Experience (if any)", value=existing_profile.get("prof_exp", ""), placeholder="e.g. 2 years at Deloitte...")
        form_data["relocate"] = st.radio("Willingness to Relocate", ["Global", "Domestic", "No preference", "Will not relocate"], index=["Global", "Domestic", "No preference", "Will not relocate"].index(existing_profile.get("relocate", "No preference")) if existing_profile.get("relocate") in ["Global", "Domestic", "No preference", "Will not relocate"] else 2)
        form_data["career_obj"] = st.radio("Career Objective", ["Academia/Research", "Industry Leadership", "Specialized Consultant", "R&D"], index=["Academia/Research", "Industry Leadership", "Specialized Consultant", "R&D"].index(existing_profile.get("career_obj", "Industry Leadership")) if existing_profile.get("career_obj") in ["Academia/Research", "Industry Leadership", "Specialized Consultant", "R&D"] else 1)
        form_data["work_values"] = st.multiselect("Work Values", ["High Salary", "Work-Life Balance", "Impact/Social Good", "Innovation", "Job Security"], default=existing_profile.get("work_values", []))

    elif qualification == "Working Professional":
        form_data["current_role"] = st.text_input("Current Role", value=existing_profile.get("current_role", ""), placeholder="e.g. Software Engineer")
        form_data["years_exp"] = st.selectbox("Years of Experience", ["0–2 years", "3–5 years", "6–10 years", "10+ years"], index=["0–2 years", "3–5 years", "6–10 years", "10+ years"].index(existing_profile.get("years_exp", "0–2 years")) if existing_profile.get("years_exp") in ["0–2 years", "3–5 years", "6–10 years", "10+ years"] else 0)
        form_data["core_comp"] = st.text_input("Core Competencies / Specialized Skills", value=existing_profile.get("core_comp", ""), placeholder="e.g. Cloud Architecture, B2B Sales...")
        form_data["pivot_intent"] = st.radio("Pivot Intent", ["Grow in current field", "Switch domain entirely", "Move to leadership", "Start own venture"], index=["Grow in current field", "Switch domain entirely", "Move to leadership", "Start own venture"].index(existing_profile.get("pivot_intent", "Grow in current field")) if existing_profile.get("pivot_intent") in ["Grow in current field", "Switch domain entirely", "Move to leadership", "Start own venture"] else 0)
        form_data["frustration"] = st.radio("Biggest Career Frustration", ["Lack of growth", "Low pay", "Poor work-life balance", "Boredom", "None"], index=["Lack of growth", "Low pay", "Poor work-life balance", "Boredom", "None"].index(existing_profile.get("frustration", "None")) if existing_profile.get("frustration") in ["Lack of growth", "Low pay", "Poor work-life balance", "Boredom", "None"] else 4)
        form_data["company_stage"] = st.radio("Preferred Company Stage", ["Early-stage startup", "Mid-size", "Enterprise/MNC"], index=["Early-stage startup", "Mid-size", "Enterprise/MNC"].index(existing_profile.get("company_stage", "Enterprise/MNC")) if existing_profile.get("company_stage") in ["Early-stage startup", "Mid-size", "Enterprise/MNC"] else 2)

    level_cfg = LEVELS[qualification]

    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("⟶ Analyse My Profile")

# ─── PAGE HEADER ──────────────────────────────────────────────────────────────
lc = LEVELS[qualification]
st.markdown(f"""
<div class="pg-header">
    <div class="pg-eyebrow">03 / Career Analysis</div>
    <div class="pg-title">Your <span>Career</span> Intelligence Report</div>
    <div style="display:flex; align-items:center; gap:1rem; margin-top:0.8rem;">
        <span class="level-badge {lc['badge_class']}">
            <span style="width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;"></span>
            {lc['label']}
        </span>
        <span class="pg-sub">Adaptive analysis tailored to your level</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── IDLE STATE ───────────────────────────────────────────────────────────────
if not analyze_btn:
    cols = st.columns(4)
    items = [
        ("#7c6af7", "rgba(124,106,247,0.08)", "Career Matches", "Top 3 AI-matched careers for your profile"),
        ("#3ecfcf", "rgba(62,207,207,0.08)", "Skill Gap Map", "What you have vs what you need"),
        ("#f06292", "rgba(240,98,146,0.08)", "Visual Roadmap", "Glowing orb milestone path"),
        ("#ffb347", "rgba(255,179,71,0.08)", "Level Insights", "Adaptive sections for your stage"),
    ]
    for col, (accent, bg, title, desc) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div style="background:{bg};border:1px solid {accent}22;border-radius:14px;padding:1.4rem;height:130px;">
                <div style="width:8px;height:8px;border-radius:50%;background:{accent};margin-bottom:0.8rem;box-shadow:0 0 10px {accent};"></div>
                <div style="font-family:var(--font-serif);font-weight:600;font-size:1.06rem;color:#e8e8f0;margin-bottom:0.4rem;">{title}</div>
                <div style="font-size:0.9rem;color:#9898b0;line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-top:3rem;padding:2rem;border:1px dashed rgba(255,255,255,0.07);border-radius:16px;">
        <div style="font-family:var(--font-serif);font-size:1.26rem;font-weight:600;color:#5a5a72;margin-bottom:0.4rem;">Fill in your profile</div>
        <div style="font-size:0.98rem;color:#3a3a52;">Complete the sidebar and click Analyse My Profile</div>
    </div>
    """, unsafe_allow_html=True)

else:
    if not name:
        st.warning("Please fill in your name to continue.")
        st.stop()

    # Format the profile data into a readable string for the prompt
    profile_details = ""
    for key, value in form_data.items():
        if isinstance(value, list):
            value = ", ".join(value)
        # Format the key nicely (e.g. 'current_stream' -> 'Current Stream')
        formatted_key = key.replace("_", " ").title()
        profile_details += f"{formatted_key}: {value}\n"

    # ── BUILD PROMPT ──────────────────────────────────────────────────────────
    prompt = f"""
You are an elite AI career counselor. Analyse this student's profile and return ONLY a valid JSON object.

Student: {name}
Qualification Level: {qualification}

--- Student Profile ---
{profile_details.strip()}
-----------------------

Focus areas for this level: {level_cfg['focus']}

Return ONLY valid JSON (no markdown, no backticks, no preamble) in this exact format:
{{
  "summary": "2-sentence personalised summary of this student's career profile",
  "match_score": 87,
  "careers": [
    {{
      "title": "Career Title",
      "tagline": "5-word punchy tagline",
      "reason": "Why this suits them — 2-3 sentences personalised",
      "skills_missing": ["skill1", "skill2", "skill3", "skill4"],
      "skills_present": ["skill1", "skill2", "skill3"],
      "demand": "High/Medium/Low",
      "growth": "X% growth expected in 5 years",
      "roadmap": [
        {{"step": 1, "milestone": "Short title", "detail": "What to do and why", "duration": "e.g. 6 months"}},
        {{"step": 2, "milestone": "Short title", "detail": "What to do and why", "duration": "e.g. 1 year"}},
        {{"step": 3, "milestone": "Short title", "detail": "What to do and why", "duration": "e.g. 6 months"}},
        {{"step": 4, "milestone": "Short title", "detail": "What to do and why", "duration": "e.g. 1 year"}},
        {{"step": 5, "milestone": "Short title", "detail": "What to do and why", "duration": "e.g. ongoing"}}
      ]
    }},
    {{
      "title": "Career Title 2",
      "tagline": "5-word punchy tagline",
      "reason": "Why this suits them",
      "skills_missing": ["skill1", "skill2"],
      "skills_present": ["skill1", "skill2"],
      "demand": "High/Medium/Low",
      "growth": "X% growth",
      "roadmap": [
        {{"step": 1, "milestone": "Title", "detail": "Detail", "duration": "time"}},
        {{"step": 2, "milestone": "Title", "detail": "Detail", "duration": "time"}},
        {{"step": 3, "milestone": "Title", "detail": "Detail", "duration": "time"}},
        {{"step": 4, "milestone": "Title", "detail": "Detail", "duration": "time"}},
        {{"step": 5, "milestone": "Title", "detail": "Detail", "duration": "time"}}
      ]
    }},
    {{
      "title": "Career Title 3",
      "tagline": "5-word punchy tagline",
      "reason": "Why this suits them",
      "skills_missing": ["skill1"],
      "skills_present": ["skill1", "skill2"],
      "demand": "High/Medium/Low",
      "growth": "X% growth",
      "roadmap": [
        {{"step": 1, "milestone": "Title", "detail": "Detail", "duration": "time"}},
        {{"step": 2, "milestone": "Title", "detail": "Detail", "duration": "time"}},
        {{"step": 3, "milestone": "Title", "detail": "Detail", "duration": "time"}},
        {{"step": 4, "milestone": "Title", "detail": "Detail", "duration": "time"}},
        {{"step": 5, "milestone": "Title", "detail": "Detail", "duration": "time"}}
      ]
    }}
  ]
  {level_cfg['prompt_extras']}
}}
"""

    # ── API CALL ──────────────────────────────────────────────────────────────
    prog = st.progress(0, text="Scanning profile...")
    time.sleep(0.3)
    prog.progress(25, text="Matching careers with AI...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4000,
    )

    prog.progress(70, text="Building your report...")
    time.sleep(0.3)

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        data = json.loads(raw)
        careers = data["careers"]
    except Exception as e:
        st.error(f"Could not parse AI response. Please try again. ({e})")
        st.stop()

    prog.progress(100, text="Done!")
    time.sleep(0.3)
    prog.empty()

    # ── PROFILE SUMMARY BANNER ────────────────────────────────────────────────
    match_score = data.get("match_score", 88)
    summary = data.get("summary", "")

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(124,106,247,0.08),rgba(62,207,207,0.05));
                border:1px solid rgba(124,106,247,0.2);border-radius:16px;padding:1.6rem 2rem;
                display:flex;align-items:center;gap:2rem;margin-bottom:2rem;flex-wrap:wrap;">
        <div style="flex:1;min-width:200px;">
            <div style="font-family:var(--font-mono);font-size:0.75rem;letter-spacing:0.15em;
                        text-transform:uppercase;color:#5a5a72;margin-bottom:0.4rem;">Profile Summary · {name}</div>
            <div style="font-size:1.06rem;color:#c8c8e0;line-height:1.6;font-weight:300;">{summary}</div>
        </div>
        <div style="text-align:center;flex-shrink:0;">
            <div style="font-family:var(--font-serif);font-size:3.22rem;font-weight:800;
                        background:linear-gradient(135deg,#7c6af7,#3ecfcf);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1;">{match_score}</div>
            <div style="font-size:0.92rem;color:#5a5a72;letter-spacing:0.1em;text-transform:uppercase;margin-top:0.2rem;">Match Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TOP 3 CAREER CARDS ────────────────────────────────────────────────────
    st.markdown('<div class="sec-label">Top 3 Career Matches</div>', unsafe_allow_html=True)

    accent_colors = [lc["accent"], "#7c6af7", "#3ecfcf"]
    accent_glows  = [lc["accent_glow"], "rgba(124,106,247,0.2)", "rgba(62,207,207,0.2)"]
    rank_labels   = ["01", "02", "03"]
    demand_colors = {"High": "#3ecfcf", "Medium": "#ffb347", "Low": "#f06292"}

    cols = st.columns(3)
    for i, (col, career) in enumerate(zip(cols, careers)):
        demand = career.get("demand", "Medium")
        dc = demand_colors.get(demand, "#ffb347")
        with col:
            st.markdown(f"""
            <div class="cm-card" style="border-color:{accent_colors[i]}22;">
                <div class="cm-card-accent" style="background:linear-gradient(90deg,{accent_colors[i]},{accent_colors[i]}44);"></div>
                <div class="cm-rank" style="color:{accent_colors[i]};">{rank_labels[i]}</div>
                <div class="cm-title">{career['title']}</div>
                <div style="font-family:var(--font-mono);font-size:0.78rem;
                            color:{accent_colors[i]};letter-spacing:0.08em;margin-bottom:0.8rem;
                            opacity:0.8;">{career.get('tagline','')}</div>
                <div class="cm-body">{career['reason']}</div>
                <div style="margin-top:1rem;display:flex;gap:0.6rem;flex-wrap:wrap;">
                    <div style="background:{dc}15;border:1px solid {dc}40;color:{dc};
                                padding:0.2rem 0.6rem;border-radius:6px;font-size:0.8rem;
                                font-family:var(--font-mono);">
                        {demand} Demand
                    </div>
                    <div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
                                color:#9898b0;padding:0.2rem 0.6rem;border-radius:6px;
                                font-size:0.8rem;font-family:var(--font-mono);">
                        {career.get('growth','—')}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── LEVEL-SPECIFIC SECTIONS ───────────────────────────────────────────────
    if level_cfg["code"] == "hs":
        st.markdown('<div class="sec-label">Stream Guidance</div>', unsafe_allow_html=True)
        sg = data.get("stream_guidance", {})
        gp = data.get("govt_vs_private", {})
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:rgba(255,179,71,0.06);border:1px solid rgba(255,179,71,0.15);
                        border-radius:14px;padding:1.4rem;">
                <div style="font-family:var(--font-serif);font-weight:700;font-size:1.15rem;
                            color:#ffb347;margin-bottom:0.5rem;">Recommended Stream</div>
                <div style="font-family:var(--font-serif);font-size:1.72rem;font-weight:800;
                            color:#e8e8f0;margin-bottom:0.6rem;">{sg.get('recommended_stream','—')}</div>
                <div style="font-size:0.98rem;color:#9898b0;line-height:1.6;">{sg.get('reason','')}</div>
                <div style="margin-top:0.8rem;font-size:0.9rem;color:#5a5a72;">
                    Alternative: <span style="color:#ffb347;">{sg.get('alternative_stream','—')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:rgba(124,106,247,0.06);border:1px solid rgba(124,106,247,0.15);
                        border-radius:14px;padding:1.4rem;">
                <div style="font-family:var(--font-serif);font-weight:700;font-size:1.03rem;
                            color:#7c6af7;margin-bottom:0.8rem;">Govt vs Private Roles</div>
                <div style="display:flex;gap:1rem;">
                    <div style="flex:1;">
                        <div style="font-size:0.8rem;color:#5a5a72;text-transform:uppercase;
                                    letter-spacing:0.1em;margin-bottom:0.4rem;">Govt</div>
                        {"".join([f'<div style="font-size:0.94rem;color:#c8c8e0;padding:0.2rem 0;">· {r}</div>' for r in gp.get('govt_roles',[])])}
                    </div>
                    <div style="width:1px;background:rgba(255,255,255,0.06);"></div>
                    <div style="flex:1;">
                        <div style="font-size:0.8rem;color:#5a5a72;text-transform:uppercase;
                                    letter-spacing:0.1em;margin-bottom:0.4rem;">Private</div>
                        {"".join([f'<div style="font-size:0.94rem;color:#c8c8e0;padding:0.2rem 0;">· {r}</div>' for r in gp.get('private_roles',[])])}
                    </div>
                </div>
                <div style="margin-top:0.8rem;font-size:0.92rem;color:#9898b0;border-top:1px solid rgba(255,255,255,0.05);padding-top:0.8rem;">
                    {gp.get('recommendation','')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Entrance exams
        exams = data.get("entrance_exams", [])
        if exams:
            st.markdown('<div class="sec-label" style="margin-top:1.5rem;">Relevant Entrance Exams</div>', unsafe_allow_html=True)
            ecols = st.columns(len(exams))
            for col, exam in zip(ecols, exams):
                with col:
                    st.markdown(f"""
                    <div style="background:rgba(255,179,71,0.05);border:1px solid rgba(255,179,71,0.12);
                                border-radius:12px;padding:1.2rem;">
                        <div style="font-family:var(--font-serif);font-weight:700;font-size:1.09rem;
                                    color:#ffb347;margin-bottom:0.4rem;">{exam.get('name','')}</div>
                        <div style="font-size:0.92rem;color:#9898b0;margin-bottom:0.5rem;">{exam.get('description','')}</div>
                        <div style="font-size:0.92rem;color:#5a5a72;">Eligible: {exam.get('eligibility','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

    elif level_cfg["code"] == "ug":
        st.markdown('<div class="sec-label">Industry Trends & Opportunities</div>', unsafe_allow_html=True)
        trends = data.get("industry_trends", [])
        intern = data.get("internship_guide", {})
        courses = data.get("course_recommendations", [])

        # Trends
        tcols = st.columns(len(trends) if trends else 1)
        for col, trend in zip(tcols, trends):
            with col:
                st.markdown(f"""
                <div style="background:rgba(124,106,247,0.06);border:1px solid rgba(124,106,247,0.15);
                            border-radius:12px;padding:1.2rem;height:100%;">
                    <div style="font-family:var(--font-serif);font-weight:700;font-size:1.03rem;
                                color:#7c6af7;margin-bottom:0.5rem;">{trend.get('trend','')}</div>
                    <div style="font-size:0.94rem;color:#9898b0;margin-bottom:0.5rem;">{trend.get('impact','')}</div>
                    <div style="font-size:0.9rem;color:#5a5a72;">{trend.get('relevance','')}</div>
                </div>
                """, unsafe_allow_html=True)

        # Internship + Courses
        st.markdown("<br>", unsafe_allow_html=True)
        ic1, ic2 = st.columns([1, 2])
        with ic1:
            st.markdown(f"""
            <div style="background:rgba(62,207,207,0.05);border:1px solid rgba(62,207,207,0.15);
                        border-radius:12px;padding:1.3rem;">
                <div style="font-family:var(--font-serif);font-weight:700;font-size:1.03rem;
                            color:#3ecfcf;margin-bottom:0.8rem;">Internship Guide</div>
                <div style="font-size:0.92rem;color:#9898b0;margin-bottom:0.6rem;">{intern.get('tips','')}</div>
                <div style="font-size:0.86rem;color:#5a5a72;margin-bottom:0.5rem;">Timeline: {intern.get('timeline','')}</div>
                <div style="display:flex;flex-wrap:wrap;gap:0.3rem;margin-top:0.5rem;">
                    {"".join([f'<span style="background:rgba(62,207,207,0.08);border:1px solid rgba(62,207,207,0.2);color:#3ecfcf;padding:0.2rem 0.5rem;border-radius:6px;font-size:0.92rem;">{p}</span>' for p in intern.get('platforms',[])])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with ic2:
            st.markdown('<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;letter-spacing:0.15em;text-transform:uppercase;color:#5a5a72;margin-bottom:0.8rem;">Recommended Courses</div>', unsafe_allow_html=True)
            for course in courses:
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
                            border-radius:10px;padding:0.9rem 1rem;margin-bottom:0.5rem;
                            display:flex;align-items:center;gap:1rem;">
                    <div style="flex:1;">
                        <div style="font-size:1.01rem;color:#e8e8f0;font-weight:500;">{course.get('name','')}</div>
                        <div style="font-size:0.86rem;color:#5a5a72;margin-top:0.2rem;">{course.get('platform','')} · {course.get('duration','')}</div>
                    </div>
                    <div style="font-size:0.86rem;color:#9898b0;max-width:160px;text-align:right;">{course.get('why','')}</div>
                </div>
                """, unsafe_allow_html=True)

    elif level_cfg["code"] == "pg":
        st.markdown('<div class="sec-label">Academia vs Industry & Global Scope</div>', unsafe_allow_html=True)
        avi = data.get("academia_vs_industry", {})
        specs = data.get("specialisations", [])
        global_ops = data.get("global_opportunities", [])

        ac1, ac2 = st.columns(2)
        for col, key, title, color in [(ac1, "academia", "Academia Path", "#3ecfcf"), (ac2, "industry", "Industry Path", "#7c6af7")]:
            with col:
                section = avi.get(key, {})
                pros = section.get("pros", [])
                cons = section.get("cons", [])
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
                            border-radius:12px;padding:1.3rem;">
                    <div style="font-family:var(--font-serif);font-weight:700;color:{color};
                                margin-bottom:0.8rem;font-size:1.09rem;">{title}</div>
                    {"".join([f'<div style="font-size:0.94rem;color:#9898b0;padding:0.2rem 0;">✓ {p}</div>' for p in pros])}
                    {"".join([f'<div style="font-size:0.94rem;color:#5a5a72;padding:0.2rem 0;">✗ {c}</div>' for c in cons])}
                </div>
                """, unsafe_allow_html=True)

        if avi.get("recommendation"):
            st.markdown(f"""
            <div style="background:rgba(62,207,207,0.05);border:1px solid rgba(62,207,207,0.15);
                        border-radius:10px;padding:1rem 1.2rem;margin-top:0.8rem;
                        font-size:0.98rem;color:#9898b0;">{avi['recommendation']}</div>
            """, unsafe_allow_html=True)

        # Global opportunities
        if global_ops:
            st.markdown('<div class="sec-label" style="margin-top:1.5rem;">Global Opportunities</div>', unsafe_allow_html=True)
            gcols = st.columns(len(global_ops))
            for col, op in zip(gcols, global_ops):
                with col:
                    st.markdown(f"""
                    <div style="background:rgba(62,207,207,0.04);border:1px solid rgba(62,207,207,0.12);
                                border-radius:12px;padding:1.2rem;">
                        <div style="font-family:var(--font-serif);font-weight:700;font-size:1.15rem;
                                    color:#3ecfcf;">{op.get('country','')}</div>
                        <div style="font-size:0.94rem;color:#c8c8e0;margin:0.4rem 0;">{op.get('opportunity','')}</div>
                        <div style="font-size:0.86rem;color:#5a5a72;">{op.get('visa_info','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

    elif level_cfg["code"] == "wp":
        st.markdown('<div class="sec-label">Career Pivot & Growth Analysis</div>', unsafe_allow_html=True)
        pivot = data.get("pivot_analysis", {})
        upskill = data.get("upskilling_plan", [])
        leadership = data.get("leadership_paths", [])

        risk_colors = {"Easy": "#3ecfcf", "Medium": "#ffb347", "Hard": "#f06292"}
        priority_colors = {"High": "#f06292", "Medium": "#ffb347", "Low": "#3ecfcf"}

        pc1, pc2, pc3, pc4 = st.columns(4)
        stats = [
            (pivot.get("pivot_ease", "—"), "Pivot Ease", "#3ecfcf"),
            (pivot.get("transition_time", "—"), "Transition Time", "#ffb347"),
            (pivot.get("risk_level", "—"), "Risk Level", "#f06292"),
            (data.get("demand_index", "—"), "Market Demand", "#7c6af7"),
        ]
        for col, (val, lbl, color) in zip([pc1, pc2, pc3, pc4], stats):
            with col:
                st.markdown(f"""
                <div class="stat-chip">
                    <div class="stat-num" style="color:{color};">{val}</div>
                    <div class="stat-lbl">{lbl}</div>
                </div>
                """, unsafe_allow_html=True)

        if pivot.get("reason"):
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);
                        border-radius:10px;padding:1rem 1.2rem;margin:0.8rem 0;
                        font-size:0.98rem;color:#9898b0;">{pivot['reason']}</div>
            """, unsafe_allow_html=True)

        # Upskilling plan
        if upskill:
            st.markdown('<div class="sec-label" style="margin-top:1.2rem;">Upskilling Plan</div>', unsafe_allow_html=True)
            for item in upskill:
                pc = priority_colors.get(item.get("priority", "Medium"), "#ffb347")
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
                            border-radius:10px;padding:0.9rem 1.1rem;margin-bottom:0.4rem;
                            display:flex;align-items:center;gap:1.2rem;flex-wrap:wrap;">
                    <div style="width:6px;height:6px;border-radius:50%;background:{pc};
                                box-shadow:0 0 8px {pc};flex-shrink:0;"></div>
                    <div style="flex:1;min-width:120px;">
                        <div style="font-size:1.01rem;color:#e8e8f0;font-weight:500;">{item.get('skill','')}</div>
                        <div style="font-size:0.86rem;color:#5a5a72;margin-top:0.1rem;">{item.get('resource','')}</div>
                    </div>
                    <div style="font-size:0.86rem;color:#9898b0;">{item.get('time_to_learn','')}</div>
                    <div style="background:{pc}15;border:1px solid {pc}30;color:{pc};
                                padding:0.2rem 0.6rem;border-radius:6px;font-size:0.8rem;
                                font-family:var(--font-mono);">{item.get('priority','')}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── SALARY BAND (all levels) ───────────────────────────────────────────────
    salary_entry = data.get("salary_entry", "")
    if salary_entry:
        st.markdown(f"""
        <div class="salary-card" style="margin-top:1rem;">
            <div class="salary-title">Salary Insight</div>
            <div class="salary-value">{salary_entry}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── SKILL GAP ANALYSIS ────────────────────────────────────────────────────
    st.markdown('<div class="sec-label" style="margin-top:2rem;">Skill Gap Analysis</div>', unsafe_allow_html=True)
    for i, career in enumerate(careers):
        with st.expander(f"{rank_labels[i]}  {career['title']}", expanded=(i == 0)):
            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown('<div style="font-size:0.86rem;color:#5a5a72;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem;">Skills to Acquire</div>', unsafe_allow_html=True)
                pills = "".join([f'<span class="skill-pill sp-missing"><span class="sp-dot" style="background:#f06292;"></span>{s}</span>' for s in career.get("skills_missing", [])])
                st.markdown(pills, unsafe_allow_html=True)
            with sc2:
                st.markdown('<div style="font-size:0.86rem;color:#5a5a72;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.6rem;">Skills You Already Have</div>', unsafe_allow_html=True)
                pills = "".join([f'<span class="skill-pill sp-present"><span class="sp-dot" style="background:#3ecfcf;"></span>{s}</span>' for s in career.get("skills_present", [])])
                st.markdown(pills, unsafe_allow_html=True)

    # ── GLOWING ORB CAREER ROADMAP TREE ───────────────────────────────────────
    st.markdown('<div class="sec-label" style="margin-top:2rem;">Career Path Roadmap</div>', unsafe_allow_html=True)

    tree_careers = []
    for i, career in enumerate(careers):
        nodes = []
        for step in career.get("roadmap", []):
            nodes.append({
                "label": step["milestone"],
                "detail": step["detail"],
                "duration": step.get("duration", ""),
                "step": step["step"]
            })
        tree_careers.append({
            "title": career["title"],
            "tagline": career.get("tagline", ""),
            "color": accent_colors[i],
            "glow": accent_glows[i],
            "nodes": nodes
        })

    tree_json = json.dumps(tree_careers)

    roadmap_html = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@300;400&family=JetBrains+Mono:wght@300;400&display=swap');

.rm-root {{
    background: #13131a;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 2.5rem 1.5rem 2rem;
    overflow-x: auto;
    position: relative;
}}

.rm-canvas {{
    display: flex;
    gap: 0;
    justify-content: center;
    min-width: fit-content;
    align-items: flex-start;
    padding: 0 1rem;
}}

.rm-col {{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 200px;
    position: relative;
}}

.rm-col-header {{
    text-align: center;
    margin-bottom: 2rem;
    padding: 0 0.5rem;
}}

.rm-col-title {{
    font-family:var(--font-serif);
    font-size:0.9rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    line-height: 1.3;
    margin-bottom: 0.3rem;
}}

.rm-col-tag {{
    font-family:var(--font-mono);
    font-size:0.69rem;
    letter-spacing: 0.06em;
    opacity: 0.5;
}}

.rm-node-wrap {{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    position: relative;
    z-index: 2;
}}

.rm-orb-container {{
    position: relative;
    width: 44px;
    height: 44px;
    cursor: pointer;
}}

.rm-orb-ring {{
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    border: 1.5px solid;
    opacity: 0.35;
    animation: rm-ring-pulse 2.5s ease-in-out infinite;
}}

.rm-orb-ring2 {{
    position: absolute;
    inset: -10px;
    border-radius: 50%;
    border: 1px solid;
    opacity: 0.15;
    animation: rm-ring-pulse 2.5s ease-in-out infinite 0.5s;
}}

@keyframes rm-ring-pulse {{
    0%, 100% {{ transform: scale(1); opacity: 0.35; }}
    50%        {{ transform: scale(1.08); opacity: 0.15; }}
}}

.rm-orb {{
    position: absolute;
    inset: 0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family:var(--font-mono);
    font-size:0.92rem;
    font-weight: 400;
    transition: transform 0.25s cubic-bezier(0.34,1.56,0.64,1);
}}

.rm-orb-container:hover .rm-orb {{ transform: scale(1.18); }}
.rm-orb-container:hover .rm-orb-ring {{ opacity: 0.6; animation-play-state: paused; transform: scale(1.1); }}
.rm-orb-container:hover .rm-tooltip {{ opacity: 1; transform: translateY(0) scale(1); pointer-events: auto; }}

.rm-node-label {{
    font-family:var(--font);
    font-size:0.92rem;
    font-weight: 400;
    text-align: center;
    max-width: 120px;
    line-height: 1.4;
    margin-top: 0.6rem;
    opacity: 0.7;
    color: #c8c8e0;
}}

.rm-node-duration {{
    font-family:var(--font-mono);
    font-size:0.67rem;
    letter-spacing: 0.05em;
    opacity: 0.4;
    margin-top: 0.2rem;
    color: #9898b0;
}}

/* SVG connector sits behind orbs */
.rm-svg-layer {{
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 1;
    overflow: visible;
}}

.rm-col-connector {{
    width: 100%;
    position: relative;
}}

/* Tooltip */
.rm-tooltip {{
    position: absolute;
    left: 56px;
    top: -8px;
    background: #1a1a24;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 1rem 1.1rem;
    width: 210px;
    z-index: 100;
    opacity: 0;
    transform: translateY(4px) scale(0.97);
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1);
    pointer-events: none;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}}

.rm-tooltip-step {{
    font-family:var(--font-mono);
    font-size:0.69rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.5;
    margin-bottom: 0.3rem;
    color: #e8e8f0;
}}

.rm-tooltip-title {{
    font-family:var(--font-serif);
    font-size:0.94rem;
    font-weight: 700;
    margin-bottom: 0.4rem;
}}

.rm-tooltip-body {{
    font-family:var(--font);
    font-size:0.86rem;
    color: #9898b0;
    line-height: 1.55;
    font-weight: 300;
}}

.rm-hint {{
    text-align: center;
    margin-top: 1.5rem;
    font-family:var(--font-mono);
    font-size:0.71rem;
    letter-spacing: 0.1em;
    color: #3a3a52;
    text-transform: uppercase;
}}
</style>

<div class="rm-root">
    <div class="rm-canvas" id="rm-canvas"></div>
    <div class="rm-hint">hover over orbs to see milestone details</div>
</div>

<script>
(function() {{
    const careers = {tree_json};
    const canvas = document.getElementById('rm-canvas');
    const ORB_H = 44;
    const NODE_H = 44 + 20 + 30 + 24; // orb + label + duration + gap
    const HEADER_H = 80;

    careers.forEach((career, ci) => {{
        const col = document.createElement('div');
        col.className = 'rm-col';

        // Header
        const hdr = document.createElement('div');
        hdr.className = 'rm-col-header';
        hdr.innerHTML = `
            <div class="rm-col-title" style="color:${{career.color}}">${{career.title}}</div>
            <div class="rm-col-tag">${{career.tagline}}</div>
        `;
        col.appendChild(hdr);

        // SVG layer for bezier curves between orbs
        const svg = document.createElementNS('http://www.w3.org/2000/svg','svg');
        svg.classList.add('rm-svg-layer');
        svg.setAttribute('id', `rm-svg-${{ci}}`);
        col.appendChild(svg);

        const nodeWraps = [];

        career.nodes.forEach((node, ni) => {{
            const wrap = document.createElement('div');
            wrap.className = 'rm-node-wrap';
            wrap.style.marginBottom = ni < career.nodes.length - 1 ? '2rem' : '0';

            const orbContainer = document.createElement('div');
            orbContainer.className = 'rm-orb-container';

            // Pulse rings
            const ring1 = document.createElement('div');
            ring1.className = 'rm-orb-ring';
            ring1.style.borderColor = career.color;
            ring1.style.animationDelay = `${{ni * 0.3}}s`;

            const ring2 = document.createElement('div');
            ring2.className = 'rm-orb-ring2';
            ring2.style.borderColor = career.color;
            ring2.style.animationDelay = `${{ni * 0.3 + 0.25}}s`;

            // Orb core
            const orb = document.createElement('div');
            orb.className = 'rm-orb';
            orb.style.background = `radial-gradient(circle at 35% 35%, ${{career.color}}dd, ${{career.color}}66)`;
            orb.style.boxShadow = `0 0 20px ${{career.glow}}, 0 0 6px ${{career.color}}55 inset`;
            orb.style.color = '#fff';
            orb.textContent = String(node.step).padStart(2,'0');

            // Tooltip
            const tooltip = document.createElement('div');
            tooltip.className = 'rm-tooltip';
            tooltip.style.borderColor = career.color + '33';
            tooltip.innerHTML = `
                <div class="rm-tooltip-step">Step ${{node.step}}</div>
                <div class="rm-tooltip-title" style="color:${{career.color}}">${{node.label}}</div>
                <div class="rm-tooltip-body">${{node.detail}}</div>
                ${{node.duration ? `<div style="margin-top:0.6rem;font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.08em;color:${{career.color}};opacity:0.6;">${{node.duration}}</div>` : ''}}
            `;

            orbContainer.appendChild(ring2);
            orbContainer.appendChild(ring1);
            orbContainer.appendChild(orb);
            orbContainer.appendChild(tooltip);
            wrap.appendChild(orbContainer);

            const label = document.createElement('div');
            label.className = 'rm-node-label';
            label.textContent = node.label;
            wrap.appendChild(label);

            if (node.duration) {{
                const dur = document.createElement('div');
                dur.className = 'rm-node-duration';
                dur.textContent = node.duration;
                wrap.appendChild(dur);
            }}

            col.appendChild(wrap);
            nodeWraps.push(wrap);
        }});

        canvas.appendChild(col);

        // After DOM is laid out, draw bezier connectors
        requestAnimationFrame(() => {{
            const colRect = col.getBoundingClientRect();
            const svgEl = document.getElementById(`rm-svg-${{ci}}`);
            svgEl.setAttribute('viewBox', `0 0 200 ${{col.offsetHeight}}`);
            svgEl.style.height = col.offsetHeight + 'px';

            for (let ni = 0; ni < nodeWraps.length - 1; ni++) {{
                const wrapA = nodeWraps[ni];
                const wrapB = nodeWraps[ni + 1];
                const orbA = wrapA.querySelector('.rm-orb-container');
                const orbB = wrapB.querySelector('.rm-orb-container');

                const aRect = orbA.getBoundingClientRect();
                const bRect = orbB.getBoundingClientRect();

                const x = 100; // center of 200px col
                const y1 = aRect.bottom - colRect.top - col.getBoundingClientRect().top + col.scrollTop;
                const y2 = bRect.top  - colRect.top - col.getBoundingClientRect().top + col.scrollTop;

                // Curved bezier
                const cp1y = y1 + (y2 - y1) * 0.4;
                const cp2y = y1 + (y2 - y1) * 0.6;

                const path = document.createElementNS('http://www.w3.org/2000/svg','path');
                path.setAttribute('d', `M ${{x}} ${{y1 - colRect.top + col.getBoundingClientRect().top}} C ${{x}} ${{cp1y - colRect.top + col.getBoundingClientRect().top}}, ${{x}} ${{cp2y - colRect.top + col.getBoundingClientRect().top}}, ${{x}} ${{y2 - colRect.top + col.getBoundingClientRect().top}}`);
                path.setAttribute('fill','none');
                path.setAttribute('stroke', career.color);
                path.setAttribute('stroke-width','1.5');
                path.setAttribute('stroke-opacity','0.25');
                path.setAttribute('stroke-dasharray','4 4');
                svgEl.appendChild(path);
            }}
        }});
    }});
}})();
</script>
"""

    st.components.v1.html(roadmap_html, height=680, scrolling=True)

    # ── SAVE TO SESSION ───────────────────────────────────────────────────────
    st.session_state["career_data"] = data
    st.session_state["user_name"] = name
    st.session_state["qualification"] = qualification
    st.session_state["profile"] = form_data