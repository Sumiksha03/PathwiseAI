import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os, json, time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── PAGE CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.pg-eyebrow { font-family:var(--font-mono);font-size:0.77rem;color:var(--a4);letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.5rem; }
.pg-title { font-family:var(--font-display);font-size:2.53rem;font-weight:800;color:var(--text);line-height:1.1;margin-bottom:0.4rem; }
.pg-title span { color:var(--a4); }
.pg-sub { font-size:1.03rem;color:var(--text2);font-weight:300;margin-bottom:2rem; }

/* Quiz card */
.quiz-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 2rem;
    margin-bottom: 1rem;
}
.quiz-q-num {
    font-family: var(--font-mono);
    font-size:0.71rem;
    letter-spacing: 0.15em;
    color: var(--a4);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.quiz-q-text {
    font-family: var(--font-display);
    font-size:1.21rem;
    font-weight: 600;
    color: var(--text);
    line-height: 1.4;
    margin-bottom: 1.2rem;
}

/* Trait bar */
.trait-row {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.7rem;
}
.trait-label { font-size:0.92rem;color:var(--text2);width:130px;flex-shrink:0; }
.trait-bar-bg {
    flex:1;height:6px;background:var(--bg4);border-radius:3px;overflow:hidden;
}
.trait-bar-fill { height:100%;border-radius:3px;transition:width 0.5s ease; }
.trait-pct { font-family:var(--font-mono);font-size:0.8rem;color:var(--text3);width:36px;text-align:right; }

/* Result card */
.result-card {
    background: linear-gradient(135deg, rgba(255,179,71,0.07), rgba(124,106,247,0.05));
    border: 1px solid rgba(255,179,71,0.2);
    border-radius: var(--r-lg);
    padding: 2rem;
}
.personality-type {
    font-family: var(--font-display);
    font-size:3.45rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--a4), var(--a1));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.personality-name {
    font-size:1.26rem;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 0.8rem;
}
.personality-desc {
    font-size:1.01rem;color:var(--text2);line-height:1.65;font-weight:300;
}

/* Profile field */
.field-label {
    font-family:var(--font-mono);font-size:0.75rem;letter-spacing:0.12em;
    text-transform:uppercase;color:var(--text3);margin-bottom:0.4rem;
}

/* Tab-style toggle */
.tab-toggle {
    display:flex;gap:0.5rem;margin-bottom:1.5rem;
}

.sh { font-family:var(--font-mono);font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;
      color:var(--text3);margin:1.8rem 0 1rem;display:flex;align-items:center;gap:0.8rem; }
.sh::after { content:'';flex:1;height:1px;background:var(--border); }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:2.5rem 0 1.5rem;border-bottom:1px solid var(--border);margin-bottom:2rem;">
    <div class="pg-eyebrow">02 / Profile & Quiz</div>
    <div class="pg-title">Know <span>Yourself</span> First</div>
    <div class="pg-sub">Complete your profile and take the aptitude quiz to unlock personalised career intelligence.</div>
