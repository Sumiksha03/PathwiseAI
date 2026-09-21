import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os, random
from datetime import datetime, date

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── DATA ──────────────────────────────────────────────────────────────────────
CAREER_TIPS = [
    "Build in public — sharing your learning journey on LinkedIn attracts more opportunities than a polished resume alone.",
    "Informational interviews are underused gold. One 20-minute conversation with a professional beats 100 cold applications.",
    "Your first job matters less than your first skill. Focus on becoming genuinely good at something specific.",
    "Rejection emails are data, not verdicts. Track what you apply for and iterate like a product manager.",
    "The best time to network is before you need it. Invest in relationships when there's no ask.",
    "Side projects tell stories resumes can't. Even a small deployed project signals initiative and curiosity.",
    "Salary negotiation starts at the first call. Never anchor low — the first number said often sticks.",
    "Most career pivots happen in 18 months with consistent daily effort. Slow is smooth, smooth is fast.",
    "Specialise enough to be found, stay broad enough to adapt. The T-shaped professional wins long term.",
    "The skill that compounds fastest in any career: clear written communication. Invest in it early.",
    "Certifications matter most in the first 3 years. After that, portfolio and reputation speak louder.",
]

# ─── PAGE-LEVEL CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Hero */
.hero {
    padding: 3.5rem 2.5rem;
    border-bottom: 1.5px solid var(--border, #e0ddd8);
    margin-bottom: 2rem;
    background: linear-gradient(135deg, rgba(37,99,235,0.06) 0%, rgba(13,148,136,0.06) 100%);
    border-radius: 20px;
    box-shadow: inset 0 2px 20px rgba(255,255,255,0.5);
}
.hero-eyebrow {
    font-family: var(--font-mono, monospace);
    font-size:0.83rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--teal, #0d9488);
    margin-bottom: 0.7rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.hero-eyebrow::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--teal, #0d9488);
    display: inline-block;
}
.hero-title {
    font-family: var(--font-serif, serif);
    font-size:3.5rem;
    font-weight: 800;
    color: var(--text, #18160f);
    line-height: 1.1;
    margin-bottom: 0.8rem;
    letter-spacing: -0.02em;
    background: linear-gradient(to right, var(--text), var(--blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size:1.15rem;
    color: var(--text3, #6b6760);
    font-weight: 400;
    max-width: 520px;
    line-height: 1.6;
}

/* Stat strip */
.stat-strip {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.4);
    border-radius: 20px;
    padding: 1.6rem 2rem;
    display: flex;
    align-items: center;
    gap: 0;
    flex-wrap: wrap;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.07);
}
.stat-item {
    text-align: center;
    flex: 1;
    min-width: 90px;
    padding: 0 1rem;
}
.stat-n {
    font-family: var(--font-serif, serif);
    font-size:2.3rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.stat-l {
    font-size:0.9rem;
    color: var(--text3, #6b6760);
    font-weight: 500;
    letter-spacing: 0.02em;
}
.stat-div {
    width: 1px;
    height: 44px;
    background: var(--border, #e0ddd8);
    flex-shrink: 0;
}

/* Empty state */
.empty-state {
    background: var(--blue-bg, #eff6ff);
    border: 1.5px dashed rgba(37,99,235,0.3);
    border-radius: 14px;
    padding: 1.6rem 2rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}
.empty-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--blue, #2563eb);
    box-shadow: 0 0 10px rgba(37,99,235,0.4);
    flex-shrink: 0;
    margin-top: 4px;
}
.empty-title {
    font-size:1.12rem;
    font-weight: 600;
    color: var(--text, #18160f);
    margin-bottom: 0.25rem;
}
.empty-sub {
    font-size:1.01rem;
    color: var(--text3, #6b6760);
    line-height: 1.6;
}

/* Section label */
.slabel {
    font-family: var(--font-mono, monospace);
    font-size:0.8rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text4, #9b9790);
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2.2rem 0 1.1rem;
}
.slabel::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border, #e0ddd8);
}

/* Tip card */
.tip-card {
    background: #ffffff;
    border: 1.5px solid var(--border, #e0ddd8);
    border-left: 4px solid var(--blue, #2563eb);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.tip-eyebrow {
    font-family: var(--font-mono, monospace);
    font-size:0.78rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--blue, #2563eb);
    margin-bottom: 0.7rem;
    font-weight: 500;
}
.tip-text {
    font-size:1.17rem;
    color: var(--text, #18160f);
    line-height: 1.72;
    font-weight: 400;
}

/* Nav hub cards */
.nav-hub {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.5);
    border-radius: 16px;
    padding: 1.6rem;
    height: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    cursor: pointer;
}
.nav-hub:hover {
    border-color: var(--blue, #2563eb);
    box-shadow: 0 10px 30px rgba(37,99,235,0.1);
    transform: translateY(-4px);
}
.nav-icon {
    font-size:1.84rem;
    margin-bottom: 0.75rem;
    display: block;
    line-height: 1;
}
.nav-title {
    font-family: var(--font-serif, serif);
    font-size:1.21rem;
    font-weight: 700;
    color: var(--text, #18160f);
    margin-bottom: 0.35rem;
}
.nav-desc {
    font-size:0.98rem;
    color: var(--text3, #6b6760);
    line-height: 1.5;
}

/* Exam cards */
.exam-row {
    background: #ffffff;
    border: 1.5px solid var(--border, #e0ddd8);
    border-radius: 12px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 1.1rem;
    transition: border-color 0.15s;
}
.exam-row:hover { border-color: var(--border2, #cbc7c0); }
.exam-badge {
    font-size:0.9rem;
    font-weight: 700;
    padding: 0.3rem 0.75rem;
    border-radius: 7px;
    white-space: nowrap;
    flex-shrink: 0;
    font-family: var(--font-mono, monospace);
}
.exam-name {
    font-size:1.09rem;
    font-weight: 600;
    color: var(--text, #18160f);
}
.exam-meta {
    font-size:0.94rem;
    color: var(--text3, #6b6760);
    margin-top: 0.15rem;
}
.exam-date {
    font-family: var(--font-mono, monospace);
    font-size:0.9rem;
    color: var(--amber, #d97706);
    white-space: nowrap;
    font-weight: 500;
}
.exam-link {
    font-family: var(--font-mono, monospace);
    font-size:0.83rem;
    color: var(--text2, #3d3a33);
    text-decoration: none;
    border: 1.5px solid var(--border2, #cbc7c0);
    padding: 0.28rem 0.7rem;
    border-radius: 7px;
    white-space: nowrap;
    transition: all 0.15s;
    flex-shrink: 0;
}
.exam-link:hover {
    border-color: var(--blue, #2563eb);
    color: var(--blue, #2563eb);
}

/* Career match cards */
.match-card {
    background: #ffffff;
    border: 1.5px solid var(--border, #e0ddd8);
    border-radius: 14px;
    padding: 1.3rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    height: 100%;
}
.match-title {
    font-family: var(--font-serif, serif);
    font-size:1.15rem;
    font-weight: 700;
    color: var(--text, #18160f);
    margin-bottom: 0.25rem;
}
.match-tagline {
    font-family: var(--font-mono, monospace);
    font-size:0.8rem;
    font-weight: 500;
    margin-bottom: 0.7rem;
    letter-spacing: 0.03em;
}
.match-reason {
    font-size:1.0rem;
    color: var(--text2, #3d3a33);
    line-height: 1.6;
    font-weight: 400;
}
.badge {
    display: inline-block;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    font-size:0.84rem;
    font-family: var(--font-mono, monospace);
    font-weight: 500;
    margin-top: 0.7rem;
    margin-right: 0.4rem;
}

/* Footer */
.footer {
    margin-top: 3.5rem;
    padding-top: 1.5rem;
    border-top: 1.5px solid var(--border, #e0ddd8);
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.75rem;
}
.footer-brand {
    font-family: var(--font-serif, serif);
    font-size:1.21rem;
    font-weight: 700;
    color: var(--text, #18160f);
}
.footer-sub {
    font-family: var(--font-mono, monospace);
    font-size:0.75rem;
    color: var(--text4, #9b9790);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ─── INIT ──────────────────────────────────────────────────────────────────────
now = datetime.now()
hour = now.hour
greet = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")
user_name = st.session_state.get("user_name", "")
name_str  = f", {user_name}" if user_name else ""
date_str  = now.strftime("%A, %d %B %Y")
career_data = st.session_state.get("career_data", None)
qualification = st.session_state.get("qualification", "")
profile = st.session_state.get("profile", {})

# ─── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">Your Career Command Centre &nbsp;·&nbsp; {date_str}</div>
    <div class="hero-title">{greet}{name_str}</div>
    <div class="hero-sub">Everything you need to navigate your professional journey — powered by AI, built for you.</div>
</div>
""", unsafe_allow_html=True)

# ─── STATS / EMPTY STATE ───────────────────────────────────────────────────────
if career_data:
    careers   = career_data.get("careers", [])
    score     = career_data.get("match_score", "—")
    gap       = sum(len(c.get("skills_missing", [])) for c in careers)
    have      = sum(len(c.get("skills_present", [])) for c in careers)
    top_title = careers[0]["title"] if careers else "—"
    top_tag   = careers[0].get("tagline", "") if careers else ""
    st.markdown(f"""
    <div class="stat-strip">
        <div class="stat-item">
            <div class="stat-n" style="color:var(--blue)">{score}</div>
            <div class="stat-l">Match Score</div>
        </div>
        <div class="stat-div"></div>
        <div class="stat-item">
            <div class="stat-n" style="color:var(--teal)">{len(careers)}</div>
            <div class="stat-l">Career Matches</div>
        </div>
        <div class="stat-div"></div>
        <div class="stat-item">
            <div class="stat-n" style="color:var(--rose)">{gap}</div>
            <div class="stat-l">Skills to Build</div>
        </div>
        <div class="stat-div"></div>
        <div class="stat-item">
            <div class="stat-n" style="color:var(--amber)">{have}</div>
            <div class="stat-l">Skills You Have</div>
        </div>
        <div class="stat-div"></div>
        <div class="stat-item" style="flex:2;text-align:left;padding-left:1.5rem;">
            <div style="font-size:0.86rem;color:var(--text3);margin-bottom:0.3rem;font-weight:500;text-transform:uppercase;letter-spacing:0.06em;">Top Match</div>
            <div style="font-family:var(--font-serif);font-size:1.26rem;font-weight:700;color:var(--text);">{top_title}</div>
            <div style="font-family:var(--font-mono);font-size:0.8rem;color:var(--blue);margin-top:0.15rem;">{top_tag}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-dot"></div>
        <div>
            <div class="empty-title">No analysis yet</div>
            <div class="empty-sub">Complete <strong>Profile & Quiz</strong>, then head to <strong>Career Analysis</strong> to unlock your personalised dashboard.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── DAILY TIP ─────────────────────────────────────────────────────────────────
st.markdown('<div class="slabel">Daily Career Tip</div>', unsafe_allow_html=True)

tip_seed = int(date.today().strftime("%j")) + int(date.today().strftime("%Y"))
if "daily_tip" not in st.session_state:
    st.session_state["daily_tip"] = CAREER_TIPS[tip_seed % len(CAREER_TIPS)]

tip_col, btn_col = st.columns([6, 1])
with tip_col:
    st.markdown(f"""
    <div class="tip-card">
        <div class="tip-eyebrow">✦ Tip of the day &nbsp;·&nbsp; {date_str}</div>
        <div class="tip-text">{st.session_state['daily_tip']}</div>
    </div>
    """, unsafe_allow_html=True)

with btn_col:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↻ New tip", use_container_width=True):
        if profile.get("interests") or career_data:
            ctx = f"interests: {profile.get('interests',[])} qualification: {qualification}"
            try:
                r = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"user","content":f"Give ONE sharp, specific, actionable career tip (2-3 sentences, no fluff) for a student with {ctx}. Return only the tip text."}],
                    max_tokens=120
                )
                st.session_state["daily_tip"] = r.choices[0].message.content.strip()
            except:
                st.session_state["daily_tip"] = CAREER_TIPS[random.randint(0, len(CAREER_TIPS)-1)]
        else:
            st.session_state["daily_tip"] = CAREER_TIPS[random.randint(0, len(CAREER_TIPS)-1)]
        st.rerun()

# ─── NAVIGATION HUB ───────────────────────────────────────────────────────────
st.markdown('<div class="slabel">Quick Navigation</div>', unsafe_allow_html=True)

nav_items = [
    ("📋", "Profile & Quiz",  "Take the aptitude quiz & build your full profile",  "#fffbeb", "pages/2_profile_quiz.py"),
    ("🎯", "Career Analysis", "Get AI-matched careers with a full roadmap",         "#eff6ff", "pages/3_career_analysis.py"),
    ("🛠️", "Tools & Explore", "Heatmap, What-If, Resume Builder, Salary & more",  "#f0fdfa", "pages/4_tools_explore.py"),
    ("💬", "AI Chat",         "Chat with your AI counselor or do a mock interview", "#fdf2f8", "pages/5_ai_chat.py"),
]

n_cols = st.columns(4, gap="medium")
for col, (icon, title, desc, bg, page_path) in zip(n_cols, nav_items):
    with col:
        st.markdown(f"""
        <div class="nav-hub" style="background:{bg};">
            <span class="nav-icon">{icon}</span>
            <div class="nav-title">{title}</div>
            <div class="nav-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        # Invisible spacer so button sits flush under card
        st.markdown("<div style='margin-top:0.5rem'></div>", unsafe_allow_html=True)
        if st.button(f"Open →", key=f"nav_{title}", use_container_width=True):
            try:
                st.switch_page(page_path)
            except Exception:
                st.session_state["_nav_target"] = page_path
                st.rerun()

# ─── DYNAMIC EXAMS ENGINE ─────────────────────────────────────────────────────
st.markdown('<div class="slabel">Personalised Upcoming Exams</div>', unsafe_allow_html=True)

if not profile or not qualification:
    st.markdown("""
    <div class="empty-state" style="background:#fdf2f8;border-color:rgba(190,24,93,0.3);">
        <div class="empty-dot" style="background:var(--rose);box-shadow:0 0 10px rgba(225,29,72,0.4);"></div>
        <div>
            <div class="empty-title">Profile required for tailored exams</div>
            <div class="empty-sub">Fill out your profile to get a dynamically generated list of exams and certifications you're eligible for!</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    if "dynamic_exams" not in st.session_state:
        if st.button("✨ Discover My Exams (AI)", use_container_width=True):
            with st.spinner("Analyzing your profile for the best upcoming exams..."):
                import json
                prompt = f"""
You are an expert career counselor. Based on the following user profile, recommend 5-6 upcoming real-world examinations, entrance tests, or global certifications the user is eligible for and should consider.
User Profile:
Name: {user_name}
Qualification Level: {qualification}
Profile Details: {json.dumps(profile)}
Current Date: {date_str}

Output ONLY valid JSON in this exact format:
[
  {{
    "name": "Short Name (e.g. GRE)",
    "full_name": "Full Expanded Name",
    "category": "Domain/Category",
    "eligibility_reason": "Why this fits their profile",
    "registration_deadline": "Approximate upcoming deadline (e.g. 'Oct 2026' or 'Rolling')",
    "urgency": "Urgent" (if soon) OR "Upcoming" OR "Planning",
    "link": "Official Website URL"
  }}
]
"""
                try:
                    r = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":prompt}],
                        temperature=0.7,
                        max_tokens=1500
                    )
                    raw = r.choices[0].message.content.strip()
                    if raw.startswith("```"):
                        raw = raw.split("```")[1]
                        if raw.startswith("json"):
                            raw = raw[4:]
                    st.session_state["dynamic_exams"] = json.loads(raw.strip())
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to fetch exams: {e}")
    else:
        exams = st.session_state["dynamic_exams"]
        col1, col2 = st.columns([5,1])
        with col2:
            if st.button("↻ Refresh", use_container_width=True):
                del st.session_state["dynamic_exams"]
                st.rerun()
                
        urgency_colors = {
            "Urgent": ("#fff1f2", "#fecdd3", "#e11d48"),     # Rose
            "Upcoming": ("#fffbeb", "#fde68a", "#d97706"),   # Amber
            "Planning": ("#f0fdfa", "#ccfbf1", "#0d9488")    # Teal
        }

        for exam in exams:
            urgency = exam.get("urgency", "Planning")
            bg, border, color = urgency_colors.get(urgency, ("#f0fdfa", "#ccfbf1", "#0d9488"))
            
            st.markdown(f"""
            <div class="exam-row" style="background:rgba(255,255,255,0.6);backdrop-filter:blur(10px);">
                <div class="exam-badge" style="background:{bg};border:1.5px solid {border};color:{color};">
                    {exam.get('name', 'Exam')}
                </div>
                <div style="flex:1;min-width:0;">
                    <div class="exam-name">{exam.get('full_name', 'Full Name')}</div>
                    <div class="exam-meta"><strong>{exam.get('category', 'Category')}</strong> &nbsp;·&nbsp; {exam.get('eligibility_reason', '')}</div>
                </div>
                <div class="exam-date" style="color:{color};">{exam.get('registration_deadline', '')}</div>
                <a href="{exam.get('link', '#')}" target="_blank" class="exam-link" style="border-color:{color};color:{color};">Info ↗</a>
            </div>
            """, unsafe_allow_html=True)

# ─── CAREER SNAPSHOT ──────────────────────────────────────────────────────────
if career_data and career_data.get("careers"):
    st.markdown('<div class="slabel">Your Career Matches Snapshot</div>', unsafe_allow_html=True)
    careers = career_data["careers"]
    top_colors = ["var(--amber)", "var(--blue)", "var(--teal)"]
    mc = st.columns(3, gap="medium")
    for col, career, accent in zip(mc, careers, top_colors):
        with col:
            demand = career.get("demand", "—")
            dc = {"High":"#0d9488","Medium":"#d97706","Low":"#be185d"}.get(demand, "#6b6760")
            reason = career.get("reason","")[:130]
            st.markdown(f"""
            <div class="match-card" style="border-top:3px solid {accent};">
                <div class="match-title">{career['title']}</div>
                <div class="match-tagline" style="color:{accent};">{career.get('tagline','')}</div>
                <div class="match-reason">{reason}…</div>
                <div>
                    <span class="badge" style="background:{dc}18;border:1.5px solid {dc}40;color:{dc};">{demand} Demand</span>
                    <span class="badge" style="background:var(--bg3);border:1.5px solid var(--border);color:var(--text3);">{career.get('growth','')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div>
        <span class="footer-brand">PathWise</span>
        &nbsp;&nbsp;
        <span class="footer-sub">AI Career Guidance</span>
    </div>
    <div class="footer-sub">Powered by Groq · llama-3.3-70b · Built with Streamlit</div>
</div>
""", unsafe_allow_html=True)