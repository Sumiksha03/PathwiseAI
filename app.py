import streamlit as st

st.set_page_config(
    page_title="PathWise · AI Career Guidance",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ═══════════════════════════════════════════
   DESIGN TOKENS
═══════════════════════════════════════════ */
:root {
  --bg:      #fafafa;
  --bg2:     #ffffff;
  --bg3:     #f4f4f5;
  --bg4:     #e4e4e7;

  --border:  #e4e4e7;
  --border2: #d4d4d8;

  --text:    #09090b;
  --text2:   #27272a;
  --text3:   #52525b;
  --text4:   #a1a1aa;

  --blue:    #4f46e5;
  --teal:    #0ea5e9;
  --rose:    #e11d48;
  --amber:   #f59e0b;
  --violet:  #8b5cf6;

  --blue-bg:   #eef2ff;
  --teal-bg:   #f0f9ff;
  --rose-bg:   #fff1f2;
  --amber-bg:  #fffbeb;
  --violet-bg: #f5f3ff;

  --shadow:  0 4px 20px rgba(0, 0, 0, 0.05), 0 1px 3px rgba(0,0,0,0.03);
  --shadow2: 0 10px 40px rgba(0, 0, 0, 0.08), 0 2px 6px rgba(0,0,0,0.04);

  --font:       'Inter', system-ui, sans-serif;
  --font-serif: 'Outfit', sans-serif;
  --font-mono:  'JetBrains Mono', monospace;

  --r:  12px;
  --r2: 16px;
  --r3: 24px;
}

* { box-sizing: border-box; }

/* ═══════════════════════════════════════════
   HIDE STREAMLIT CHROME
═══════════════════════════════════════════ */
#MainMenu, footer { display: none !important; }
# header[data-testid="stHeader"] { display: none !important; }

/* ═══════════════════════════════════════════
   APP + MAIN BACKGROUND
═══════════════════════════════════════════ */
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--bg) !important;
    font-family: var(--font) !important;
    color: var(--text) !important;
}

.main .block-container {
    background: var(--bg) !important;
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1100px !important;
}

/* Hide native sidebar toggle button as we moved to top navigation */
[data-testid="collapsedControl"] { display: none !important; }

/* ═══════════════════════════════════════════
   TYPOGRAPHY SCALE
═══════════════════════════════════════════ */
[data-testid="stMarkdownContainer"] p {
    font-size:1.21rem !important;
    color: var(--text2) !important;
    line-height: 1.75 !important;
}

[data-testid="stMarkdownContainer"] h1 {
    font-family: var(--font-serif) !important;
    font-size:2.99rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
    line-height: 1.15 !important;
    margin-bottom: 0.8rem !important;
    letter-spacing: -0.03em !important;
}

[data-testid="stMarkdownContainer"] h2 {
    font-family: var(--font-serif) !important;
    font-size:2.07rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
    margin-bottom: 0.6rem !important;
    letter-spacing: -0.02em !important;
}

[data-testid="stMarkdownContainer"] h3 {
    font-size:1.44rem !important;
    font-weight: 600 !important;
    color: var(--text) !important;
}

[data-testid="stMarkdownContainer"] li {
    font-size:1.21rem !important;
    color: var(--text2) !important;
    line-height: 1.75 !important;
}

[data-testid="stMarkdownContainer"] strong {
    color: var(--text) !important;
    font-weight: 600 !important;
}

[data-testid="stMarkdownContainer"] code {
    font-family: var(--font-mono) !important;
    background: var(--bg3) !important;
    color: var(--violet) !important;
    padding: 0.15em 0.4em !important;
    border-radius: 4px !important;
    font-size: 0.88em !important;
}

/* ═══════════════════════════════════════════
   BUTTONS — PREMIUM THEME
═══════════════════════════════════════════ */

div.stButton > button {
    background: linear-gradient(135deg, var(--blue), #6366f1) !important;
    color: #ffffff !important;
    font-family: var(--font-serif) !important;
    font-size:1.15rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;

    border: none !important;
    border-radius: var(--r) !important;
    padding: 0.6rem 1.6rem !important;
    min-height: 48px !important;

    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
    cursor: pointer !important;
}

/* HOVER */
div.stButton > button:hover {
    background: linear-gradient(135deg, #4338ca, #4f46e5) !important;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
    transform: translateY(-2px) !important;
}

/* CLICK */
div.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3) !important;
}

/* FORM SUBMIT BUTTONS ALSO MATCH */
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--blue), #6366f1) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: var(--r) !important;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
    font-family: var(--font-serif) !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.4) !important;
}

/* ═══════════════════════════════════════════
   INPUTS
═══════════════════════════════════════════ */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    border: 1.5px solid var(--border2) !important;
    color: var(--text) !important;
    border-radius: var(--r) !important;
    font-family: var(--font) !important;
    font-size:1.09rem !important;
    padding: 0.55rem 0.85rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    outline: none !important;
}

div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stNumberInput"] label {
    color: var(--text2) !important;
    font-size:1.0rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.25rem !important;
    display: block !important;
}

