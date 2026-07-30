import streamlit as st
from rag_engine import load_index, retrieve, generate_answer
from resume_analyzer import extract_resume_text, analyze_resume
from skill_quiz import get_skills_for_role, generate_roadmap, ROLE_SKILLS

st.set_page_config(
    page_title="CareerSaathi",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

.stApp {
    background: #FBF7F0;
    background-image:
        radial-gradient(circle at 8% 10%, rgba(244,162,97,0.25) 0%, transparent 35%),
        radial-gradient(circle at 92% 15%, rgba(232,115,74,0.18) 0%, transparent 40%),
        radial-gradient(circle at 50% 90%, rgba(43,42,76,0.08) 0%, transparent 45%);
    background-attachment: fixed;
}

#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 1.8rem; max-width: 980px; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: rgba(232,115,74,0.35); border-radius: 10px; }
::-webkit-scrollbar-track { background: transparent; }

/* PAGE HEADER (small, per-page — not the big hero) */
.page-header { padding: 0.3rem 0 1.2rem 0; animation: fadeInDown 0.5s ease-out; }
.page-header h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.9rem; font-weight: 700; color: #2B2A4C; margin: 0;
}
.page-header p { color: #8a87a8; font-size: 0.95rem; margin-top: 0.3rem; }

/* WELCOME / HOME SCREEN */
.welcome-wrap { text-align: center; padding: 2.5rem 1rem 1rem 1rem; animation: fadeInDown 0.7s ease-out; }
.welcome-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(255,255,255,0.7); backdrop-filter: blur(10px);
    border: 1px solid rgba(232,115,74,0.3); color: #C85A32;
    padding: 0.4rem 1.1rem; border-radius: 999px;
    font-size: 0.78rem; font-weight: 600; letter-spacing: 0.6px;
    margin-bottom: 1.1rem; box-shadow: 0 4px 14px rgba(232,115,74,0.12);
}
.welcome-wrap h1 {
    font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 800;
    background: linear-gradient(100deg, #C85A32 10%, #2B2A4C 60%, #E8734A 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0.1rem 0; letter-spacing: -1px;
}
.welcome-wrap p.sub {
    color: #6b6889; font-size: 1.05rem; max-width: 560px;
    margin: 0.6rem auto 0 auto; line-height: 1.6;
}

/* NAV CARDS on home screen */
.nav-card-row { display: flex; gap: 1.1rem; margin: 2.2rem 0; flex-wrap: wrap; justify-content: center; }
.nav-card {
    background: rgba(255,255,255,0.78); backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.9); border-radius: 20px;
    padding: 1.6rem 1.4rem; flex: 1; min-width: 220px; text-align: left;
    box-shadow: 0 10px 30px rgba(43,42,76,0.07);
    animation: fadeInUp 0.75s ease-out; transition: all 0.25s ease;
}
.nav-card:hover { transform: translateY(-4px); box-shadow: 0 16px 34px rgba(232,115,74,0.16); }
.nav-card .icon {
    font-size: 1.5rem; width: 48px; height: 48px; display: flex;
    align-items: center; justify-content: center; margin-bottom: 0.8rem;
    background: linear-gradient(135deg, #FFE8D6, #FFD8B8); border-radius: 14px;
}
.nav-card h4 { color: #2B2A4C; margin: 0.2rem 0; font-size: 1.05rem; font-weight: 700; }
.nav-card p { color: #8a87a8; font-size: 0.87rem; margin: 0; line-height: 1.5; }

/* STAT STRIP */
.stat-row { display: flex; gap: 1rem; justify-content: center; margin: 1.8rem 0; flex-wrap: wrap; }
.stat-card {
    background: rgba(255,255,255,0.75); backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.9); border-radius: 16px;
    padding: 0.9rem 1.6rem; text-align: center; min-width: 130px;
    box-shadow: 0 8px 24px rgba(43,42,76,0.06);
}
.stat-card .num { font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #E8734A; }
.stat-card .label { font-size: 0.75rem; color: #8a87a8; margin-top: 0.2rem; font-weight: 500; }

/* CONTENT CARD (used inside every page) */
.content-card {
    background: rgba(255,255,255,0.8); backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.9); border-radius: 22px;
    padding: 1.6rem; box-shadow: 0 14px 36px rgba(43,42,76,0.07);
    margin-bottom: 1rem;
}
.empty-state { color: #a5a2c2; text-align: center; padding: 2rem 1rem; font-size: 0.95rem; line-height: 1.6; }

[data-testid="stChatMessage"] {
    animation: fadeInUp 0.4s ease-out; border-radius: 16px !important;
    box-shadow: 0 4px 14px rgba(43,42,76,0.05); margin-bottom: 0.6rem !important;
}
[data-testid="stChatMessageContent"] { font-size: 0.95rem; line-height: 1.6; }

@keyframes fadeInDown { from {opacity:0; transform:translateY(-18px);} to {opacity:1; transform:translateY(0);} }
@keyframes fadeInUp { from {opacity:0; transform:translateY(18px);} to {opacity:1; transform:translateY(0);} }

/* SIDEBAR — this is now the navbar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFF6EC 0%, #FBF7F0 100%);
    border-right: 1px solid rgba(232,115,74,0.12);
}
[data-testid="stSidebar"] * { color: #2B2A4C !important; }
.sidebar-brand {
    font-family: 'Playfair Display', serif; font-weight: 800; font-size: 1.4rem;
    padding: 0.5rem 0 0.2rem 0;
}
.sidebar-brand span { color: #E8734A; }

/* Sidebar nav radio styled as menu items */
[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.6);
    border-radius: 12px;
    padding: 0.6rem 0.8rem !important;
    margin-bottom: 0.4rem;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.9);
    border-color: rgba(232,115,74,0.25);
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(100deg, #E8734A, #F4A261);
    color: #FFFFFF !important; font-weight: 600; border-radius: 12px;
    border: none; padding: 0.6rem 1rem; width: 100%;
    box-shadow: 0 4px 14px rgba(232,115,74,0.25);
    transition: all 0.2s ease;
}
.stButton>button:hover { transform: translateY(-2px) scale(1.01); box-shadow: 0 8px 20px rgba(232,115,74,0.4); }

[data-testid="stChatInput"] {
    border-radius: 18px; border: 1px solid rgba(43,42,76,0.15) !important;
    background: rgba(255,255,255,0.9) !important; box-shadow: 0 6px 18px rgba(43,42,76,0.06);
}
[data-testid="stFileUploader"] { border-radius: 16px; }
hr { border-color: rgba(43,42,76,0.08) !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD INDEX ----------------
@st.cache_resource
def get_index():
    return load_index()

index, chunks = get_index()

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None

# ---------------- SIDEBAR NAVBAR ----------------
with st.sidebar:
    st.markdown('<div class="sidebar-brand">💼 Career<span>Saathi</span></div>', unsafe_allow_html=True)
    st.caption("AI-powered bilingual career companion")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏠 Home", "💬 Ask CareerSaathi", "📄 Resume Feedback", "🎯 Skill Gap Quiz"],
        label_visibility="collapsed",
        index=["🏠 Home", "💬 Ask CareerSaathi", "📄 Resume Feedback", "🎯 Skill Gap Quiz"].index(st.session_state.page)
    )
    st.session_state.page = page

    st.markdown("---")
    if st.session_state.page == "💬 Ask CareerSaathi":
        st.markdown("### 🎯 Popular Careers")
        example_roles = ["Data Scientist", "Software Engineer", "Product Manager", "UX Designer", "Marketing Manager", "Business Analyst"]
        for role in example_roles:
            if st.button(role, key=f"role_{role}"):
                st.session_state.pending_query = f"What skills do I need to become a {role}?"
        st.markdown("---")
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = []
            st.rerun()
        st.markdown("---")

    st.caption("Built with RAG · FAISS · Sentence-Transformers · Groq")

# ============================================================
# PAGE: HOME
# ============================================================
if st.session_state.page == "🏠 Home":
    st.markdown("""
    <div class="welcome-wrap">
        <span class="welcome-badge">🎓 AI-Powered · Retrieval-Augmented Generation</span>
        <h1>Hi, I'm CareerSaathi 👋</h1>
        <p class="sub">Your bilingual career guidance companion. Ask about any career, get resume feedback, or find your skill gaps — in English or हिंदी.</p>
    </div>
    <div class="stat-row">
        <div class="stat-card"><div class="num">1600+</div><div class="label">Q&A Entries</div></div>
        <div class="stat-card"><div class="num">50+</div><div class="label">Career Roles</div></div>
        <div class="stat-card"><div class="num">2</div><div class="label">Languages</div></div>
        <div class="stat-card"><div class="num">⚡ Instant</div><div class="label">AI Answers</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-card-row">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="icon">💬</div>
            <h4>Ask CareerSaathi</h4>
            <p>Get answers on skills, responsibilities, and growth paths for any career — English or Hindi.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start Chatting →", key="home_chat"):
            st.session_state.page = "💬 Ask CareerSaathi"
            st.rerun()
    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="icon">📄</div>
            <h4>Resume Feedback</h4>
            <p>Upload your resume and get instant, structured AI feedback tailored to your target role.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Analyze Resume →", key="home_resume"):
            st.session_state.page = "📄 Resume Feedback"
            st.rerun()
    with col3:
        st.markdown("""
        <div class="nav-card">
            <div class="icon">🎯</div>
            <h4>Skill Gap Quiz</h4>
            <p>Rate your current skills for a target role and get a personalized learning roadmap.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Take Quiz →", key="home_quiz"):
            st.session_state.page = "🎯 Skill Gap Quiz"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: CHAT
# ============================================================
elif st.session_state.page == "💬 Ask CareerSaathi":
    st.markdown("""
    <div class="page-header">
        <h2>💬 Ask CareerSaathi</h2>
        <p>Ask any career question in English or हिंदी — grounded in real data, not guesses.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown('<div class="empty-state">👋 Hi! Pick a career from the sidebar, or type your own question below.</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "💼"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    query = st.chat_input("Ask about any career — e.g. 'Product Manager बनने के लिए क्या चाहिए?'")
    if st.session_state.pending_query:
        query = st.session_state.pending_query
        st.session_state.pending_query = None

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(query)
        with st.chat_message("assistant", avatar="💼"):
            with st.spinner("Thinking..."):
                retrieved = retrieve(query, index, chunks)
                answer = generate_answer(query, retrieved)
                st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: RESUME FEEDBACK
# ============================================================
elif st.session_state.page == "📄 Resume Feedback":
    st.markdown("""
    <div class="page-header">
        <h2>📄 Resume Feedback</h2>
        <p>Upload your resume as a PDF and get instant, structured AI feedback.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    target_role = st.text_input("Target role (optional)", placeholder="e.g. Data Scientist, Frontend Developer")
    uploaded_resume = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_resume is not None:
        if st.button("🔍 Analyze Resume"):
            with st.spinner("Reading and analyzing your resume..."):
                resume_text = extract_resume_text(uploaded_resume)
                if len(resume_text.strip()) < 50:
                    st.error("Couldn't extract enough text from this PDF. Try a different file.")
                else:
                    feedback = analyze_resume(resume_text, target_role if target_role else None)
                    st.markdown("---")
                    st.markdown(feedback)

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: SKILL GAP QUIZ
# ============================================================
elif st.session_state.page == "🎯 Skill Gap Quiz":
    st.markdown("""
    <div class="page-header">
        <h2>🎯 Skill Gap Quiz</h2>
        <p>Rate your current skills and get a personalized roadmap to close the gap.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    quiz_role = st.selectbox("Target role", list(ROLE_SKILLS.keys()))
    skills_to_rate = get_skills_for_role(quiz_role)

    st.markdown("#### Rate yourself (1 = beginner, 5 = expert)")
    ratings = {}
    for skill in skills_to_rate:
        ratings[skill] = st.slider(skill, 1, 5, 3, key=f"quiz_{skill}")

    if st.button("🧭 Generate My Roadmap"):
        with st.spinner("Building your personalized roadmap..."):
            roadmap = generate_roadmap(quiz_role, ratings)
            st.markdown("---")
            st.markdown(roadmap)

    st.markdown('</div>', unsafe_allow_html=True)