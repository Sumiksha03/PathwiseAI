import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os, json, time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── PAGE CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.pg-eyebrow{font-family:var(--font-mono);font-size:0.77rem;color:var(--a2);letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.5rem;}
.pg-title{font-family:var(--font-display);font-size:2.53rem;font-weight:800;color:var(--text);line-height:1.1;margin-bottom:0.4rem;}
.pg-title span{color:var(--a2);}
.sh{font-family:var(--font-mono);font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;
    color:var(--text3);margin:1.8rem 0 1rem;display:flex;align-items:center;gap:0.8rem;}
.sh::after{content:'';flex:1;height:1px;background:var(--border);}

/* Tool card */
.tool-card{background:var(--bg2);border:1px solid var(--border);border-radius:var(--r-lg);padding:1.8rem;margin-bottom:1.5rem;}
.tool-header{display:flex;align-items:center;gap:0.8rem;margin-bottom:1.2rem;}
.tool-icon{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.15rem;flex-shrink:0;}
.tool-title{font-family:var(--font-display);font-size:1.21rem;font-weight:700;color:var(--text);}
.tool-sub{font-size:0.9rem;color:var(--text3);margin-top:0.1rem;}

/* Heatmap cell */
.hm-cell{
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    border-radius:var(--r-md);padding:0.8rem 0.5rem;cursor:default;
    transition:transform 0.15s ease;font-size:0.92rem;text-align:center;
}
.hm-cell:hover{transform:scale(1.04);}
.hm-city{font-family:var(--font-display);font-weight:600;font-size:0.92rem;margin-bottom:0.3rem;}
.hm-score{font-family:var(--font-mono);font-size:1.26rem;font-weight:500;}
.hm-lbl{font-size:0.75rem;margin-top:0.1rem;opacity:0.7;}

/* What-if card */
.wi-scenario{background:var(--bg3);border:1px solid var(--border);border-radius:var(--r-md);padding:1.2rem;margin-bottom:0.8rem;}
.wi-path-label{font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.4rem;}
.wi-path-title{font-family:var(--font-display);font-size:1.09rem;font-weight:700;margin-bottom:0.4rem;}
.wi-path-body{font-size:0.95rem;color:var(--text2);line-height:1.6;font-weight:300;}

/* Resume */
.resume-preview{background:#fff;border-radius:var(--r-md);padding:2rem;color:#1a1a2e;font-family:var(--font-serif);
    box-shadow:0 20px 60px rgba(0,0,0,0.4);line-height:1.5;}
