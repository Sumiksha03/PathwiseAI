# PathWise — AI Career Guidance System

## Setup

1. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Get your free key at https://console.groq.com

3. **Project structure**
   ```
   pathwise/
   ├── app.py                  ← Entry point (run this)
   ├── requirements.txt
   ├── .env
   └── pages/
       ├── 1_home.py           ← Home: daily tip, exams, nav hub
       ├── 2_profile_quiz.py   ← MBTI quiz + full profile builder
       ├── 3_career_analysis.py← Core career analysis (adaptive by level)
       ├── 4_tools_explore.py  ← Heatmap, What-If, Resume Builder, Salary, Growth
       └── 5_ai_chat.py        ← AI Counselor + Mock Interview
   ```

4. **Run the app**
   ```
   streamlit run app.py
   ```

## Pages

| Page | Features |
|------|----------|
| **Home** | Daily AI tip, exam reminders (India + Global), navigation hub, career snapshot |
| **Profile & Quiz** | 8-question MBTI-style aptitude quiz, personality archetype, full profile form |
| **Career Analysis** | Top 3 AI career matches, adaptive sections by qualification level, skill gap, glowing orb roadmap |
| **Tools & Explore** | Job demand heatmap, What-If career simulator, AI resume builder, salary intelligence, growth tracker |
| **AI Chat** | Career counselor chat, mock interview with scoring |

## Notes
- All user data is stored in `st.session_state` — fills across pages automatically
- Complete Profile & Quiz first for best personalisation
- Resume builder includes `.txt` download
- Model: `llama-3.3-70b-versatile` via Groq (free tier available)