import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os, json, time, random

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─── PAGE CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.pg-eyebrow{font-family:var(--font-mono);font-size:0.77rem;color:var(--a3);letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.5rem;}
.pg-title{font-family:var(--font-display);font-size:2.53rem;font-weight:800;color:var(--text);line-height:1.1;margin-bottom:0.4rem;}
.pg-title span{color:var(--a3);}
.sh{font-family:var(--font-mono);font-size:0.72rem;letter-spacing:0.18em;text-transform:uppercase;
    color:var(--text3);margin:1.8rem 0 1rem;display:flex;align-items:center;gap:0.8rem;}
.sh::after{content:'';flex:1;height:1px;background:var(--border);}

/* Chat bubble */
.chat-bubble {
    max-width: 82%;
    padding: 0.9rem 1.1rem;
    border-radius: var(--r-lg);
    font-size:1.01rem;
    line-height: 1.65;
    margin-bottom: 0.6rem;
    font-weight: 300;
}
.chat-user {
    background: rgba(124,106,247,0.12);
    border: 1px solid rgba(124,106,247,0.22);
    color: var(--text);
    margin-left: auto;
    border-bottom-right-radius: 4px;
}
.chat-ai {
    background: var(--bg2);
    border: 1px solid var(--border);
    color: var(--text);
    margin-right: auto;
    border-bottom-left-radius: 4px;
}
.chat-meta {
    font-family: var(--font-mono);
    font-size:0.69rem;
    letter-spacing: 0.08em;
    margin-bottom: 0.25rem;
}
.chat-user-meta { text-align:right; color:var(--a1); }
.chat-ai-meta { color:var(--a3); }

.chat-container {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--r-xl);
    padding: 1.5rem;
    height: 420px;
    overflow-y: auto;
    margin-bottom: 1rem;
}

/* Mode toggle */
.mode-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 1.4rem;
    cursor: pointer;
    transition: all 0.2s ease;
}
.mode-card.active {
    border-color: var(--a3);
    background: rgba(240,98,146,0.06);
}
.mode-card:hover { border-color: var(--border2); }
.mode-icon { font-size:1.84rem;margin-bottom:0.5rem; }
.mode-title { font-family:var(--font-display);font-size:1.06rem;font-weight:700;color:var(--text); }
.mode-desc { font-size:0.86rem;color:var(--text3);margin-top:0.2rem;line-height:1.5; }

/* Score card */
.score-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: var(--r-lg);
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.score-num {
    font-family: var(--font-display);
    font-size:3.45rem;
    font-weight: 800;
    line-height: 1;
}
.feedback-item {
    background: var(--bg3);
    border-radius: var(--r-md);
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    font-size:0.95rem;
    color: var(--text2);
    line-height: 1.5;
    border-left: 2px solid;
}