.resume-name{font-size:1.84rem;font-weight:700;color:#1a1a2e;margin-bottom:0.2rem;}
.resume-contact{font-size:0.9rem;color:#555;margin-bottom:1rem;font-family:var(--font);}
.resume-section{margin-top:1rem;border-top:1px solid #e0e0e0;padding-top:0.8rem;}
.resume-section-title{font-size:0.86rem;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
    color:#444;margin-bottom:0.5rem;font-family:var(--font);}
.resume-body{font-size:0.94rem;color:#333;line-height:1.6;}

/* Growth tracker */
.growth-entry{background:var(--bg3);border:1px solid var(--border);border-radius:var(--r-md);
    padding:0.9rem 1.1rem;margin-bottom:0.4rem;display:flex;align-items:center;gap:1rem;}

/* Salary bar */
.sal-row{display:flex;align-items:center;gap:0.8rem;margin-bottom:0.6rem;}
.sal-label{font-size:0.92rem;color:var(--text2);width:160px;flex-shrink:0;}
.sal-bar-bg{flex:1;height:7px;background:var(--bg4);border-radius:4px;overflow:hidden;}
.sal-bar-fill{height:100%;border-radius:4px;}
.sal-val{font-family:var(--font-mono);font-size:0.92rem;color:var(--a4);width:80px;text-align:right;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:2.5rem 0 1.5rem;border-bottom:1px solid var(--border);margin-bottom:2rem;">
    <div class="pg-eyebrow">04 / Tools & Explore</div>
    <div class="pg-title">Power <span>Tools</span> for Your Career</div>
    <div style="font-size:1.03rem;color:var(--text2);font-weight:300;">Explore, plan, and build — everything from salary insights to your AI-generated resume.</div>
</div>
""", unsafe_allow_html=True)

# Get session data
career_data   = st.session_state.get("career_data", {})
profile       = st.session_state.get("profile", {})
user_name     = st.session_state.get("user_name", "User")
qualification = st.session_state.get("qualification", "Undergraduate / College")
careers       = career_data.get("careers", []) if career_data else []
top_career    = careers[0]["title"] if careers else "Software Engineer"

tool_tabs = st.tabs(["⬡ Job Heatmap", "◎ What If?", "⭐ Resume Builder", "◈ Salary Insights", "◇ Growth Tracker"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — JOB DEMAND HEATMAP
# ════════════════════════════════════════════════════════════════════════════════
with tool_tabs[0]:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <div class="tool-icon" style="background:rgba(62,207,207,0.1);color:var(--a2);">⬡</div>
            <div>
                <div class="tool-title">Job Demand Heatmap</div>
                <div class="tool-sub">City-wise demand for any career role — India & Global</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    hm_col1, hm_col2 = st.columns([3,1])
    with hm_col1:
        hm_role = st.text_input("Enter a career/role", value=top_career, placeholder="e.g. Data Scientist, UX Designer…")
    with hm_col2:
        hm_region = st.selectbox("Region", ["India", "Global", "Both"])

    if st.button("◎  Generate Heatmap", key="hm_btn"):
        with st.spinner("Analysing job demand across cities…"):
            prompt = f"""Generate job demand data for the role: "{hm_role}" in {hm_region}.
Return ONLY valid JSON (no markdown):
{{
  "role": "{hm_role}",
  "region": "{hm_region}",
  "cities": [
    {{"city": "City Name", "country": "Country", "demand_score": 85, "demand_label": "Very High", "avg_salary": "₹18-25 LPA or $95k-130k", "top_companies": ["Co1","Co2","Co3"], "growth_trend": "↑ Growing"}},
    ... (12 cities total, mix based on region)
  ],
  "insights": "2-sentence market insight for this role"
}}
demand_score is 0-100. Include top tech hubs, emerging cities, and tier-2 surprises."""
            try:
                r = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"user","content":prompt}],
                    max_tokens=1200
                )
                raw = r.choices[0].message.content.strip()
                raw = raw.split("```")[1] if "```" in raw else raw
                raw = raw[4:].strip() if raw.startswith("json") else raw.strip()
                hm_data = json.loads(raw)
                st.session_state["heatmap_data"] = hm_data
            except Exception as e:
                st.error(f"Could not generate heatmap data. Try again. ({e})")

    if "heatmap_data" in st.session_state:
        hd = st.session_state["heatmap_data"]
        cities = hd.get("cities", [])

        if hd.get("insights"):
            st.markdown(f"""
            <div style="background:rgba(62,207,207,0.06);border:1px solid rgba(62,207,207,0.15);
                        border-radius:var(--r-md);padding:0.9rem 1.2rem;margin-bottom:1.2rem;
                        font-size:0.98rem;color:var(--text2);">{hd['insights']}</div>
            """, unsafe_allow_html=True)

        # Heatmap grid
        cols_per_row = 4
        for row_start in range(0, len(cities), cols_per_row):
            row_cities = cities[row_start:row_start+cols_per_row]
            gcols = st.columns(len(row_cities))
            for col, city in zip(gcols, row_cities):
                score = city.get("demand_score", 50)
                # Color gradient based on score
                if score >= 80:
                    bg, color = "rgba(62,207,207,0.15)", "var(--a2)"
                elif score >= 60:
                    bg, color = "rgba(124,106,247,0.12)", "var(--a1)"
                elif score >= 40:
                    bg, color = "rgba(255,179,71,0.10)", "var(--a4)"
                else:
                    bg, color = "rgba(240,98,146,0.10)", "var(--a3)"

                companies = ", ".join(city.get("top_companies",[])[:2])
                with col:
                    st.markdown(f"""
                    <div class="hm-cell" style="background:{bg};border:1px solid {color}25;"
                         title="{city.get('avg_salary','')} | {companies}">
                        <div class="hm-city" style="color:{color};">{city['city']}</div>
                        <div class="hm-score" style="color:{color};">{score}</div>
                        <div class="hm-lbl" style="color:{color};">{city.get('demand_label','')}</div>
                        <div style="font-size:0.69rem;color:var(--text3);margin-top:0.3rem;">
                            {city.get('growth_trend','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Legend
        st.markdown("""
        <div style="display:flex;gap:1.2rem;margin-top:1rem;flex-wrap:wrap;">
            <div style="display:flex;align-items:center;gap:0.4rem;font-size:0.92rem;color:var(--text3);">
                <div style="width:10px;height:10px;border-radius:2px;background:rgba(62,207,207,0.3);"></div> 80+ Very High
            </div>
            <div style="display:flex;align-items:center;gap:0.4rem;font-size:0.92rem;color:var(--text3);">
                <div style="width:10px;height:10px;border-radius:2px;background:rgba(124,106,247,0.25);"></div> 60–79 High
            </div>
            <div style="display:flex;align-items:center;gap:0.4rem;font-size:0.92rem;color:var(--text3);">
                <div style="width:10px;height:10px;border-radius:2px;background:rgba(255,179,71,0.2);"></div> 40–59 Medium
            </div>
            <div style="display:flex;align-items:center;gap:0.4rem;font-size:0.92rem;color:var(--text3);">
                <div style="width:10px;height:10px;border-radius:2px;background:rgba(240,98,146,0.2);"></div> <40 Low
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — WHAT IF EXPLORER
# ════════════════════════════════════════════════════════════════════════════════
with tool_tabs[1]:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <div class="tool-icon" style="background:rgba(124,106,247,0.1);color:var(--a1);">◎</div>
            <div>
                <div class="tool-title">"What If?" Career Explorer</div>
                <div class="tool-sub">Simulate any career path — see your 10-year diverging timeline</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    wi_col1, wi_col2 = st.columns(2)
    with wi_col1:
        wi_path_a = st.text_input("Career Path A (your current direction)", value=top_career)
    with wi_col2:
        wi_path_b = st.text_input("Career Path B (what if I chose this?)", placeholder="e.g. Product Manager, Journalist…")

    wi_context = st.text_input("Your current background (brief)", placeholder="e.g. CS student, 2nd year college, loves coding and design…",
        value=f"{qualification} | {', '.join(profile.get('subjects',[])[:3])}" if profile else "")

    if st.button("◎  Simulate Both Paths", key="wi_btn"):
        if not wi_path_b:
            st.warning("Please enter a second career path to compare.")
        else:
            with st.spinner("Simulating your diverging timelines…"):
                prompt = f"""You are a career scenario simulator. Compare two career paths for this person:
Background: {wi_context}
Path A: {wi_path_a}
Path B: {wi_path_b}

Return ONLY valid JSON:
{{
  "comparison_title": "short title",
  "path_a": {{
    "title": "{wi_path_a}",
    "year1": "What year 1 looks like",
    "year3": "What year 3 looks like",
    "year5": "What year 5 looks like",
    "year10": "What year 10 looks like",
    "salary_5yr": "Expected salary at year 5",
    "peak_role": "Role you could reach at peak",
    "lifestyle": "Work-life balance & lifestyle",
    "risk": "High/Medium/Low",
    "upside": "The big upside of this path",
    "downside": "The main challenge"
  }},
  "path_b": {{
    "title": "{wi_path_b}",
    "year1": "What year 1 looks like",
    "year3": "What year 3 looks like",
    "year5": "What year 5 looks like",
    "year10": "What year 10 looks like",
    "salary_5yr": "Expected salary at year 5",
    "peak_role": "Role you could reach at peak",
    "lifestyle": "Work-life balance & lifestyle",
    "risk": "High/Medium/Low",
    "upside": "The big upside of this path",
    "downside": "The main challenge"
  }},
  "verdict": "Honest 2-sentence verdict on which path fits this person better and why"
}}"""
                try:
                    r = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":prompt}],
                        max_tokens=1000
                    )
                    raw = r.choices[0].message.content.strip()
                    raw = raw.split("```")[1] if "```" in raw else raw
                    raw = raw[4:].strip() if raw.startswith("json") else raw.strip()
                    wi_data = json.loads(raw)
                    st.session_state["whatif_data"] = wi_data
                except Exception as e:
                    st.error(f"Could not simulate. Try again. ({e})")

    if "whatif_data" in st.session_state:
        wd = st.session_state["whatif_data"]
        a_col, b_col = st.columns(2)
        timeline_steps = [("Year 1","year1","var(--a4)"), ("Year 3","year3","var(--a2)"),
                          ("Year 5","year5","var(--a1)"), ("Year 10","year10","var(--a3)")]

        for col, path_key, accent in [(a_col,"path_a","var(--a1)"), (b_col,"path_b","var(--a2)")]:
            path = wd.get(path_key, {})
            risk = path.get("risk","Medium")
            risk_color = {"High":"var(--a3)","Medium":"var(--a4)","Low":"var(--a2)"}.get(risk,"var(--a4)")
            with col:
                st.markdown(f"""
                <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--r-lg);
                            padding:1.4rem;border-top:2px solid {accent};">
                    <div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.12em;
                                text-transform:uppercase;color:{accent};margin-bottom:0.3rem;">
                        {'Path A' if path_key=='path_a' else 'Path B'}
                    </div>
                    <div style="font-family:var(--font-display);font-size:1.26rem;font-weight:700;
                                color:var(--text);margin-bottom:1rem;">{path.get('title','')}</div>
                """, unsafe_allow_html=True)

                for label, key, dot_color in timeline_steps:
                    st.markdown(f"""
                    <div style="display:flex;gap:0.8rem;margin-bottom:0.7rem;align-items:flex-start;">
                        <div style="width:7px;height:7px;border-radius:50%;background:{dot_color};
                                    box-shadow:0 0 6px {dot_color};margin-top:5px;flex-shrink:0;"></div>
                        <div>
                            <div style="font-family:var(--font-mono);font-size:0.71rem;color:var(--text3);
                                        letter-spacing:0.1em;text-transform:uppercase;">{label}</div>
                            <div style="font-size:0.95rem;color:var(--text2);font-weight:300;
                                        line-height:1.5;margin-top:0.1rem;">{path.get(key,'')}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                    <div style="border-top:1px solid var(--border);padding-top:0.8rem;margin-top:0.5rem;">
                        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:0.6rem;">
                            <span style="background:rgba(255,179,71,0.1);border:1px solid rgba(255,179,71,0.2);
                                         color:var(--a4);padding:0.2rem 0.6rem;border-radius:5px;
                                         font-size:0.8rem;font-family:var(--font-mono);">
                                {path.get('salary_5yr','')}
                            </span>
                            <span style="background:{risk_color.replace('var(--','rgba(').replace(')',',0.1)')};
                                         border:1px solid {risk_color.replace('var(--','rgba(').replace(')',',0.25)')};
                                         color:{risk_color};padding:0.2rem 0.6rem;border-radius:5px;
                                         font-size:0.8rem;font-family:var(--font-mono);">
                                {risk} Risk
                            </span>
                        </div>
                        <div style="font-size:0.9rem;color:var(--text2);margin-bottom:0.3rem;">
                            <span style="color:var(--a2);">↑</span> {path.get('upside','')}
                        </div>
                        <div style="font-size:0.9rem;color:var(--text3);">
                            <span style="color:var(--a3);">↓</span> {path.get('downside','')}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        if wd.get("verdict"):
            st.markdown(f"""
            <div style="background:rgba(124,106,247,0.06);border:1px solid rgba(124,106,247,0.2);
                        border-radius:var(--r-md);padding:1.1rem 1.4rem;margin-top:1rem;
                        font-size:1.01rem;color:var(--text2);line-height:1.6;">
                <span style="color:var(--a1);font-family:var(--font-mono);font-size:0.75rem;
                              letter-spacing:0.1em;text-transform:uppercase;">Verdict · </span>
                {wd['verdict']}
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — RESUME BUILDER
# ════════════════════════════════════════════════════════════════════════════════
with tool_tabs[2]:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <div class="tool-icon" style="background:rgba(240,98,146,0.1);color:var(--a3);"></div>
            <div>
                <div class="tool-title">AI Resume Builder</div>
                <div class="tool-sub">Generate an industry-ready resume tailored to your target role</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    rb1, rb2 = st.columns(2)
    with rb1:
        rb_name     = st.text_input("Full Name", value=st.session_state.get("user_name",""), key="rb_name")
        rb_email    = st.text_input("Email", placeholder="you@email.com", key="rb_email")
        rb_phone    = st.text_input("Phone", placeholder="+91 98765 43210", key="rb_phone")
        rb_location = st.text_input("Location", placeholder="City, State", key="rb_loc")
        rb_linkedin = st.text_input("LinkedIn (optional)", placeholder="linkedin.com/in/yourname", key="rb_li")
        rb_github   = st.text_input("GitHub/Portfolio (optional)", placeholder="github.com/yourname", key="rb_gh")

    with rb2:
        rb_target   = st.text_input("Target Role", value=top_career, key="rb_role")
        rb_summary  = st.text_area("Brief About You", placeholder="2-3 sentences: who you are, what you're good at, what you're seeking…", height=80, key="rb_sum")
        rb_edu      = st.text_area("Education", placeholder="Degree | College | Year | GPA/percentage\ne.g. B.Tech CSE | IIT Delhi | 2024 | 8.5 CGPA", height=80, key="rb_edu")
        rb_exp      = st.text_area("Experience / Projects", placeholder="Role | Company | Duration | Key achievement\ne.g. SDE Intern | Google | May–Aug 2023 | Built recommendation engine", height=80, key="rb_exp")
        rb_skills   = st.text_input("Skills (comma-separated)", placeholder="Python, ML, React, Leadership…", key="rb_skills")
        rb_extra    = st.text_input("Certifications / Awards (optional)", placeholder="e.g. AWS Certified, Hackathon winner…", key="rb_extra")

    rb_style = st.radio("Resume Style", ["Professional & Concise", "Technical & Detailed", "Creative & Impactful"], horizontal=True)

    if st.button("  Generate Industry-Ready Resume", key="rb_btn"):
        if not rb_name or not rb_target:
            st.warning("Please enter your name and target role at minimum.")
        else:
            with st.spinner("Crafting your resume with AI…"):
                prompt = f"""You are a professional resume writer. Create an industry-ready resume for:

Name: {rb_name}
Email: {rb_email} | Phone: {rb_phone} | Location: {rb_location}
LinkedIn: {rb_linkedin} | GitHub: {rb_github}
Target Role: {rb_target}
About: {rb_summary}
Education: {rb_edu}
Experience/Projects: {rb_exp}
Skills: {rb_skills}
Certifications/Awards: {rb_extra}
Qualification Level: {qualification}
Style: {rb_style}

Return ONLY valid JSON (no markdown):
{{
  "name": "{rb_name}",
  "contact_line": "email | phone | location | linkedin | github (only include non-empty)",
  "target_role": "{rb_target}",
  "professional_summary": "Polished 3-sentence summary tailored to {rb_target}",
  "education": [
    {{"degree":"","institution":"","year":"","score":"","note":""}}
  ],
  "experience": [
    {{"role":"","company":"","duration":"","bullets":["achievement 1 with metric","achievement 2","achievement 3"]}}
  ],
  "skills": {{
    "technical": ["skill1","skill2","skill3","skill4","skill5","skill6"],
    "soft": ["skill1","skill2","skill3"]
  }},
  "projects": [
    {{"name":"","description":"one sentence","tech_stack":"","impact":""}}
  ],
  "certifications": ["cert1","cert2"],
  "keywords": ["ATS keyword 1","keyword 2","keyword 3","keyword 4","keyword 5"]
}}

Make all bullet points start with strong action verbs. Quantify achievements wherever possible. Tailor everything to the target role."""
                try:
                    r = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role":"user","content":prompt}],
                        max_tokens=1500
                    )
                    raw = r.choices[0].message.content.strip()
                    raw = raw.split("```")[1] if "```" in raw else raw
                    raw = raw[4:].strip() if raw.startswith("json") else raw.strip()
                    rb_data = json.loads(raw)
                    st.session_state["resume_data"] = rb_data
                except Exception as e:
                    st.error(f"Resume generation failed. Try again. ({e})")

    if "resume_data" in st.session_state:
        rd = st.session_state["resume_data"]
        st.markdown('<div class="sh">Your Generated Resume</div>', unsafe_allow_html=True)

        # Preview
        exp_html = ""
        for exp in rd.get("experience",[]):
            bullets = "".join([f"<li style='margin-bottom:0.2rem;'>{b}</li>" for b in exp.get("bullets",[])])
            exp_html += f"""
            <div style="margin-bottom:0.8rem;">
                <div style="display:flex;justify-content:space-between;align-items:baseline;">
                    <strong>{exp.get('role','')}</strong>
                    <span style="font-size:0.86rem;color:#666;">{exp.get('duration','')}</span>
                </div>
                <div style="font-size:0.92rem;color:#555;margin-bottom:0.3rem;">{exp.get('company','')}</div>
                <ul style="margin:0;padding-left:1.2rem;font-size:0.92rem;">{bullets}</ul>
            </div>"""

        proj_html = ""
        for proj in rd.get("projects",[]):
            proj_html += f"""
            <div style="margin-bottom:0.6rem;">
                <strong>{proj.get('name','')}</strong>
                <span style="font-size:0.86rem;color:#666;margin-left:0.5rem;">{proj.get('tech_stack','')}</span>
                <div style="font-size:0.92rem;color:#444;">{proj.get('description','')} {proj.get('impact','')}</div>
            </div>"""

        edu_html = ""
        for edu in rd.get("education",[]):
            edu_html += f"""
            <div style="margin-bottom:0.4rem;font-size:0.94rem;">
                <strong>{edu.get('degree','')}</strong> · {edu.get('institution','')}
                <span style="color:#666;"> · {edu.get('year','')} · {edu.get('score','')}</span>
            </div>"""

        tech_skills = " · ".join(rd.get("skills",{}).get("technical",[]))
        soft_skills = " · ".join(rd.get("skills",{}).get("soft",[]))
        certs = " · ".join(rd.get("certifications",[]))

        st.markdown(f"""
        <div class="resume-preview">
            <div class="resume-name">{rd.get('name','')}</div>
            <div style="font-size:0.98rem;color:#666;font-family:var(--font);margin-bottom:0.2rem;">{rd.get('target_role','')}</div>
            <div class="resume-contact">{rd.get('contact_line','')}</div>

            <div class="resume-section">
                <div class="resume-section-title">Professional Summary</div>
                <div class="resume-body">{rd.get('professional_summary','')}</div>
            </div>

            {'<div class="resume-section"><div class="resume-section-title">Experience</div><div class="resume-body">' + exp_html + '</div></div>' if rd.get('experience') else ''}

            {'<div class="resume-section"><div class="resume-section-title">Projects</div><div class="resume-body">' + proj_html + '</div></div>' if rd.get('projects') else ''}

            {'<div class="resume-section"><div class="resume-section-title">Education</div><div class="resume-body">' + edu_html + '</div></div>' if rd.get('education') else ''}

            <div class="resume-section">
                <div class="resume-section-title">Skills</div>
                <div class="resume-body">
                    <strong>Technical:</strong> {tech_skills}<br>
                    <strong>Soft Skills:</strong> {soft_skills}
                </div>
            </div>

            {'<div class="resume-section"><div class="resume-section-title">Certifications</div><div class="resume-body">' + certs + '</div></div>' if certs else ''}
        </div>
        """, unsafe_allow_html=True)

        # ATS Keywords
        keywords = rd.get("keywords",[])
        if keywords:
            kw_html = " ".join([f'<span style="background:rgba(62,207,207,0.1);border:1px solid rgba(62,207,207,0.2);color:var(--a2);padding:0.25rem 0.7rem;border-radius:6px;font-size:0.86rem;margin:0.2rem;display:inline-block;">{kw}</span>' for kw in keywords])
            st.markdown(f"""
            <div style="margin-top:1rem;">
                <div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.12em;text-transform:uppercase;
                            color:var(--text3);margin-bottom:0.5rem;">ATS Keywords Included</div>
                {kw_html}
            </div>
            """, unsafe_allow_html=True)

        # Download as text
        resume_text = f"""{rd.get('name','').upper()}
{rd.get('target_role','')}
{rd.get('contact_line','')}

PROFESSIONAL SUMMARY
{rd.get('professional_summary','')}

EDUCATION
{chr(10).join([f"{e.get('degree','')} | {e.get('institution','')} | {e.get('year','')} | {e.get('score','')}" for e in rd.get('education',[])])}

EXPERIENCE
{chr(10).join([f"{e.get('role','')} | {e.get('company','')} | {e.get('duration','')}{chr(10)}{chr(10).join(['• '+b for b in e.get('bullets',[])])}" for e in rd.get('experience',[])])}

SKILLS
Technical: {', '.join(rd.get('skills',{}).get('technical',[]))}
Soft: {', '.join(rd.get('skills',{}).get('soft',[]))}

CERTIFICATIONS
{chr(10).join(rd.get('certifications',[]))}
"""
        st.download_button("↓ Download Resume as .txt", resume_text, file_name=f"{rd.get('name','resume').replace(' ','_')}_resume.txt", mime="text/plain")

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 — SALARY INSIGHTS
# ════════════════════════════════════════════════════════════════════════════════
with tool_tabs[3]:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <div class="tool-icon" style="background:rgba(255,179,71,0.1);color:var(--a4);">◈</div>
            <div>
                <div class="tool-title">Salary Intelligence</div>
                <div class="tool-sub">Market-rate salary data by role, experience, and location</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    sal_col1, sal_col2, sal_col3 = st.columns(3)
    with sal_col1:
        sal_role = st.text_input("Role", value=top_career, key="sal_role")
    with sal_col2:
        sal_loc = st.selectbox("Market", ["India","USA","UK","Germany","Singapore","Canada","Australia"], key="sal_loc")
    with sal_col3:
        sal_yrs = st.selectbox("Experience Level", ["Fresher (0-1 yr)","Junior (2-4 yr)","Mid (5-8 yr)","Senior (9-12 yr)","Lead/Director (13+ yr)"], key="sal_exp")

    if st.button("◈  Get Salary Data", key="sal_btn"):
        with st.spinner("Fetching salary intelligence…"):
            prompt = f"""Provide detailed salary data for {sal_role} in {sal_loc} at {sal_yrs} experience.
Return ONLY valid JSON:
{{
  "role": "{sal_role}",
  "market": "{sal_loc}",
  "experience": "{sal_yrs}",
  "currency": "₹ or $ or £ etc.",
  "salary_bands": [
    {{"label":"Entry","range":"X-Y LPA/K","midpoint":X}},
    {{"label":"Median","range":"X-Y LPA/K","midpoint":X}},
    {{"label":"Top 10%","range":"X-Y LPA/K","midpoint":X}},
    {{"label":"FAANG/Top Co.","range":"X-Y LPA/K","midpoint":X}}
  ],
  "total_compensation": "Note about equity/bonuses for this role",
  "top_paying_companies": ["Co1","Co2","Co3","Co4","Co5"],
  "skills_that_pay_more": [
    {{"skill":"Skill Name","premium":"e.g. +15-20%"}}
  ],
  "negotiation_tip": "One specific negotiation insight for this role",
  "5yr_outlook": "Expected salary growth in 5 years"
}}"""
            try:
                r = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"user","content":prompt}],
                    max_tokens=800
                )
                raw = r.choices[0].message.content.strip()
                raw = raw.split("```")[1] if "```" in raw else raw
                raw = raw[4:].strip() if raw.startswith("json") else raw.strip()
                sal_data = json.loads(raw)
                st.session_state["salary_data"] = sal_data
            except Exception as e:
                st.error(f"Could not fetch salary data. ({e})")

    if "salary_data" in st.session_state:
        sd = st.session_state["salary_data"]
        bands = sd.get("salary_bands",[])
        max_mid = max([b.get("midpoint",1) for b in bands] or [1])

        st.markdown('<div class="sh">Salary Bands</div>', unsafe_allow_html=True)
        bar_colors = ["var(--a2)","var(--a1)","var(--a4)","var(--a3)"]
        for band, color in zip(bands, bar_colors):
            pct = int((band.get("midpoint",0) / max_mid) * 100)
            st.markdown(f"""
            <div class="sal-row">
                <div class="sal-label">{band.get('label','')}</div>
                <div class="sal-bar-bg">
                    <div class="sal-bar-fill" style="width:{pct}%;background:{color};box-shadow:0 0 6px {color}55;"></div>
                </div>
                <div class="sal-val">{band.get('range','')}</div>
            </div>
            """, unsafe_allow_html=True)

        sdc1, sdc2 = st.columns(2)
        with sdc1:
            companies = sd.get("top_paying_companies",[])
            co_html = "".join([f'<div style="font-size:0.94rem;color:var(--text2);padding:0.2rem 0;">· {c}</div>' for c in companies])
            st.markdown(f"""
            <div style="background:var(--bg3);border:1px solid var(--border);border-radius:var(--r-md);padding:1.1rem;">
                <div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.12em;
                            text-transform:uppercase;color:var(--text3);margin-bottom:0.6rem;">Top Paying Companies</div>
                {co_html}
            </div>
            """, unsafe_allow_html=True)

        with sdc2:
            skill_prems = sd.get("skills_that_pay_more",[])
            sp_html = "".join([f'<div style="display:flex;justify-content:space-between;font-size:0.94rem;padding:0.2rem 0;"><span style="color:var(--text2);">{s["skill"]}</span><span style="color:var(--a4);font-family:var(--font-mono);font-size:0.92rem;">{s["premium"]}</span></div>' for s in skill_prems])
            st.markdown(f"""
            <div style="background:var(--bg3);border:1px solid var(--border);border-radius:var(--r-md);padding:1.1rem;">
                <div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.12em;
                            text-transform:uppercase;color:var(--text3);margin-bottom:0.6rem;">Skills That Pay More</div>
                {sp_html}
            </div>
            """, unsafe_allow_html=True)

        if sd.get("negotiation_tip"):
            st.markdown(f"""
            <div style="background:rgba(62,207,207,0.05);border:1px solid rgba(62,207,207,0.15);
                        border-radius:var(--r-md);padding:0.9rem 1.1rem;margin-top:0.8rem;">
                <span style="color:var(--a2);font-family:var(--font-mono);font-size:0.71rem;
                              letter-spacing:0.1em;text-transform:uppercase;">Negotiation Tip · </span>
                <span style="font-size:0.98rem;color:var(--text2);">{sd['negotiation_tip']}</span>
            </div>
            """, unsafe_allow_html=True)

        if sd.get("5yr_outlook"):
            st.markdown(f"""
            <div style="background:rgba(255,179,71,0.05);border:1px solid rgba(255,179,71,0.15);
                        border-radius:var(--r-md);padding:0.9rem 1.1rem;margin-top:0.5rem;">
                <span style="color:var(--a4);font-family:var(--font-mono);font-size:0.71rem;
                              letter-spacing:0.1em;text-transform:uppercase;">5-Year Outlook · </span>
                <span style="font-size:0.98rem;color:var(--text2);">{sd['5yr_outlook']}</span>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 5 — GROWTH TRACKER
# ════════════════════════════════════════════════════════════════════════════════
with tool_tabs[4]:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-header">
            <div class="tool-icon" style="background:rgba(86,207,178,0.1);color:var(--a5);">◇</div>
            <div>
                <div class="tool-title">Growth Tracker</div>
                <div class="tool-sub">Track skills, goals, and milestones over time</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "growth_entries" not in st.session_state:
        st.session_state["growth_entries"] = []

    with st.form("growth_form"):
        gf1, gf2, gf3 = st.columns([2,2,1])
        with gf1:
            g_skill = st.text_input("Skill / Goal / Milestone", placeholder="e.g. Completed Python course, Got internship…")
        with gf2:
            g_category = st.selectbox("Category", ["Skill Learned","Certification","Project Completed","Internship/Job","Course","Achievement","Other"])
        with gf3:
            g_level = st.selectbox("Progress", ["Started","In Progress","Completed"])
        g_note = st.text_input("Note (optional)", placeholder="Brief context…")
        g_submit = st.form_submit_button("+ Add Entry", use_container_width=True)
        if g_submit and g_skill:
            from datetime import date as dt_date
            st.session_state["growth_entries"].insert(0, {
                "skill": g_skill,
                "category": g_category,
                "level": g_level,
                "note": g_note,
                "date": str(dt_date.today())
            })
            st.success("Entry added!")

    if st.session_state["growth_entries"]:
        entries = st.session_state["growth_entries"]
        # Stats
        total = len(entries)
        completed = sum(1 for e in entries if e["level"] == "Completed")
        in_prog = sum(1 for e in entries if e["level"] == "In Progress")

        sc1, sc2, sc3 = st.columns(3)
        for col, num, lbl, color in [
            (sc1, total, "Total Entries", "var(--a1)"),
            (sc2, completed, "Completed", "var(--a2)"),
            (sc3, in_prog, "In Progress", "var(--a4)"),
        ]:
            with col:
                st.markdown(f"""
                <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--r-md);
                            padding:1rem;text-align:center;">
                    <div style="font-family:var(--font-display);font-size:2.3rem;font-weight:800;
                                color:{color};">{num}</div>
                    <div style="font-size:0.86rem;color:var(--text3);margin-top:0.2rem;">{lbl}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="sh" style="margin-top:1.2rem;">Your Journey</div>', unsafe_allow_html=True)

        level_colors = {"Completed":"var(--a2)","In Progress":"var(--a4)","Started":"var(--text3)"}
        cat_icons = {"Skill Learned":"◈","Certification":"⭐","Project Completed":"◎","Internship/Job":"◇","Course":"⬡","Achievement":"★","Other":"·"}

        for entry in entries:
            lc = level_colors.get(entry["level"],"var(--text3)")
            ic = cat_icons.get(entry["category"],"·")
            st.markdown(f"""
            <div class="growth-entry">
                <div style="font-size:1.15rem;color:var(--text3);width:20px;flex-shrink:0;">{ic}</div>
                <div style="flex:1;">
                    <div style="font-size:1.01rem;color:var(--text);font-weight:500;">{entry['skill']}</div>
                    <div style="font-size:0.92rem;color:var(--text3);margin-top:0.1rem;">
                        {entry['category']}{'  ·  ' + entry['note'] if entry['note'] else ''}
                    </div>
                </div>
                <div style="display:flex;flex-direction:column;align-items:flex-end;gap:0.2rem;">
                    <div style="background:{lc.replace('var(--','rgba(').replace(')',',0.12)')};
                                border:1px solid {lc.replace('var(--','rgba(').replace(')',',0.25)')};
                                color:{lc};padding:0.15rem 0.55rem;border-radius:5px;
                                font-size:0.78rem;font-family:var(--font-mono);">{entry['level']}</div>
                    <div style="font-family:var(--font-mono);font-size:0.69rem;color:var(--text4);">{entry['date']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.button("🗑 Clear All Entries", key="clear_growth"):
            st.session_state["growth_entries"] = []
            st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:3rem;color:var(--text3);font-size:0.98rem;">
            No entries yet. Start tracking your growth above.
        </div>
        """, unsafe_allow_html=True)