</div>
""", unsafe_allow_html=True)

# ─── QUIZ QUESTIONS ───────────────────────────────────────────────────────────
QUIZ_QUESTIONS = [
    {
        "id": "q1",
        "text": "You're given a complex problem at work. Your first instinct is to...",
        "options": [
            ("Break it down into a step-by-step logical framework", "analytical"),
            ("Brainstorm freely and explore creative solutions", "creative"),
            ("Discuss it with others and gather different perspectives", "social"),
            ("Research how others have solved similar problems", "investigative"),
        ]
    },
    {
        "id": "q2",
        "text": "Which of these activities would you find most energising over a full week?",
        "options": [
            ("Leading a team project and delegating tasks", "leadership"),
            ("Deep-diving into data and finding hidden patterns", "analytical"),
            ("Designing something beautiful — visual, product, or experience", "creative"),
            ("Helping someone solve a personal or professional challenge", "social"),
        ]
    },
    {
        "id": "q3",
        "text": "When you learn something new, you prefer to...",
        "options": [
            ("Read documentation, books, or structured courses", "investigative"),
            ("Jump in and learn by doing — trial and error", "practical"),
            ("Watch someone demonstrate it first", "social"),
            ("Build a mental model first, then experiment", "analytical"),
        ]
    },
    {
        "id": "q4",
        "text": "Your ideal work output at the end of a great day is...",
        "options": [
            ("A working product or feature I built", "practical"),
            ("A piece of writing, design, or creative work I'm proud of", "creative"),
            ("A problem I solved that made someone's life easier", "social"),
            ("Insights or conclusions from analysis I completed", "analytical"),
        ]
    },
    {
        "id": "q5",
        "text": "When things go wrong in a project, you tend to...",
        "options": [
            ("Stay calm and systematically find the root cause", "analytical"),
            ("Rally the team and keep energy up", "leadership"),
            ("Pivot quickly and find a new creative direction", "creative"),
            ("Focus on the human impact and support those affected", "social"),
        ]
    },
    {
        "id": "q6",
        "text": "Which statement resonates most with how you see yourself?",
        "options": [
            ("I love digging into research and understanding systems deeply", "investigative"),
            ("I'm at my best when I'm building or making something tangible", "practical"),
            ("I thrive on connecting people and creating community", "social"),
            ("I have strong opinions and love persuading people with ideas", "leadership"),
        ]
    },
    {
        "id": "q7",
        "text": "Your dream work environment is...",
        "options": [
            ("Quiet, focused, with autonomy to explore ideas independently", "investigative"),
            ("Dynamic and collaborative — lots of energy and team interaction", "social"),
            ("A creative studio or lab where experimentation is encouraged", "creative"),
            ("A fast-paced environment where I can take charge and deliver results", "leadership"),
        ]
    },
    {
        "id": "q8",
        "text": "The subject of a book you'd actually read for fun is most likely...",
        "options": [
            ("How a complex technology or scientific concept works", "investigative"),
            ("Biographies of founders, leaders, or change-makers", "leadership"),
            ("Human psychology, philosophy, or social dynamics", "social"),
            ("Design, architecture, or the craft of making things", "creative"),
        ]
    },
]

TRAIT_LABELS = {
    "analytical":    ("Analytical",   "var(--a1)"),
    "creative":      ("Creative",     "var(--a3)"),
    "social":        ("Social",       "var(--a2)"),
    "investigative": ("Investigative","var(--a4)"),
    "practical":     ("Practical",    "#56cfb2"),
    "leadership":    ("Leadership",   "#c084fc"),
}

PERSONALITY_PROFILES = {
    ("analytical","investigative"): ("THE ARCHITECT","Systems thinker who builds elegant frameworks. Best in research, engineering, strategy, data science."),
    ("analytical","practical"):     ("THE ENGINEER","Logical builder who turns ideas into working systems. Best in software, product, infrastructure."),
    ("analytical","creative"):      ("THE INNOVATOR","Blends logic with imagination. Best in design thinking, product strategy, AI/ML."),
    ("analytical","leadership"):    ("THE STRATEGIST","Data-driven leader who builds winning teams. Best in management consulting, operations, finance."),
    ("creative","social"):          ("THE VISIONARY","Empathetic creator who builds for people. Best in UX/UI, marketing, content, education."),
    ("creative","investigative"):   ("THE EXPLORER","Curious mind who turns research into art. Best in media, science communication, writing."),
    ("creative","leadership"):      ("THE ENTREPRENEUR","Bold creative who leads from the front. Best in startups, creative direction, brand building."),
    ("creative","practical"):       ("THE MAKER","Hands-on creative who brings ideas to life. Best in design, product, game dev, architecture."),
    ("social","leadership"):        ("THE CATALYST","Inspires and mobilises people around a vision. Best in leadership, HR, social impact, policy."),
    ("social","investigative"):     ("THE COUNSELLOR","Deep empathy + research mindset. Best in psychology, medicine, education, social work."),
    ("social","practical"):         ("THE HELPER","Tangible impact on real people. Best in healthcare, teaching, NGO work, community building."),
    ("leadership","investigative"): ("THE PIONEER","Leads exploration into unknown territory. Best in research leadership, policy, academia."),
    ("leadership","practical"):     ("THE OPERATOR","Gets things done at scale. Best in operations, project management, entrepreneurship."),
    ("investigative","practical"):  ("THE SCIENTIST","Rigorous and precise — turns data into decisions. Best in research, medicine, law, finance."),
}

def get_personality(scores):
    sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top1 = sorted_traits[0][0]
    top2 = sorted_traits[1][0]
    key = (top1, top2)
    rev_key = (top2, top1)
    label, desc = PERSONALITY_PROFILES.get(key) or PERSONALITY_PROFILES.get(rev_key) or ("THE SEEKER","A unique blend of traits — you defy easy categorisation. Explore broadly before specialising.")
    return label, desc, top1, top2

# ─── TABS ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["◈  Aptitude Quiz", "◎  Full Profile"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — QUIZ
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    if "quiz_scores" not in st.session_state:
        st.session_state["quiz_scores"] = {t: 0 for t in TRAIT_LABELS}
    if "quiz_done" not in st.session_state:
        st.session_state["quiz_done"] = False
    if "quiz_answers" not in st.session_state:
        st.session_state["quiz_answers"] = {}

    if not st.session_state["quiz_done"]:
        st.markdown("""
        <div style="background:rgba(255,179,71,0.06);border:1px solid rgba(255,179,71,0.15);
                    border-radius:var(--r-md);padding:1rem 1.3rem;margin-bottom:1.5rem;
                    font-size:0.98rem;color:var(--text2);line-height:1.6;">
            Answer all 8 questions honestly — there are no right or wrong answers.
            Your responses reveal your natural working style and personality archetype.
        </div>
        """, unsafe_allow_html=True)

        with st.form("quiz_form"):
            for i, q in enumerate(QUIZ_QUESTIONS):
                st.markdown(f"""
                <div class="quiz-card">
                    <div class="quiz-q-num">Question {i+1} of {len(QUIZ_QUESTIONS)}</div>
                    <div class="quiz-q-text">{q['text']}</div>
                </div>
                """, unsafe_allow_html=True)

                options_text = [opt[0] for opt in q["options"]]
                choice = st.radio(
                    f"q_{q['id']}",
                    options_text,
                    key=f"radio_{q['id']}",
                    label_visibility="collapsed"
                )
                st.markdown("<br>", unsafe_allow_html=True)

            submitted = st.form_submit_button("◎  Reveal My Personality Type", use_container_width=True)
            if submitted:
                scores = {t: 0 for t in TRAIT_LABELS}
                for q in QUIZ_QUESTIONS:
                    chosen_text = st.session_state.get(f"radio_{q['id']}")
                    for opt_text, trait in q["options"]:
                        if opt_text == chosen_text:
                            scores[trait] = scores.get(trait, 0) + 1
                            break
                st.session_state["quiz_scores"] = scores
                st.session_state["quiz_done"] = True

                # Store in profile
                label, desc, t1, t2 = get_personality(scores)
                st.session_state["personality_type"] = label
                st.session_state["personality_desc"] = desc
                st.session_state["primary_trait"] = t1
                st.session_state["secondary_trait"] = t2
                st.rerun()

    else:
        scores = st.session_state["quiz_scores"]
        total = max(sum(scores.values()), 1)
        label, desc, t1, t2 = get_personality(scores)

        # Result card
        t1_name, t1_color = TRAIT_LABELS.get(t1, (t1, "var(--a1)"))
        t2_name, t2_color = TRAIT_LABELS.get(t2, (t2, "var(--a2)"))

        st.markdown(f"""
        <div class="result-card">
            <div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.18em;
                        text-transform:uppercase;color:var(--a4);margin-bottom:0.5rem;">Your Personality Archetype</div>
            <div class="personality-type">{label}</div>
            <div style="display:flex;gap:0.5rem;margin-bottom:1rem;flex-wrap:wrap;">
                <span style="background:{t1_color}18;border:1px solid {t1_color}35;color:{t1_color};
                             padding:0.25rem 0.7rem;border-radius:6px;font-size:0.92rem;
                             font-family:var(--font-mono);">Primary: {t1_name}</span>
                <span style="background:{t2_color}18;border:1px solid {t2_color}35;color:{t2_color};
                             padding:0.25rem 0.7rem;border-radius:6px;font-size:0.92rem;
                             font-family:var(--font-mono);">Secondary: {t2_name}</span>
            </div>
            <div class="personality-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

        # Trait bars
        st.markdown('<div class="sh">Trait Breakdown</div>', unsafe_allow_html=True)
        for trait, count in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            name, color = TRAIT_LABELS.get(trait, (trait, "var(--a1)"))
            pct = int((count / total) * 100)
            st.markdown(f"""
            <div class="trait-row">
                <div class="trait-label">{name}</div>
                <div class="trait-bar-bg">
                    <div class="trait-bar-fill" style="width:{pct}%;background:{color};box-shadow:0 0 6px {color}55;"></div>
                </div>
                <div class="trait-pct">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

        # AI Personalised insight
        if st.button("⭐ Get AI-Personalised Career Insight from Quiz"):
            with st.spinner("Analysing your personality profile…"):
                prompt = f"""Based on this personality quiz result:
Archetype: {label}
Primary trait: {t1_name}
Secondary trait: {t2_name}
Trait scores: {json.dumps({TRAIT_LABELS[k][0]: v for k,v in scores.items()})}

Write a personalised 3-paragraph career insight:
1. What this personality type excels at and why
2. Top 3 specific career paths that suit this exact combination
3. One key blind spot to watch out for and how to turn it into a strength

Be direct, specific, and inspiring. No generic advice."""
                r = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role":"user","content":prompt}],
                    max_tokens=500
                )
                insight = r.choices[0].message.content.strip()
                st.markdown(f"""
                <div style="background:var(--bg3);border:1px solid var(--border2);border-radius:var(--r-lg);
                            padding:1.6rem;margin-top:1rem;font-size:1.01rem;color:var(--text2);
                            line-height:1.7;font-weight:300;white-space:pre-wrap;">{insight}</div>
                """, unsafe_allow_html=True)

        if st.button("↻ Retake Quiz"):
            st.session_state["quiz_done"] = False
            st.session_state["quiz_scores"] = {t: 0 for t in TRAIT_LABELS}
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — FULL PROFILE
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div style="background:rgba(62,207,207,0.05);border:1px solid rgba(62,207,207,0.15);
                border-radius:var(--r-md);padding:1rem 1.3rem;margin-bottom:1.5rem;
                font-size:0.98rem;color:var(--text2);line-height:1.6;">
        Your profile powers the Career Analysis page. Fill it in once and all pages adapt to you.
    </div>
    """, unsafe_allow_html=True)

    qual_options = [
        "Higher Secondary (11th–12th)",
        "Undergraduate / College",
        "Postgraduate",
        "Working Professional"
    ]
    
    # Place the qualification selectbox outside the form to allow dynamic updates of form fields
    current_qual = st.session_state.get("qualification", "Higher Secondary (11th–12th)")
    qual_index = qual_options.index(current_qual) if current_qual in qual_options else 0
    p_qual = st.selectbox("Qualification Level", qual_options, index=qual_index)

    # Initialize a temporary dictionary to hold the form data
    form_data = {}

    with st.form("profile_form"):
        p_name = st.text_input("Full Name", value=st.session_state.get("user_name",""), placeholder="Your name")
        
        pc1, pc2 = st.columns(2)
        
        existing_profile = st.session_state.get("profile", {})
        
        if p_qual == "Higher Secondary (11th–12th)":
            with pc1:
                form_data["current_stream"] = st.radio("Current Stream", ["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", "Not decided yet"], index=["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", "Not decided yet"].index(existing_profile.get("current_stream", "Science (PCM)")) if existing_profile.get("current_stream") in ["Science (PCM)", "Science (PCB)", "Commerce", "Arts/Humanities", "Not decided yet"] else 0)
                form_data["subjects"] = st.multiselect("Favourite Subjects", ["Mathematics","Physics","Chemistry","Biology","Computer Science","Economics","Psychology","History","Literature","Art","Commerce","Political Science","Statistics","Geography"], default=existing_profile.get("subjects", []))
                form_data["learning_style"] = st.radio("Preferred Learning Style", ["Practical/Hands-on", "Theoretical/Reading", "Visual", "Interactive"], index=["Practical/Hands-on", "Theoretical/Reading", "Visual", "Interactive"].index(existing_profile.get("learning_style", "Practical/Hands-on")) if existing_profile.get("learning_style") in ["Practical/Hands-on", "Theoretical/Reading", "Visual", "Interactive"] else 0)
            with pc2:
                form_data["strengths"] = st.multiselect("Key Strengths", ["Logical Reasoning", "Creativity", "Communication", "Memorization", "Problem Solving", "Leadership"], default=existing_profile.get("strengths", []))
                form_data["extracurricular"] = st.multiselect("Extracurricular Interests", ["Sports", "Arts", "Coding", "Debating", "Music", "Volunteering"], default=existing_profile.get("extracurricular", []))
                form_data["career_goal"] = st.radio("Primary Goal after 12th", ["Top University", "Quick Job", "Entrepreneurship", "Govt Job", "Undecided"], index=["Top University", "Quick Job", "Entrepreneurship", "Govt Job", "Undecided"].index(existing_profile.get("career_goal", "Top University")) if existing_profile.get("career_goal") in ["Top University", "Quick Job", "Entrepreneurship", "Govt Job", "Undecided"] else 0)

        elif p_qual == "Undergraduate / College":
            with pc1:
                form_data["current_course"] = st.text_input("Current Course/Degree", value=existing_profile.get("current_course", ""), placeholder="e.g. B.Tech CSE, BBA...")
                form_data["years_remaining"] = st.radio("Years Remaining", ["3rd Year", "2nd Year", "Final Year", "Just Started"], index=["3rd Year", "2nd Year", "Final Year", "Just Started"].index(existing_profile.get("years_remaining", "3rd Year")) if existing_profile.get("years_remaining") in ["3rd Year", "2nd Year", "Final Year", "Just Started"] else 0)
                form_data["academic_perf"] = st.radio("Academic Performance", ["Excellent", "Average", "Struggling"], index=["Excellent", "Average", "Struggling"].index(existing_profile.get("academic_perf", "Average")) if existing_profile.get("academic_perf") in ["Excellent", "Average", "Struggling"] else 1)
            with pc2:
                form_data["practical_exp"] = st.multiselect("Practical Experience", ["Internships", "Projects", "Competitions", "Freelancing", "None yet"], default=existing_profile.get("practical_exp", []))
                form_data["soft_skills"] = st.multiselect("Soft Skills", ["Leadership", "Teamwork", "Problem Solving", "Public Speaking", "Writing"], default=existing_profile.get("soft_skills", []))
                form_data["ideal_setting"] = st.radio("Ideal Work Setting", ["Fast-paced/Startup", "Structured/MNC", "Remote", "Fieldwork"], index=["Fast-paced/Startup", "Structured/MNC", "Remote", "Fieldwork"].index(existing_profile.get("ideal_setting", "Structured/MNC")) if existing_profile.get("ideal_setting") in ["Fast-paced/Startup", "Structured/MNC", "Remote", "Fieldwork"] else 1)
                form_data["career_goal"] = st.radio("Career Goal", ["Corporate Job", "Startup/Founder", "Higher Studies", "Freelancing"], index=["Corporate Job", "Startup/Founder", "Higher Studies", "Freelancing"].index(existing_profile.get("career_goal", "Corporate Job")) if existing_profile.get("career_goal") in ["Corporate Job", "Startup/Founder", "Higher Studies", "Freelancing"] else 0)

        elif p_qual == "Postgraduate":
            with pc1:
                form_data["pg_specialisation"] = st.text_input("PG Specialisation", value=existing_profile.get("pg_specialisation", ""), placeholder="e.g. M.Tech AI, MBA Finance...")
                form_data["research_interest"] = st.radio("Research Interest", ["High - Want to do PhD", "Medium - Open to it", "Low - Prefer industry"], index=["High - Want to do PhD", "Medium - Open to it", "Low - Prefer industry"].index(existing_profile.get("research_interest", "Medium - Open to it")) if existing_profile.get("research_interest") in ["High - Want to do PhD", "Medium - Open to it", "Low - Prefer industry"] else 1)
                form_data["niche_skills"] = st.text_input("Key Expertise / Niche Skills", value=existing_profile.get("niche_skills", ""), placeholder="e.g. Python, Financial Modeling...")
            with pc2:
                form_data["prof_exp"] = st.text_input("Professional Experience (if any)", value=existing_profile.get("prof_exp", ""), placeholder="e.g. 2 years at Deloitte...")
                form_data["relocate"] = st.radio("Willingness to Relocate", ["Global", "Domestic", "No preference", "Will not relocate"], index=["Global", "Domestic", "No preference", "Will not relocate"].index(existing_profile.get("relocate", "No preference")) if existing_profile.get("relocate") in ["Global", "Domestic", "No preference", "Will not relocate"] else 2)
                form_data["career_obj"] = st.radio("Career Objective", ["Academia/Research", "Industry Leadership", "Specialized Consultant", "R&D"], index=["Academia/Research", "Industry Leadership", "Specialized Consultant", "R&D"].index(existing_profile.get("career_obj", "Industry Leadership")) if existing_profile.get("career_obj") in ["Academia/Research", "Industry Leadership", "Specialized Consultant", "R&D"] else 1)
                form_data["work_values"] = st.multiselect("Work Values", ["High Salary", "Work-Life Balance", "Impact/Social Good", "Innovation", "Job Security"], default=existing_profile.get("work_values", []))

        elif p_qual == "Working Professional":
            with pc1:
                form_data["current_role"] = st.text_input("Current Role", value=existing_profile.get("current_role", ""), placeholder="e.g. Software Engineer")
                form_data["years_exp"] = st.selectbox("Years of Experience", ["0–2 years", "3–5 years", "6–10 years", "10+ years"], index=["0–2 years", "3–5 years", "6–10 years", "10+ years"].index(existing_profile.get("years_exp", "0–2 years")) if existing_profile.get("years_exp") in ["0–2 years", "3–5 years", "6–10 years", "10+ years"] else 0)
                form_data["core_comp"] = st.text_input("Core Competencies / Specialized Skills", value=existing_profile.get("core_comp", ""), placeholder="e.g. Cloud Architecture, B2B Sales...")
            with pc2:
                form_data["pivot_intent"] = st.radio("Pivot Intent", ["Grow in current field", "Switch domain entirely", "Move to leadership", "Start own venture"], index=["Grow in current field", "Switch domain entirely", "Move to leadership", "Start own venture"].index(existing_profile.get("pivot_intent", "Grow in current field")) if existing_profile.get("pivot_intent") in ["Grow in current field", "Switch domain entirely", "Move to leadership", "Start own venture"] else 0)
                form_data["frustration"] = st.radio("Biggest Career Frustration", ["Lack of growth", "Low pay", "Poor work-life balance", "Boredom", "None"], index=["Lack of growth", "Low pay", "Poor work-life balance", "Boredom", "None"].index(existing_profile.get("frustration", "None")) if existing_profile.get("frustration") in ["Lack of growth", "Low pay", "Poor work-life balance", "Boredom", "None"] else 4)
                form_data["company_stage"] = st.radio("Preferred Company Stage", ["Early-stage startup", "Mid-size", "Enterprise/MNC"], index=["Early-stage startup", "Mid-size", "Enterprise/MNC"].index(existing_profile.get("company_stage", "Enterprise/MNC")) if existing_profile.get("company_stage") in ["Early-stage startup", "Mid-size", "Enterprise/MNC"] else 2)

        save_btn = st.form_submit_button("◎  Save Profile", use_container_width=True)
        if save_btn:
            st.session_state["user_name"] = p_name
            st.session_state["qualification"] = p_qual
            st.session_state["profile"] = form_data
            st.success("⭐ Profile saved! Head to Career Analysis to get your personalised report.")

    # Show saved profile
    if st.session_state.get("profile") and st.session_state.get("qualification") == p_qual:
        st.markdown('<div class="sh">Saved Profile</div>', unsafe_allow_html=True)
        prof = st.session_state["profile"]
        
        def format_val(v):
            if isinstance(v, list): return ", ".join(v) if v else "—"
            return str(v) if v else "—"
            
        items = [(k.replace("_", " ").title(), format_val(v)) for k, v in prof.items()]
        
        ic1, ic2 = st.columns(2)
        for i, (k, v) in enumerate(items):
            with (ic1 if i % 2 == 0 else ic2):
                st.markdown(f"""
                <div style="background:var(--bg2);border:1px solid var(--border);border-radius:var(--r-md);
                            padding:0.9rem 1.1rem;margin-bottom:0.5rem;">
                    <div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.12em;
                                text-transform:uppercase;color:var(--text3);margin-bottom:0.3rem;">{k}</div>
                    <div style="font-size:1.01rem;color:var(--text);">{v}</div>
                </div>
                """, unsafe_allow_html=True)