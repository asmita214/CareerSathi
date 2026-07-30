import streamlit as st
from rag_engine import load_index, retrieve, generate_answer
from resume_analyzer import extract_resume_text, analyze_resume

st.set_page_config(page_title="CareerSaathi", page_icon="💼", layout="wide")

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

/* Gradient mesh background with soft blobs */
.stApp {
    background: #FBF7F0;
    background-image:
        radial-gradient(circle at 8% 10%, rgba(244,162,97,0.25) 0%, transparent 35%),
        radial-gradient(circle at 92% 15%, rgba(232,115,74,0.18) 0%, transparent 40%),
        radial-gradient(circle at 50% 90%, rgba(43,42,76,0.08) 0%, transparent 45%);
    background-attachment: fixed;
}

#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 2.2rem; max-width: 1020px; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: rgba(232,115,74,0.35); border-radius: 10px; }
::-webkit-scrollbar-track { background: transparent; }

/* HERO */
.hero { text-align: center; padding: 1.5rem 1rem 0.5rem 1rem; animation: fadeInDown 0.8s ease-out; }
.hero-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(232,115,74,0.3);
    color: #C85A32;
    padding: 0.4rem 1.1rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.6px;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 14px rgba(232,115,74,0.12);
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3.6rem;
    font-weight: 800;
    background: linear-gradient(100deg, #C85A32 10%, #2B2A4C 60%, #E8734A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0.1rem 0;
    letter-spacing: -1px;
}
.hero p {
    color: #6b6889; font-size: 1.08rem; max-width: 600px;
    margin: 0.7rem auto 0 auto; line-height: 1.6; font-weight: 400;
}

