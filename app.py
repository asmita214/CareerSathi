import re
import streamlit as st
import plotly.graph_objects as go
from analytics import dataset_stats, role_embedding_similarity, ats_match_score
from skill_quiz import ROLE_SKILLS
from rag_engine import load_index, retrieve, generate_answer
from resume_analyzer import extract_resume_text, analyze_resume
from skill_quiz import get_skills_for_role, generate_roadmap, ROLE_SKILLS
from career_compare import compare_careers
from career_roadmap import generate_roadmap_stages, parse_roadmap
from interview_prep import generate_interview_questions
from learning_resources import generate_learning_resources
from career_quiz import INTEREST_QUESTIONS, recommend_careers
from salary_data import SALARY_DATA, NOTE as SALARY_NOTE

st.set_page_config(page_title="CareerSaathi", page_icon="💼", layout="wide", initial_sidebar_state="expanded")

# ============================================================
# CSS (same theme: cream/ivory + navy + orange, glassmorphism)
# ============================================================
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
.block-container { padding-top: 1.6rem; max-width: 1020px; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: rgba(232,115,74,0.35); border-radius: 10px; }
::-webkit-scrollbar-track { background: transparent; }

.page-header { padding: 0.3rem 0 1.2rem 0; animation: fadeInDown 0.5s ease-out; }
.page-header h2 { font-family: 'Playfair Display', serif; font-size: 1.85rem; font-weight: 700; color: #2B2A4C; margin: 0; }
.page-header p { color: #8a87a8; font-size: 0.93rem; margin-top: 0.3rem; }

.welcome-wrap { text-align: center; padding: 2rem 1rem 0.5rem 1rem; animation: fadeInDown 0.7s ease-out; }
.welcome-badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(255,255,255,0.7); backdrop-filter: blur(10px);
    border: 1px solid rgba(232,115,74,0.3); color: #C85A32;
    padding: 0.4rem 1.1rem; border-radius: 999px;
    font-size: 0.76rem; font-weight: 600; letter-spacing: 0.6px;
    margin-bottom: 1rem; box-shadow: 0 4px 14px rgba(232,115,74,0.12);
}
.welcome-wrap h1 {
    font-family: 'Playfair Display', serif; font-size: 2.7rem; font-weight: 800;
    background: linear-gradient(100deg, #C85A32 10%, #2B2A4C 60%, #E8734A 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0.1rem 0; letter-spacing: -1px;
}
.welcome-wrap p.sub { color: #6b6889; font-size: 1.0rem; max-width: 580px; margin: 0.5rem auto 0 auto; line-height: 1.6; }

.stat-row { display: flex; gap: 0.9rem; justify-content: center; margin: 1.6rem 0; flex-wrap: wrap; }
.stat-card {
    background: rgba(255,255,255,0.75); backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.9); border-radius: 16px;
    padding: 0.8rem 1.4rem; text-align: center; min-width: 120px;
    box-shadow: 0 8px 24px rgba(43,42,76,0.06);
}
.stat-card .num { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 700; color: #E8734A; }
.stat-card .label { font-size: 0.72rem; color: #8a87a8; margin-top: 0.15rem; font-weight: 500; }

.section-label {
    font-family: 'Playfair Display', serif; color: #2B2A4C; font-weight: 700;
    font-size: 1.05rem; margin: 1.6rem 0 0.7rem 0.2rem;
}

.nav-card-row { display: flex; gap: 1rem; margin: 0.8rem 0; flex-wrap: wrap; }
.nav-card {
    background: rgba(255,255,255,0.78); backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.9); border-radius: 18px;
    padding: 1.3rem 1.2rem; flex: 1; min-width: 200px; text-align: left;
    box-shadow: 0 8px 24px rgba(43,42,76,0.06);
    animation: fadeInUp 0.6s ease-out; transition: all 0.25s ease;
}
.nav-card:hover { transform: translateY(-4px); box-shadow: 0 14px 30px rgba(232,115,74,0.15); }
.nav-card .icon {
    font-size: 1.3rem; width: 42px; height: 42px; display: flex;
    align-items: center; justify-content: center; margin-bottom: 0.6rem;
    background: linear-gradient(135deg, #FFE8D6, #FFD8B8); border-radius: 12px;
}
.nav-card h4 { color: #2B2A4C; margin: 0.15rem 0; font-size: 0.98rem; font-weight: 700; }
.nav-card p { color: #8a87a8; font-size: 0.82rem; margin: 0; line-height: 1.45; }

.content-card {
    background: rgba(255,255,255,0.8); backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.9); border-radius: 22px;
    padding: 1.5rem; box-shadow: 0 14px 36px rgba(43,42,76,0.07);
    margin-bottom: 1rem;
}
.empty-state { color: #a5a2c2; text-align: center; padding: 2rem 1rem; font-size: 0.95rem; line-height: 1.6; }

[data-testid="stChatMessage"] {
    animation: fadeInUp 0.4s ease-out; border-radius: 16px !important;
    box-shadow: 0 4px 14px rgba(43,42,76,0.05); margin-bottom: 0.6rem !important;
}

@keyframes fadeInDown { from {opacity:0; transform:translateY(-18px);} to {opacity:1; transform:translateY(0);} }
@keyframes fadeInUp { from {opacity:0; transform:translateY(18px);} to {opacity:1; transform:translateY(0);} }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFF6EC 0%, #FBF7F0 100%);
    border-right: 1px solid rgba(232,115,74,0.12);
}
[data-testid="stSidebar"] * { color: #2B2A4C !important; }
.sidebar-brand { font-family: 'Playfair Display', serif; font-weight: 800; font-size: 1.35rem; padding: 0.3rem 0 0 0; }
.sidebar-brand span { color: #E8734A; }
.sidebar-section-label {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase;
    color: #A88C7D !important; margin: 1rem 0 0.3rem 0.1rem;
}

[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: rgba(255,255,255,0.6); border-radius: 10px;
    padding: 0.45rem 0.7rem !important; margin-bottom: 0.25rem;
    transition: all 0.2s ease; border: 1px solid transparent; font-size: 0.88rem;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.9); border-color: rgba(232,115,74,0.25);
}

.stButton>button {
    background: linear-gradient(100deg, #E8734A, #F4A261);
    color: #FFFFFF !important; font-weight: 600; border-radius: 12px;
    border: none; padding: 0.55rem 1rem; width: 100%;
    box-shadow: 0 4px 14px rgba(232,115,74,0.25); transition: all 0.2s ease;
}
.stButton>button:hover { transform: translateY(-2px) scale(1.01); box-shadow: 0 8px 20px rgba(232,115,74,0.4); }

[data-testid="stChatInput"] {
    border-radius: 18px; border: 1px solid rgba(43,42,76,0.15) !important;
    background: rgba(255,255,255,0.9) !important; box-shadow: 0 6px 18px rgba(43,42,76,0.06);
}
[data-testid="stFileUploader"] { border-radius: 16px; }
hr { border-color: rgba(43,42,76,0.08) !important; }

/* Timeline for Career Roadmap */
.timeline-stage {
    border-left: 4px solid var(--stage-color, #E8734A);
    padding: 0.2rem 0 0.2rem 1.2rem; margin-bottom: 1.4rem; position: relative;
}
.timeline-stage::before {
    content: ''; position: absolute; left: -9px; top: 4px;
    width: 14px; height: 14px; border-radius: 50%; background: var(--stage-color, #E8734A);
}
.timeline-stage h4 { color: #2B2A4C; margin: 0 0 0.3rem 0; font-size: 1rem; }
.timeline-stage p { color: #6b6889; font-size: 0.88rem; margin: 0.2rem 0; }
.skill-chip {
    display: inline-block; background: rgba(232,115,74,0.1); color: #C85A32;
    padding: 0.15rem 0.6rem; border-radius: 999px; font-size: 0.76rem;
    margin: 0.15rem 0.25rem 0 0; font-weight: 500;
}

/* Score badge */
.score-badge {
    display: inline-block; padding: 0.3rem 0.9rem; border-radius: 999px;
    font-weight: 700; font-size: 0.95rem; color: white;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD INDEX
# ============================================================
@st.cache_resource
def get_index():
    return load_index()

index, chunks = get_index()
ALL_ROLES = sorted(set(c["role"] for c in chunks))

# ============================================================
# NAVIGATION MAP (grouped)
# ============================================================
NAV_GROUPS = {
    "🧭 Guidance": ["💬 Ask CareerSaathi", "⚖️ Compare Careers", "🗺️ Career Roadmap"],
    "📝 Self-Assessment": ["📄 Resume Feedback", "🎯 Skill Gap Quiz", "🧠 Career Interest Quiz", "✅ ATS Resume Match"],
    "📚 Resources": ["🎤 Interview Prep", "📖 Learning Resources", "💰 Salary Insights"],
    "📊 Data": ["📊 Dataset Insights", "🕸️ Role Similarity Map"],
    "ℹ️ Info": ["ℹ️ About CareerSaathi"],
}
ALL_PAGES = ["🏠 Home"] + [p for g in NAV_GROUPS.values() for p in g]

def page_group(page):
    for g, pages in NAV_GROUPS.items():
        if page in pages:
            return g
    return None

# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "messages": [], "page": "🏠 Home", "pending_query": None,
    "quiz_step": 0, "quiz_answers": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# SIDEBAR NAVBAR (grouped)
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-brand">💼 Career<span>Saathi</span></div>', unsafe_allow_html=True)
    st.caption("Your complete AI career guidance platform")
    st.markdown("---")

    if st.button("🏠 Home", key="nav_home"):
        st.session_state.page = "🏠 Home"
        st.rerun()

    for group_name, pages in NAV_GROUPS.items():
        st.markdown(f'<div class="sidebar-section-label">{group_name}</div>', unsafe_allow_html=True)
        current_in_group = st.session_state.page if st.session_state.page in pages else None
        selected = st.radio(
            group_name, pages, key=f"radio_{group_name}",
            label_visibility="collapsed",
            index=pages.index(current_in_group) if current_in_group else 0
        ) if current_in_group else None
        # Only treat as navigation if user actually clicks a radio within this group while it's active
        if current_in_group and selected != current_in_group:
            st.session_state.page = selected
            st.rerun()
        elif not current_in_group:
            # render inactive (collapsed look) group as plain buttons to avoid multiple active radios
            for p in pages:
                if st.button(p, key=f"btn_{p}"):
                    st.session_state.page = p
                    st.rerun()

    st.markdown("---")
    if st.session_state.page == "💬 Ask CareerSaathi":
        st.markdown('<div class="sidebar-section-label">Quick Ask</div>', unsafe_allow_html=True)
        for role in ["Data Scientist", "Software Engineer", "Product Manager", "UX Designer", "Marketing Manager"]:
            if st.button(role, key=f"quick_{role}"):
                st.session_state.pending_query = f"What skills do I need to become a {role}?"
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
        <p class="sub">Your complete bilingual career guidance platform — chat, compare careers, check your resume, assess your skills, and plan your path. In English or हिंदी.</p>
    </div>
    <div class="stat-row">
        <div class="stat-card"><div class="num">1600+</div><div class="label">Q&A Entries</div></div>
        <div class="stat-card"><div class="num">50+</div><div class="label">Career Roles</div></div>
        <div class="stat-card"><div class="num">10</div><div class="label">Tools</div></div>
        <div class="stat-card"><div class="num">2</div><div class="label">Languages</div></div>
    </div>
    """, unsafe_allow_html=True)

    card_defs = {
        "🧭 Guidance": [
            ("💬", "Ask CareerSaathi", "Get grounded answers on skills & growth paths.", "💬 Ask CareerSaathi"),
            ("⚖️", "Compare Careers", "Weigh two roles side-by-side.", "⚖️ Compare Careers"),
            ("🗺️", "Career Roadmap", "See your stage-by-stage growth path.", "🗺️ Career Roadmap"),
        ],
        "📝 Self-Assessment": [
            ("📄", "Resume Feedback", "AI-reviewed strengths & gaps.", "📄 Resume Feedback"),
            ("🎯", "Skill Gap Quiz", "Rate yourself, get a roadmap.", "🎯 Skill Gap Quiz"),
            ("🧠", "Interest Quiz", "Find careers that fit your interests.", "🧠 Career Interest Quiz"),
            ("✅", "ATS Resume Match", "Algorithmic keyword match score.", "✅ ATS Resume Match"),
        ],
        "📚 Resources": [
            ("🎤", "Interview Prep", "Common questions, answered well.", "🎤 Interview Prep"),
            ("📖", "Learning Resources", "Where to learn, free or paid.", "📖 Learning Resources"),
            ("💰", "Salary Insights", "Typical pay by role & level.", "💰 Salary Insights"),
        ],
        "📊 Data & Analysis": [
            ("📊", "Dataset Insights", "Real stats from the dataset itself.", "📊 Dataset Insights"),
            ("🕸️", "Role Similarity Map", "Which careers are most alike.", "🕸️ Role Similarity Map"),
        ],
    }

    for group, cards in card_defs.items():
        st.markdown(f'<div class="section-label">{group}</div>', unsafe_allow_html=True)
        cols = st.columns(len(cards))
        for col, (icon, title, desc, target) in zip(cols, cards):
            with col:
                st.markdown(f"""
                <div class="nav-card">
                    <div class="icon">{icon}</div>
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Open →", key=f"home_{target}"):
                    st.session_state.page = target
                    st.rerun()

# ============================================================
# PAGE: CHAT (with source citations + download)
# ============================================================
elif st.session_state.page == "💬 Ask CareerSaathi":
    st.markdown("""<div class="page-header"><h2>💬 Ask CareerSaathi</h2>
    <p>Ask any career question in English or हिंदी — grounded in real data.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown('<div class="empty-state">👋 Pick a career from the sidebar, or type your own question below.</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "💼"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                st.caption(f"📚 Sources: {', '.join(msg['sources'])}")

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
                sources = sorted(set(c["role"] for c in retrieved))
                st.markdown(answer)
                st.caption(f"📚 Sources: {', '.join(sources)}")
        st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

    if st.session_state.messages:
        chat_text = "\n\n".join([f"{'You' if m['role']=='user' else 'CareerSaathi'}: {m['content']}" for m in st.session_state.messages])
        st.download_button("⬇️ Download Conversation", chat_text, file_name="careersaathi_chat.txt")

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: COMPARE CAREERS
# ============================================================
elif st.session_state.page == "⚖️ Compare Careers":
    st.markdown("""<div class="page-header"><h2>⚖️ Compare Careers</h2>
    <p>Weighing two options? Get a grounded, side-by-side comparison.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        role1 = st.selectbox("First career", ALL_ROLES, index=0)
    with col2:
        role2 = st.selectbox("Second career", ALL_ROLES, index=min(1, len(ALL_ROLES)-1))

    if st.button("⚖️ Compare These Careers"):
        if role1 == role2:
            st.warning("Please select two different careers.")
        else:
            with st.spinner("Comparing careers..."):
                result = compare_careers(role1, role2, index, chunks, retrieve)
                st.markdown("---")
                st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)



# ============================================================
# PAGE: CAREER ROADMAP (visual timeline)
# ============================================================
elif st.session_state.page == "🗺️ Career Roadmap":
    st.markdown("""<div class="page-header"><h2>🗺️ Career Roadmap</h2>
    <p>See a stage-by-stage path for any career, from entry-level to senior.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    role = st.selectbox("Choose a career", ALL_ROLES)

    if st.button("🗺️ Generate Roadmap"):
        with st.spinner("Building roadmap..."):
            raw = generate_roadmap_stages(role)
            stages = parse_roadmap(raw)
            colors = ["#4CAF9D", "#E8734A", "#7B61FF"]
            for stage, color in zip(stages, colors):
                skills_html = "".join([f'<span class="skill-chip">{s.strip()}</span>' for s in stage["skills"].split(",") if s.strip()])
                st.markdown(f"""
                <div class="timeline-stage" style="--stage-color:{color}">
                    <h4>{stage['title']}</h4>
                    <p>{stage['focus']}</p>
                    <div>{skills_html}</div>
                </div>
                """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
elif st.session_state.page == "📊 Dataset Insights":
    st.markdown("""<div class="page-header"><h2>📊 Dataset Insights</h2>
    <p>Real statistics computed directly from the underlying dataset — no AI involved.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    role_counts, word_counter = dataset_stats(chunks)

    st.markdown("#### Entries per Career Role")
    top_roles = role_counts.most_common(15)
    fig1 = go.Figure(go.Bar(
        x=[c for _, c in top_roles], y=[r for r, _ in top_roles], orientation="h",
        marker_color="#E8734A"
    ))
    fig1.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10),
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("#### Most Frequently Mentioned Skills/Terms (across all answers)")
    top_words = word_counter.most_common(20)
    fig2 = go.Figure(go.Bar(
        x=[w for w, _ in top_words], y=[c for _, c in top_words],
        marker_color="#2B2A4C"
    ))
    fig2.update_layout(height=350, margin=dict(l=10, r=10, t=10, b=10),
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "🕸️ Role Similarity Map":
    st.markdown("""<div class="page-header"><h2>🕸️ Role Similarity Map</h2>
    <p>Which careers are most similar, based on the embedding model's own understanding.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    with st.spinner("Computing role similarities from stored embeddings..."):
        roles, sim_matrix = role_embedding_similarity(index, chunks)

    fig = go.Figure(go.Heatmap(
        z=sim_matrix, x=roles, y=roles,
        colorscale=[[0, "#FFF3E4"], [0.5, "#F4A261"], [1, "#2B2A4C"]],
        colorbar=dict(title="Similarity")
    ))
    fig.update_layout(height=650, margin=dict(l=10, r=10, t=10, b=10),
                       plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Computed by reconstructing each role's stored FAISS vectors and averaging them into a centroid, then measuring cosine similarity between centroids — no extra API calls.")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "✅ ATS Resume Match":
    st.markdown("""<div class="page-header"><h2>✅ ATS Resume Match</h2>
    <p>Algorithmic keyword match against a target role — like real Applicant Tracking Systems use.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    role = st.selectbox("Target role", ALL_ROLES, key="ats_role")
    uploaded = st.file_uploader("Upload your resume (PDF)", type=["pdf"], key="ats_upload")

    if uploaded is not None and st.button("✅ Check ATS Match"):
        with st.spinner("Scanning resume..."):
            resume_text = extract_resume_text(uploaded)
            extra_kw = ROLE_SKILLS.get(role, [])
            result = ats_match_score(resume_text, role, chunks, extra_keywords=extra_kw)

            score = result["score"]
            color = "#E74C3C" if score < 40 else "#F5A623" if score < 70 else "#4CAF9D"
            st.markdown(f'<span class="score-badge" style="background:{color}">ATS Match Score: {score}%</span>', unsafe_allow_html=True)

            fig = go.Figure(go.Bar(
                x=[score, 100 - score], y=["Match"], orientation="h",
                marker_color=[color, "#EDEAE2"], text=[f"{score}%", ""], textposition="inside"
            ))
            fig.update_layout(height=120, showlegend=False, xaxis=dict(range=[0, 100]),
                               margin=dict(l=10, r=10, t=10, b=10),
                               plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**✅ Keywords Found**")
                st.write(", ".join(result["matched"]) or "None found")
            with col2:
                st.markdown("**❌ Missing Keywords**")
                st.write(", ".join(result["missing"]) or "None — great coverage!")
    st.markdown('</div>', unsafe_allow_html=True)
# ============================================================
# PAGE: RESUME FEEDBACK (with score badge + download)
# ============================================================
elif st.session_state.page == "📄 Resume Feedback":
    st.markdown("""<div class="page-header"><h2>📄 Resume Feedback</h2>
    <p>Upload your resume as a PDF and get instant, structured AI feedback.</p></div>""", unsafe_allow_html=True)

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
                    feedback = analyze_resume(resume_text, target_role or None)

                    score_match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", feedback)
                    if score_match:
                        score = float(score_match.group(1))
                        color = "#E74C3C" if score < 5 else "#F5A623" if score < 7.5 else "#4CAF9D"
                        st.markdown(f'<span class="score-badge" style="background:{color}">Overall Score: {score}/10</span>', unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown(feedback)
                    st.download_button("⬇️ Download Feedback", feedback, file_name="resume_feedback.txt")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: SKILL GAP QUIZ (with color-coded bar chart)
# ============================================================
elif st.session_state.page == "🎯 Skill Gap Quiz":
    st.markdown("""<div class="page-header"><h2>🎯 Skill Gap Quiz</h2>
    <p>Rate your current skills and get a personalized roadmap.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    quiz_role = st.selectbox("Target role", list(ROLE_SKILLS.keys()))
    skills_to_rate = get_skills_for_role(quiz_role)

    st.markdown("#### Rate yourself (1 = beginner, 5 = expert)")
    ratings = {}
    for skill in skills_to_rate:
        ratings[skill] = st.slider(skill, 1, 5, 3, key=f"quiz_{skill}")

    if st.button("🧭 Generate My Roadmap"):
        colors = ["#E74C3C" if v <= 2 else "#F5A623" if v == 3 else "#4CAF9D" for v in ratings.values()]
        fig = go.Figure(go.Bar(
            x=list(ratings.values()), y=list(ratings.keys()), orientation="h",
            marker_color=colors, text=list(ratings.values()), textposition="outside"
        ))
        fig.update_layout(
            xaxis=dict(range=[0, 5.5], title="Self-Rating"), height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

        with st.spinner("Building your personalized roadmap..."):
            roadmap = generate_roadmap(quiz_role, ratings)
            st.markdown("---")
            st.markdown(roadmap)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: CAREER INTEREST QUIZ
# ============================================================
elif st.session_state.page == "🧠 Career Interest Quiz":
    st.markdown("""<div class="page-header"><h2>🧠 Career Interest Quiz</h2>
    <p>Not sure what fits you? Answer a few questions to get matched.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    answers = []
    for i, q in enumerate(INTEREST_QUESTIONS):
        choice = st.radio(q["q"], q["options"], key=f"interest_q{i}")
        answers.append(choice)

    if st.button("🔮 Find My Matches"):
        with st.spinner("Matching you to careers..."):
            result = recommend_careers(answers, ALL_ROLES)
            st.markdown("---")
            st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: INTERVIEW PREP
# ============================================================
elif st.session_state.page == "🎤 Interview Prep":
    st.markdown("""<div class="page-header"><h2>🎤 Interview Prep</h2>
    <p>Common interview questions and how to approach them.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    role = st.selectbox("Choose a role to prep for", ALL_ROLES)
    if st.button("🎤 Generate Questions"):
        with st.spinner("Preparing questions..."):
            result = generate_interview_questions(role)
            st.markdown("---")
            st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: LEARNING RESOURCES
# ============================================================
elif st.session_state.page == "📖 Learning Resources":
    st.markdown("""<div class="page-header"><h2>📖 Learning Resources</h2>
    <p>Where to start learning, free or paid, for any career.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    role = st.selectbox("Choose a career", ALL_ROLES)
    if st.button("📖 Find Resources"):
        with st.spinner("Curating resources..."):
            result = generate_learning_resources(role)
            st.markdown("---")
            st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: SALARY INSIGHTS (color-coded grouped bar chart)
# ============================================================
elif st.session_state.page == "💰 Salary Insights":
    st.markdown("""<div class="page-header"><h2>💰 Salary Insights</h2>
    <p>Approximate salary ranges by career and experience level.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    role = st.selectbox("Choose a career", list(SALARY_DATA.keys()))
    data = SALARY_DATA[role]

    levels = list(data.keys())
    mins = [data[l][0] for l in levels]
    maxs = [data[l][1] for l in levels]
    colors = ["#F5A623", "#E8734A", "#2B2A4C"]

    fig = go.Figure()
    for i, level in enumerate(levels):
        fig.add_trace(go.Bar(
            x=[level], y=[maxs[i] - mins[i]], base=mins[i],
            marker_color=colors[i], name=level,
            text=f"₹{mins[i]}-{maxs[i]} LPA", textposition="outside"
        ))
    fig.update_layout(
        showlegend=False, yaxis_title="LPA (₹ Lakhs/Annum)", height=350,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(SALARY_NOTE)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE: ABOUT
# ============================================================
elif st.session_state.page == "ℹ️ About CareerSaathi":
    st.markdown("""<div class="page-header"><h2>ℹ️ About CareerSaathi</h2>
    <p>How this platform works, under the hood.</p></div>""", unsafe_allow_html=True)

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("""
CareerSaathi is built on **Retrieval Augmented Generation (RAG)**: instead of an AI model
answering purely from memory, it first retrieves relevant, real career data, then generates
a natural-language answer grounded in that data.

**Pipeline:**
1. A dataset of 1,600+ career Q&A pairs is converted into vector embeddings using a
   **multilingual sentence-transformer model** (supports English + Hindi).
2. These embeddings are stored in a **FAISS** index for fast similarity search.
3. When you ask a question, it's embedded the same way, and the most relevant chunks
   are retrieved.
4. Those chunks are passed to **Llama 3.3 70B** (via Groq) to generate a grounded,
   natural answer — in the same language you asked in.

**Tools built on this foundation:** Chat, Career Comparison, Career Roadmaps, Resume
Feedback, Skill Gap Quiz, Career Interest Quiz, Interview Prep, Learning Resources, and
Salary Insights.
    """)
    st.markdown('</div>', unsafe_allow_html=True)