/* ═══════════════════════════════════════════
   SELECT / MULTISELECT
═══════════════════════════════════════════ */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div {
    background: #ffffff !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: var(--r) !important;
    color: var(--text) !important;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label {
    color: var(--text2) !important;
    font-size:1.0rem !important;
    font-weight: 500 !important;
}

span[data-baseweb="tag"] {
    background: var(--blue-bg) !important;
    border: 1px solid rgba(37,99,235,0.25) !important;
    color: var(--blue) !important;
    border-radius: 6px !important;
    font-size:0.95rem !important;
}

/* ═══════════════════════════════════════════
   RADIO
═══════════════════════════════════════════ */
div[data-testid="stRadio"] > label {
    color: var(--text2) !important;
    font-size:1.0rem !important;
    font-weight: 500 !important;
    display: block !important;
    margin-bottom: 0.4rem !important;
}

div[data-testid="stRadio"] label {
    color: var(--text2) !important;
    font-size:1.07rem !important;
}

div[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p {
    font-size:1.07rem !important;
    color: var(--text2) !important;
}

/* ═══════════════════════════════════════════
   PROGRESS BAR
═══════════════════════════════════════════ */
.stProgress > div {
    background: var(--bg4) !important;
    border-radius: 10px !important;
    height: 7px !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, var(--blue), var(--teal)) !important;
    border-radius: 10px !important;
}

/* ═══════════════════════════════════════════
   EXPANDER
═══════════════════════════════════════════ */
div[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r2) !important;
    box-shadow: var(--shadow) !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] summary {
    color: var(--text) !important;
    font-weight: 600 !important;
    font-size:1.09rem !important;
    padding: 0.85rem 1rem !important;
}
div[data-testid="stExpander"] div[data-testid="stMarkdownContainer"] p {
    color: var(--text2) !important;
    font-size:1.07rem !important;
}

/* ═══════════════════════════════════════════
   TABS
═══════════════════════════════════════════ */
div[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: var(--bg3) !important;
    border-radius: var(--r) !important;
    padding: 4px !important;
    gap: 2px !important;
    border-bottom: none !important;
}
div[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text3) !important;
    font-family: var(--font) !important;
    font-weight: 500 !important;
    font-size:1.03rem !important;
    border-radius: var(--r) !important;
    border: none !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.15s !important;
}
div[data-testid="stTabs"] [aria-selected="true"] {
    background: #ffffff !important;
    color: var(--text) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow) !important;
}

/* ═══════════════════════════════════════════
   METRIC
═══════════════════════════════════════════ */
div[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r2) !important;
    padding: 1.2rem 1.4rem !important;
    box-shadow: var(--shadow) !important;
}
div[data-testid="stMetric"] label {
    color: var(--text3) !important;
    font-size:0.9rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-family: var(--font-serif) !important;
    font-size:2.07rem !important;
}

/* ═══════════════════════════════════════════
   ALERTS
═══════════════════════════════════════════ */
div[data-testid="stAlert"] {
    border-radius: var(--r2) !important;
    font-size:1.06rem !important;
}

/* ═══════════════════════════════════════════
   CHAT
═══════════════════════════════════════════ */
[data-testid="stChatInput"],
[data-testid="stChatInputContainer"] {
    background: #ffffff !important;
    border: 1.5px solid var(--border2) !important;
    border-radius: var(--r2) !important;
    box-shadow: var(--shadow2) !important;
    margin-top: 0.5rem !important;
}
[data-testid="stChatInput"] textarea {
    font-family: var(--font) !important;
    font-size:1.09rem !important;
    color: var(--text) !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text4) !important;
}
[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r2) !important;
    padding: 1rem 1.2rem !important;
    margin-bottom: 0.75rem !important;
    box-shadow: var(--shadow) !important;
}
[data-testid="stChatMessage"] p {
    color: var(--text2) !important;
    font-size:1.09rem !important;
    line-height: 1.7 !important;
}
/* Prevent massive gap before chat input */
[data-testid="stMain"] .block-container {
    padding-bottom: 0.5rem !important;
}

/* ═══════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 10px; }

/* ═══════════════════════════════════════════
   SPINNER
═══════════════════════════════════════════ */
.stSpinner > div { border-top-color: var(--blue) !important; }

/* ═══════════════════════════════════════════
   HR
═══════════════════════════════════════════ */
hr { border-color: var(--border) !important; margin: 1.5rem 0 !important; }

/* ═══════════════════════════════════════════
   SIDEBAR FORM LABELS
═══════════════════════════════════════════ */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stTextInput label,
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] .stTextArea label {
    color: var(--text3) !important;
    font-size:0.86rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
}

/* ═══════════════════════════════════════════
   COLUMN GAPS
═══════════════════════════════════════════ */
[data-testid="stHorizontalBlock"] {
    gap: 1rem !important;
    align-items: stretch !important;
}
</style>
""", unsafe_allow_html=True)

# ─── NAVIGATION ───────────────────────────────────────────────────────────────
pages = [
    st.Page("pages/1_home.py",            title="Home",            icon="🏠"),
    st.Page("pages/2_profile_quiz.py",    title="Profile & Quiz",  icon="📋"),
    st.Page("pages/3_career_analysis.py", title="Career Analysis", icon="🎯"),
    st.Page("pages/4_tools_explore.py",   title="Tools & Explore", icon="🛠️"),
    st.Page("pages/5_ai_chat.py",         title="AI Chat",         icon="💬"),
]

# Add the newly generated custom logo to the top navigation
st.logo("assets/pathwise_logo.png")

# Store page objects in session for switch_page compatibility
_page_map = {p.url_path: p for p in pages}

# Handle nav_target set by home page buttons
if "_nav_target" in st.session_state:
    target = st.session_state.pop("_nav_target")
    try:
        st.switch_page(target)
    except Exception:
        pass

pg = st.navigation(pages, position="top")
pg.run()