/* Quick prompt chip */
.qp-chip {
    display:inline-block;
    background:var(--bg3);
    border:1px solid var(--border2);
    border-radius:20px;
    padding:0.3rem 0.9rem;
    font-size:0.9rem;
    color:var(--text2);
    cursor:pointer;
    margin:0.2rem;
    transition:all 0.15s ease;
}
.qp-chip:hover { border-color:var(--a3);color:var(--a3); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:2.5rem 0 1.5rem;border-bottom:1px solid var(--border);margin-bottom:2rem;">
    <div class="pg-eyebrow">05 / AI Chat</div>
    <div class="pg-title">Your AI Career <span>Counselor</span></div>
    <div style="font-size:1.03rem;color:var(--text2);font-weight:300;">
        Talk through anything career-related — or put yourself through a mock interview.
    </div>
</div>
""", unsafe_allow_html=True)

# ─── SESSION DATA ─────────────────────────────────────────────────────────────
user_name     = st.session_state.get("user_name","")
qualification = st.session_state.get("qualification","Undergraduate / College")
profile       = st.session_state.get("profile",{})
career_data   = st.session_state.get("career_data",{})
careers       = career_data.get("careers",[]) if career_data else []
top_career    = careers[0]["title"] if careers else "Software Engineer"
personality   = st.session_state.get("personality_type","")

# ─── SYSTEM PROMPTS ───────────────────────────────────────────────────────────
def counselor_system():
    ctx_parts = []
    if user_name:      ctx_parts.append(f"Name: {user_name}")
    if qualification:  ctx_parts.append(f"Level: {qualification}")
    if profile.get("interests"):  ctx_parts.append(f"Interests: {', '.join(profile['interests'])}")
    if profile.get("strengths"):  ctx_parts.append(f"Strengths: {', '.join(profile['strengths'])}")
    if personality:    ctx_parts.append(f"Personality type: {personality}")
    if careers:        ctx_parts.append(f"Top career match: {careers[0]['title']}")

    ctx = "\n".join(ctx_parts) if ctx_parts else "Profile not yet filled."
    return f"""You are PathWise, an expert AI career counselor. You are warm, direct, and deeply knowledgeable.

User profile:
{ctx}

Guidelines:
- Address the user by first name when you know it
- Be specific and actionable — no vague advice
- Reference their profile context naturally when relevant
- Keep responses focused: 2-4 paragraphs max unless asked for more
- When giving career advice, personalise it to their level and interests
- Be encouraging but honest — don't sugarcoat challenges
- Use concrete examples, resources, and numbers where possible"""

def interviewer_system(role, difficulty):
    return f"""You are a professional interviewer conducting a mock interview for the role: {role}.
Difficulty: {difficulty}

Rules:
- Start with a brief warm welcome and ask the first question
- Ask ONE question at a time
- After each answer, give 2-3 sentences of specific feedback (what was good, what to improve)
- Then ask the NEXT question naturally
- Ask a mix of: behavioural (STAR), technical/conceptual, situational, and career motivation questions
- After 5-6 questions, give a comprehensive score out of 10 with detailed feedback in this JSON format:
  FINAL_EVALUATION:{{
    "score": X,
    "overall": "2-sentence overall assessment",
    "strengths": ["strength 1","strength 2","strength 3"],
    "improvements": ["area 1","area 2","area 3"],
    "recommendation": "Hire / Strong Hire / No Hire / Needs More Practice",
    "next_steps": "What to work on before a real interview"
  }}:END_EVALUATION"""

# ─── MODE SELECTION ───────────────────────────────────────────────────────────
if "chat_mode" not in st.session_state:
    st.session_state["chat_mode"] = "counselor"

mode_col1, mode_col2 = st.columns(2)
with mode_col1:
    is_active = st.session_state["chat_mode"] == "counselor"
    st.markdown(f"""
    <div class="mode-card {'active' if is_active else ''}" id="mc1">
        <div class="mode-icon" style="color:var(--a3);">◇</div>
        <div class="mode-title">Career Counselor</div>
        <div class="mode-desc">Ask anything about careers, studies, skills, pivots, interviews, or your personalised analysis.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Switch to Counselor" if not is_active else " Active — Counselor Mode", key="mode_c"):
        st.session_state["chat_mode"] = "counselor"
        st.session_state.pop("chat_history", None)
        st.rerun()

with mode_col2:
    is_active2 = st.session_state["chat_mode"] == "interview"
    st.markdown(f"""
    <div class="mode-card {'active' if is_active2 else ''}" id="mc2">
        <div class="mode-icon" style="color:var(--a1);">◈</div>
        <div class="mode-title">Mock Interview</div>
        <div class="mode-desc">Practice role-specific interviews with real-time AI feedback and a final performance score.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Switch to Mock Interview" if not is_active2 else " Active — Interview Mode", key="mode_i"):
        st.session_state["chat_mode"] = "interview"
        st.session_state.pop("chat_history", None)
        st.session_state.pop("interview_started", None)
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# COUNSELOR MODE
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state["chat_mode"] == "counselor":
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Quick prompts
    quick_prompts = [
        f"What should I focus on for {top_career}?",
        "How do I build a strong portfolio?",
        "How do I negotiate my first salary?",
        "What certifications are worth doing?",
        "How do I switch careers without starting over?",
        f"What's the day-to-day life of a {top_career}?",
    ]

    st.markdown('<div class="sh">Quick Questions</div>', unsafe_allow_html=True)
    qp_html = "".join([f'<span class="qp-chip" onclick="document.dispatchEvent(new CustomEvent(\'qp\', {{detail:\'{q}\'}}))">{q}</span>' for q in quick_prompts])
    st.markdown(f'<div>{qp_html}</div>', unsafe_allow_html=True)

    # Chat display
    st.markdown('<div class="sh">Conversation</div>', unsafe_allow_html=True)
    chat_html = '<div class="chat-container" id="chat-box">'

    if not st.session_state["chat_history"]:
        name_bit = f" {user_name.split()[0]}" if user_name else ""
        career_bit = f" I can see your top match is <strong>{top_career}</strong> — happy to go deeper on that, or we can discuss anything else on your mind." if top_career else ""
        chat_html += f"""
        <div>
            <div class="chat-meta chat-ai-meta">◇ PathWise AI · Career Counselor</div>
            <div class="chat-bubble chat-ai">
                Hey{name_bit}! I'm your PathWise AI career counselor.{career_bit}
                What's on your mind — career direction, skill gaps, internships, salary negotiation, or anything else?
            </div>
        </div>"""

    for msg in st.session_state["chat_history"]:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            chat_html += f"""
            <div style="display:flex;flex-direction:column;align-items:flex-end;">
                <div class="chat-meta chat-user-meta">You</div>
                <div class="chat-bubble chat-user">{content}</div>
            </div>"""
        else:
            chat_html += f"""
            <div>
                <div class="chat-meta chat-ai-meta">◇ PathWise AI</div>
                <div class="chat-bubble chat-ai">{content.replace(chr(10),'<br>')}</div>
            </div>"""

    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("", placeholder="Ask anything about your career…", label_visibility="collapsed")
        send = st.form_submit_button("Send →", use_container_width=False)

    if send and user_input.strip():
        st.session_state["chat_history"].append({"role":"user","content":user_input})
        messages = [{"role":"system","content":counselor_system()}]
        for msg in st.session_state["chat_history"]:
            messages.append({"role":msg["role"],"content":msg["content"]})
        with st.spinner("Thinking…"):
            r = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                max_tokens=600,
                temperature=0.75
            )
            reply = r.choices[0].message.content.strip()
        st.session_state["chat_history"].append({"role":"assistant","content":reply})
        st.rerun()

    if st.session_state["chat_history"]:
        cc1, cc2 = st.columns([4,1])
        with cc2:
            if st.button("Clear Chat", key="clear_chat"):
                st.session_state["chat_history"] = []
                st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# MOCK INTERVIEW MODE
# ════════════════════════════════════════════════════════════════════════════════
else:
    if "interview_started" not in st.session_state or not st.session_state["interview_started"]:
        st.markdown("""
        <div style="background:rgba(124,106,247,0.06);border:1px solid rgba(124,106,247,0.15);
                    border-radius:var(--r-lg);padding:1.5rem 1.8rem;margin-bottom:1.5rem;">
            <div style="font-family:var(--font-display);font-size:1.15rem;font-weight:700;
                        color:var(--text);margin-bottom:0.5rem;">How Mock Interview Works</div>
            <div style="font-size:0.98rem;color:var(--text2);line-height:1.6;">
                The AI will conduct a realistic interview with 5–6 questions.<br>
                After each answer you'll get instant feedback.<br>
                At the end, you'll receive a score out of 10 with detailed evaluation.
            </div>
        </div>
        """, unsafe_allow_html=True)

        ic1, ic2 = st.columns(2)
        with ic1:
            iv_role = st.text_input("Role to Interview For", value=top_career, key="iv_role")
            iv_company_type = st.selectbox("Company Type", ["Startup","MNC / Large Corp","FAANG / Top Tech","Consulting Firm","Government / PSU","Any"])
        with ic2:
            iv_difficulty = st.radio("Difficulty", ["Beginner-friendly","Standard","Hard — Senior Level"], key="iv_diff")
            iv_focus = st.multiselect("Focus Areas", ["Behavioural (STAR)","Technical","Case Study","HR & Motivation","Leadership","Culture Fit"], default=["Behavioural (STAR)","Technical","HR & Motivation"])

        if st.button("◈  Start Mock Interview", key="start_iv"):
            st.session_state["interview_role"] = iv_role
            st.session_state["interview_difficulty"] = iv_difficulty
            st.session_state["interview_company"] = iv_company_type
            st.session_state["interview_focus"] = iv_focus
            st.session_state["interview_started"] = True
            st.session_state["iv_history"] = []
            st.session_state["iv_evaluation"] = None

            # Kick off with first question
            sys_prompt = interviewer_system(iv_role, iv_difficulty)
            kick = f"Start the interview for {iv_role} at a {iv_company_type}. Focus on: {', '.join(iv_focus)}. Begin with a warm welcome and your first question."
            with st.spinner("Preparing your interview…"):
                r = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role":"system","content":sys_prompt},
                        {"role":"user","content":kick}
                    ],
                    max_tokens=400
                )
                opening = r.choices[0].message.content.strip()
            st.session_state["iv_history"] = [{"role":"assistant","content":opening}]
            st.rerun()

    else:
        # ── INTERVIEW IN PROGRESS ─────────────────────────────────────────────
        role = st.session_state.get("interview_role", top_career)
        difficulty = st.session_state.get("interview_difficulty","Standard")
        evaluation = st.session_state.get("iv_evaluation")

        # Header bar
        st.markdown(f"""
        <div style="background:rgba(124,106,247,0.08);border:1px solid rgba(124,106,247,0.2);
                    border-radius:var(--r-md);padding:0.8rem 1.2rem;margin-bottom:1rem;
                    display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">
            <div style="width:8px;height:8px;border-radius:50%;background:var(--a3);
                        box-shadow:0 0 8px var(--a3);animation:pulse 1.5s ease-in-out infinite;"></div>
            <div style="font-family:var(--font-mono);font-size:0.8rem;color:var(--text2);">
                Mock Interview · <span style="color:var(--a1);">{role}</span> · {difficulty}
            </div>
            <div style="margin-left:auto;font-family:var(--font-mono);font-size:0.75rem;color:var(--text3);">
                {len([m for m in st.session_state['iv_history'] if m['role']=='user'])} answers given
            </div>
        </div>
        <style>@keyframes pulse{{ 0%,100%{{opacity:1}} 50%{{opacity:0.4}} }}</style>
        """, unsafe_allow_html=True)

        # Chat display
        chat_html = '<div class="chat-container">'
        for msg in st.session_state["iv_history"]:
            role_label = msg["role"]
            content = msg["content"]
            if role_label == "user":
                chat_html += f"""
                <div style="display:flex;flex-direction:column;align-items:flex-end;">
                    <div class="chat-meta chat-user-meta">You</div>
                    <div class="chat-bubble chat-user">{content}</div>
                </div>"""
            else:
                chat_html += f"""
                <div>
                    <div class="chat-meta chat-ai-meta">◈ Interviewer</div>
                    <div class="chat-bubble chat-ai">{content.replace(chr(10),'<br>')}</div>
                </div>"""
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        # Final evaluation display
        if evaluation:
            score = evaluation.get("score", 0)
            score_color = "var(--a2)" if score >= 7 else ("var(--a4)" if score >= 5 else "var(--a3)")
            rec_colors = {
                "Strong Hire":"var(--a2)","Hire":"var(--a2)","Needs More Practice":"var(--a4)","No Hire":"var(--a3)"
            }
            rec = evaluation.get("recommendation","Needs More Practice")
            rec_color = rec_colors.get(rec,"var(--a4)")

            st.markdown(f"""
            <div class="score-card">
                <div style="display:flex;align-items:center;gap:2rem;flex-wrap:wrap;margin-bottom:1.2rem;">
                    <div>
                        <div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.15em;
                                    text-transform:uppercase;color:var(--text3);margin-bottom:0.3rem;">Interview Score</div>
                        <div class="score-num" style="color:{score_color};">{score}<span style="font-size:1.38rem;opacity:0.4;">/10</span></div>
                    </div>
                    <div>
                        <div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.15em;
                                    text-transform:uppercase;color:var(--text3);margin-bottom:0.3rem;">Recommendation</div>
                        <div style="background:{rec_color.replace('var(--','rgba(').replace(')',',0.12)')};
                                    border:1px solid {rec_color.replace('var(--','rgba(').replace(')',',0.25)')};
                                    color:{rec_color};padding:0.35rem 1rem;border-radius:8px;
                                    font-family:var(--font-display);font-size:1.03rem;font-weight:700;">{rec}</div>
                    </div>
                    <div style="flex:1;min-width:200px;">
                        <div style="font-size:0.98rem;color:var(--text2);font-weight:300;line-height:1.6;">
                            {evaluation.get('overall','')}
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            ev1, ev2 = st.columns(2)
            with ev1:
                strengths = evaluation.get("strengths",[])
                s_html = "".join([f'<div class="feedback-item" style="border-color:var(--a2);">✓ {s}</div>' for s in strengths])
                st.markdown(f'<div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--text3);margin-bottom:0.5rem;">Strengths</div>{s_html}', unsafe_allow_html=True)
            with ev2:
                improvements = evaluation.get("improvements",[])
                i_html = "".join([f'<div class="feedback-item" style="border-color:var(--a4);">→ {i}</div>' for i in improvements])
                st.markdown(f'<div style="font-family:var(--font-mono);font-size:0.71rem;letter-spacing:0.12em;text-transform:uppercase;color:var(--text3);margin-bottom:0.5rem;">Areas to Improve</div>{i_html}', unsafe_allow_html=True)

            if evaluation.get("next_steps"):
                st.markdown(f"""
                <div style="background:rgba(62,207,207,0.06);border:1px solid rgba(62,207,207,0.15);
                            border-radius:var(--r-md);padding:0.9rem 1.1rem;margin-top:0.8rem;">
                    <span style="color:var(--a2);font-family:var(--font-mono);font-size:0.71rem;
                                  letter-spacing:0.1em;text-transform:uppercase;">Next Steps · </span>
                    <span style="font-size:0.98rem;color:var(--text2);">{evaluation['next_steps']}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            if st.button("↻ New Interview", key="new_iv"):
                st.session_state["interview_started"] = False
                st.session_state.pop("iv_history", None)
                st.session_state.pop("iv_evaluation", None)
                st.rerun()

        elif len([m for m in st.session_state["iv_history"] if m["role"]=="user"]) < 7:
            with st.form("iv_form", clear_on_submit=True):
                iv_input = st.text_area("", placeholder="Type your answer here…", height=100, label_visibility="collapsed")
                iv_send = st.form_submit_button("Submit Answer →", use_container_width=False)

            if iv_send and iv_input.strip():
                st.session_state["iv_history"].append({"role":"user","content":iv_input})

                messages = [{"role":"system","content":interviewer_system(role, difficulty)}]
                for msg in st.session_state["iv_history"]:
                    messages.append({"role":msg["role"],"content":msg["content"]})

                with st.spinner("Evaluating your answer…"):
                    r = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        max_tokens=600
                    )
                    reply = r.choices[0].message.content.strip()

                st.session_state["iv_history"].append({"role":"assistant","content":reply})

                # Check for final evaluation
                if "FINAL_EVALUATION:" in reply:
                    try:
                        eval_raw = reply.split("FINAL_EVALUATION:")[1].split(":END_EVALUATION")[0].strip()
                        evaluation_data = json.loads(eval_raw)
                        st.session_state["iv_evaluation"] = evaluation_data
                    except:
                        pass

                st.rerun()

            ic1, ic2 = st.columns([4,1])
            with ic2:
                if st.button("End & Evaluate", key="end_iv"):
                    messages = [{"role":"system","content":interviewer_system(role, difficulty)}]
                    for msg in st.session_state["iv_history"]:
                        messages.append({"role":msg["role"],"content":msg["content"]})
                    messages.append({"role":"user","content":"Please end the interview now and give me the final evaluation."})
                    with st.spinner("Generating your evaluation…"):
                        r = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=messages,
                            max_tokens=700
                        )
                        final = r.choices[0].message.content.strip()
                    st.session_state["iv_history"].append({"role":"assistant","content":final})
                    if "FINAL_EVALUATION:" in final:
                        try:
                            eval_raw = final.split("FINAL_EVALUATION:")[1].split(":END_EVALUATION")[0].strip()
                            evaluation_data = json.loads(eval_raw)
                            st.session_state["iv_evaluation"] = evaluation_data
                        except:
                            pass
                    st.rerun()
        else:
            # Auto-request final evaluation
            if not st.session_state.get("iv_evaluation"):
                messages = [{"role":"system","content":interviewer_system(role, difficulty)}]
                for msg in st.session_state["iv_history"]:
                    messages.append({"role":msg["role"],"content":msg["content"]})
                messages.append({"role":"user","content":"Please give the final evaluation now."})
                with st.spinner("Generating final evaluation…"):
                    r = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        max_tokens=700
                    )
                    final = r.choices[0].message.content.strip()
                st.session_state["iv_history"].append({"role":"assistant","content":final})
                if "FINAL_EVALUATION:" in final:
                    try:
                        eval_raw = final.split("FINAL_EVALUATION:")[1].split(":END_EVALUATION")[0].strip()
                        evaluation_data = json.loads(eval_raw)
                        st.session_state["iv_evaluation"] = evaluation_data
                    except:
                        pass
                st.rerun()

        if not evaluation:
            if st.button("✕ Abandon Interview", key="abandon_iv"):
                st.session_state["interview_started"] = False
                st.session_state.pop("iv_history", None)
                st.session_state.pop("iv_evaluation", None)
                st.rerun()