/* STAT CARDS */
.stat-row { display: flex; gap: 1rem; justify-content: center; margin: 2.2rem 0 1rem 0; flex-wrap: wrap; }
.stat-card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 18px;
    padding: 1.1rem 1.8rem;
    text-align: center;
    min-width: 140px;
    box-shadow: 0 10px 30px rgba(43,42,76,0.08);
    animation: fadeInUp 0.7s ease-out;
    transition: all 0.25s ease;
}
.stat-card:hover { transform: translateY(-5px); box-shadow: 0 16px 34px rgba(232,115,74,0.18); }
.stat-card .num { font-family: 'Playfair Display', serif; font-size: 1.75rem; font-weight: 700; color: #E8734A; }
.stat-card .label { font-size: 0.78rem; color: #8a87a8; margin-top: 0.25rem; font-weight: 500; letter-spacing: 0.3px; }

/* FEATURE CARDS */
.feature-row { display: flex; gap: 1.1rem; margin: 1.8rem 0 2.5rem 0; flex-wrap: wrap; justify-content: center; }
.feature-card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 20px;
    padding: 1.5rem;
    flex: 1;
    min-width: 230px;
    box-shadow: 0 10px 30px rgba(43,42,76,0.06);
    animation: fadeInUp 0.85s ease-out;
    transition: all 0.25s ease;
}
.feature-card:hover { transform: translateY(-4px); box-shadow: 0 14px 32px rgba(43,42,76,0.1); }
.feature-card .icon {
    font-size: 1.5rem; margin-bottom: 0.6rem;
    width: 44px; height: 44px; display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #FFE8D6, #FFD8B8);
    border-radius: 12px;
}
.feature-card h4 { color: #2B2A4C; margin: 0.3rem 0; font-size: 1.02rem; font-weight: 600; }
.feature-card p { color: #8a87a8; font-size: 0.86rem; margin: 0; line-height: 1.5; }

.section-label {
    font-family: 'Playfair Display', serif;
    color: #2B2A4C; font-weight: 700; font-size: 1.35rem;
    margin: 0.8rem 0 1rem 0.2rem;
    display: flex; align-items: center; gap: 0.5rem;
}

/* CHAT CARD */
.chat-card {
    background: rgba(255,255,255,0.8);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 24px;
    padding: 1.5rem;
    box-shadow: 0 16px 40px rgba(43,42,76,0.08);
    margin-top: 0.3rem;
}
.empty-state {
    color: #a5a2c2; text-align: center; padding: 2rem 1rem;
    font-size: 0.95rem; line-height: 1.6;
}

[data-testid="stChatMessage"] {
    animation: fadeInUp 0.4s ease-out;
    border-radius: 16px !important;
    box-shadow: 0 4px 14px rgba(43,42,76,0.05);
    margin-bottom: 0.6rem !important;
}
[data-testid="stChatMessageContent"] { font-size: 0.95rem; line-height: 1.6; }

@keyframes fadeInDown { from {opacity:0; transform:translateY(-18px);} to {opacity:1; transform:translateY(0);} }
@keyframes fadeInUp { from {opacity:0; transform:translateY(18px);} to {opacity:1; transform:translateY(0);} }

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFF6EC 0%, #FBF7F0 100%);
    border-right: 1px solid rgba(232,115,74,0.12);
}
[data-testid="stSidebar"] * { color: #2B2A4C !important; }
[data-testid="stSidebar"] h2 {
    font-family: 'Playfair Display', serif !important;
    font-weight: 700 !important;
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(100deg, #E8734A, #F4A261);
    color: #FFFFFF !important;
    font-weight: 600;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1rem;
    width: 100%;
    box-shadow: 0 4px 14px rgba(232,115,74,0.25);
    transition: all 0.2s ease;
}
.stButton>button:hover {
    transform: translateY(-2px) scale(1.01);
    box-shadow: 0 8px 20px rgba(232,115,74,0.4);
}

[data-testid="stChatInput"] {
    border-radius: 18px;
    border: 1px solid rgba(43,42,76,0.15) !important;
    background: rgba(255,255,255,0.9) !important;
    box-shadow: 0 6px 18px rgba(43,42,76,0.06);
}

[data-testid="stFileUploader"] {
    border-radius: 16px;
}

[data-baseweb="tab-list"] {
    gap: 0.5rem;
}
[data-baseweb="tab"] {
    background: rgba(255,255,255,0.6);
    border-radius: 12px 12px 0 0;
    font-weight: 600;
    color: #2B2A4C;
}

hr { border-color: rgba(43,42,76,0.08) !important; }
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <span class="hero-badge">🎓 AI-Powered · Retrieval-Augmented Generation</span>
    <h1>💼 CareerSaathi</h1>
    <p>Your bilingual career guidance companion. Ask about any career — skills, salary, growth path, responsibilities — in English or हिंदी.</p>
</div>
<div class="stat-row">
    <div class="stat-card"><div class="num">1600+</div><div class="label">Q&A Entries</div></div>
    <div class="stat-card"><div class="num">50+</div><div class="label">Career Roles</div></div>
    <div class="stat-card"><div class="num">2</div><div class="label">Languages</div></div>
    <div class="stat-card"><div class="num">⚡ Instant</div><div class="label">AI Answers</div></div>
</div>
<div class="feature-row">
    <div class="feature-card">
        <div class="icon">🎯</div>
        <h4>Role-Specific Guidance</h4>
        <p>Skills, qualifications, and growth paths tailored to the exact career you ask about.</p>
    </div>
    <div class="feature-card">
        <div class="icon">🌐</div>
        <h4>Truly Bilingual</h4>
        <p>Ask in English or हिंदी — CareerSaathi understands and replies in the same language.</p>
    </div>
    <div class="feature-card">
        <div class="icon">📄</div>
        <h4>Resume Feedback</h4>
        <p>Upload your resume and get instant AI-generated feedback tailored to your target role.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------- LOAD INDEX ----------------
@st.cache_resource
def get_index():
    return load_index()

index, chunks = get_index()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 💼 CareerSaathi")
    st.markdown("---")
    st.markdown("### 🎯 Popular Careers")
    example_roles = ["Data Scientist", "Software Engineer", "Product Manager", "UX Designer", "Marketing Manager", "Business Analyst"]
    selected_example = None
    for role in example_roles:
        if st.button(role, key=f"role_{role}"):
            selected_example = f"What skills do I need to become a {role}?"

    st.markdown("---")
    st.markdown("### 🌐 Language Support")
    st.markdown("Ask in **English** or **हिंदी** — CareerSaathi understands and replies in both.")

    st.markdown("---")
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.caption("Built with RAG · FAISS · Sentence-Transformers · Groq")

# ---------------- STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["💬 Ask CareerSaathi", "📄 Resume Feedback"])

# ---------------- TAB 1: CHAT ----------------
with tab1:
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown('<div class="empty-state">👋 Start by picking a career from the sidebar, or type your own question below.</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "💼"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    query = st.chat_input("Ask about any career — e.g. 'Product Manager बनने के लिए क्या चाहिए?'")
    if selected_example:
        query = selected_example

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

# ---------------- TAB 2: RESUME FEEDBACK ----------------
with tab2:
    st.markdown('<div class="chat-card">', unsafe_allow_html=True)
    st.markdown("Upload your resume as a PDF and get instant, AI-generated feedback.")

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