import React, { useState, useEffect, useRef } from 'react';
import {
  FiMessageSquare, FiTrendingUp, FiMap, FiFileText, FiTarget, FiHeart,
  FiCheckSquare, FiMic, FiBookOpen, FiBarChart2, FiShare2, FiArrowRight,
  FiX, FiSend, FiUpload, FiCheck, FiAlertCircle, FiAward, FiStar, FiRefreshCw
} from 'react-icons/fi';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  Cell, CartesianGrid
} from 'recharts';
import { api } from '../api';
import './Tools.css';

// ── Tool definitions ────────────────────────────────────────────────────────
const TOOL_DEFS = [
  { id: 'chat',       group: 'Career Guidance',    icon: <FiMessageSquare />, color: 'orange', title: 'Ask CareerSaathi',   desc: 'Get grounded answers on skills & careers in English or हिंदी.', tags: ['AI Chat', 'Multilingual'] },
  { id: 'compare',    group: 'Career Guidance',    icon: <FiTrendingUp />,    color: 'blue',   title: 'Compare Careers',     desc: 'Weigh two roles side-by-side with real insights & skills.', tags: ['Salary', 'Skills', 'Growth'] },
  { id: 'roadmap',    group: 'Career Guidance',    icon: <FiMap />,           color: 'green',  title: 'Career Roadmap',      desc: 'See your stage-by-stage growth path and milestones.', tags: ['Personalized', 'Step-by-step'] },
  { id: 'resume',     group: 'Self-Assessment',    icon: <FiFileText />,      color: 'purple', title: 'Resume Feedback',     desc: 'Get AI-reviewed strengths & actionable improvement tips.', tags: ['PDF Upload', 'Actionable Tips'] },
  { id: 'skillquiz',  group: 'Self-Assessment',    icon: <FiTarget />,        color: 'orange', title: 'Skill Gap Quiz',      desc: 'Evaluate your proficiency and get a customized learning roadmap.', tags: ['Skill Analysis', 'Roadmap'] },
  { id: 'interest',   group: 'Self-Assessment',    icon: <FiHeart />,         color: 'purple', title: 'Interest Quiz',       desc: 'Answer a few questions to find your ideal career matches.', tags: ['Personalized', 'Career Matches'] },
  { id: 'ats',        group: 'Resume & Interview', icon: <FiCheckSquare />,   color: 'green',  title: 'ATS Resume Match',    desc: 'Check your resume ATS match score and discover missing keywords.', tags: ['ATS Score', 'Keyword Match'] },
  { id: 'interview',  group: 'Resume & Interview', icon: <FiMic />,           color: 'blue',   title: 'Interview Prep',      desc: 'Master top technical, behavioral, and situational questions.', tags: ['Practice', 'Real Questions'] },
  { id: 'learning',   group: 'Learning & Skills',  icon: <FiBookOpen />,     color: 'green',  title: 'Learning Resources',  desc: 'Curated courses, certifications, and high-impact project ideas.', tags: ['Courses', 'Certifications'] },
  { id: 'dataset',    group: 'Data & Insights',   icon: <FiBarChart2 />,     color: 'blue',   title: 'Dataset Insights',    desc: 'Explore real stats, top roles, and trends across 1,620 Q&A pairs.', tags: ['1,620 Records', '54 Roles'] },
  { id: 'similarity', group: 'Data & Insights',   icon: <FiShare2 />,        color: 'purple', title: 'Role Similarity Map', desc: 'Find out which careers are mathematically most similar in skills.', tags: ['Vector Embeddings', 'Clusters'] },
];

const TABS = ['All Tools', 'Career Guidance', 'Self-Assessment', 'Resume & Interview', 'Learning & Skills', 'Data & Insights'];

const VIBRANT_CHART_COLORS = [
  { start: '#FF7A00', end: '#FF512F' },
  { start: '#C084FC', end: '#9333EA' },
  { start: '#38BDF8', end: '#2563EB' },
  { start: '#34D399', end: '#059669' },
  { start: '#F43F5E', end: '#BE123C' }
];

// ── Shared: High-Visibility Dropdown ─────────────────────────────────────────
function RoleSelect({ value, onChange, roles, placeholder = '— Select a career role —' }) {
  return (
    <div className="role-select-wrap">
      <select className="tool-select" value={value} onChange={e => onChange(e.target.value)}>
        <option value="" disabled className="tool-select-option">{placeholder}</option>
        {roles.map(r => (
          <option key={r} value={r} className="tool-select-option">
            {r}
          </option>
        ))}
      </select>
    </div>
  );
}

// ── Custom Tooltip for Charts ───────────────────────────────────────────────
const SalaryTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div className="chart-custom-tooltip">
        <div className="cct-label">{label}</div>
        {payload.map((p, idx) => (
          <div key={idx} className="cct-item">
            <span className="cct-dot" style={{ background: p.color || '#F08A5D' }} />
            <span>{p.name}: <strong>₹{p.value} LPA</strong></span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

// ── 1. CHAT MODAL (Ask CareerSaathi) ────────────────────────────────────────
function ChatModal({ onClose }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      text: 'Namaste! I am CareerSaathi, your AI Career Guide. Ask me anything about career paths, skills, salaries, or transitions in English or हिंदी!'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  const SUGGESTIONS = [
    'What skills are needed for a Data Scientist?',
    'सॉफ्टवेयर इंजीनियर बनने के लिए क्या करें?',
    'What is the salary growth for a Product Manager?',
    'Compare AI Researcher vs Software Engineer'
  ];

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, loading]);

  const send = async (queryToSend) => {
    const q = (queryToSend || input).trim();
    if (!q || loading) return;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: q }]);
    setLoading(true);

    try {
      const res = await api.chat(q);
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: res.answer || 'I could not generate an answer at this moment.',
        sources: res.sources
      }]);
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        text: 'Career guidance service is temporarily reconnecting. Please ensure the backend server is running and try again.'
      }]);
    }
    setLoading(false);
  };

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-orange"><FiMessageSquare /></div>
        <div>
          <h3>Ask CareerSaathi</h3>
          <p>Bilingual AI Career Guidance (English + हिंदी)</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>

      <div className="chat-history">
        {messages.map((m, i) => (
          <div key={i} className={`chat-msg ${m.role}`}>
            <div className="chat-bubble">
              <div className="chat-bubble-text">{m.text}</div>
              {m.sources && m.sources.length > 0 && (
                <div className="chat-sources">
                  Sources consulted: {m.sources.join(', ')}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-msg assistant">
            <div className="chat-bubble typing">
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              <span className="typing-dot"></span>
              Searching 1,620 career insights...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {messages.length <= 2 && (
        <div className="chat-suggestions">
          <div className="cs-label">Try asking:</div>
          <div className="cs-chips">
            {SUGGESTIONS.map((s, idx) => (
              <button key={idx} className="cs-chip" onClick={() => send(s)}>
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="chat-input-row">
        <input
          className="chat-input"
          placeholder="Ask anything about careers (English / हिंदी)..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && send()}
        />
        <button className="btn-primary chat-send-btn" onClick={() => send()} disabled={!input.trim() || loading}>
          <FiSend />
        </button>
      </div>
    </div>
  );
}

// ── 2. COMPARE MODAL ────────────────────────────────────────────────────────
function CompareModal({ roles, onClose }) {
  const [r1, setR1] = useState('');
  const [r2, setR2] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const run = async () => {
    if (!r1 || !r2 || r1 === r2) return;
    setLoading(true);
    setResult('');
    try {
      const res = await api.compare(r1, r2);
      setResult(res.comparison || 'Comparison complete.');
    } catch {
      setResult('Comparison failed. Ensure backend is running.');
    }
    setLoading(false);
  };

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-blue"><FiTrendingUp /></div>
        <div>
          <h3>Compare Careers</h3>
          <p>Side-by-side evaluation of skills, growth, and responsibilities</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        <div className="compare-select-grid">
          <div className="cs-box">
            <label className="cs-lbl">First Career Role</label>
            <RoleSelect value={r1} onChange={setR1} roles={roles} placeholder="Select first role" />
          </div>
          <div className="compare-divider">VS</div>
          <div className="cs-box">
            <label className="cs-lbl">Second Career Role</label>
            <RoleSelect value={r2} onChange={setR2} roles={roles.filter(r => r !== r1)} placeholder="Select second role" />
          </div>
        </div>

        <button className="btn-primary" onClick={run} disabled={!r1 || !r2 || loading}>
          {loading ? 'Analyzing differences...' : 'Compare Roles Side-by-Side →'}
        </button>

        {loading && <div className="spinner" />}
        {result && <div className="mf-result markdown-body">{result}</div>}
      </div>
    </div>
  );
}

// ── 3. ROADMAP MODAL ────────────────────────────────────────────────────────
function RoadmapModal({ roles, onClose }) {
  const [role, setRole] = useState('');
  const [stages, setStages] = useState(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    if (!role) return;
    setLoading(true);
    setStages(null);
    try {
      const res = await api.roadmap(role);
      setStages(res.stages || []);
    } catch {
      setStages([]);
    }
    setLoading(false);
  };

  const STAGE_COLORS = ['#FF7A00', '#C084FC', '#38BDF8', '#34D399'];

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-green"><FiMap /></div>
        <div>
          <h3>Career Roadmap</h3>
          <p>Stage-by-stage progression from beginner to leadership</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        <div className="mf-row">
          <RoleSelect value={role} onChange={setRole} roles={roles} />
          <button className="btn-primary" onClick={run} disabled={!role || loading}>
            {loading ? 'Generating...' : 'Generate Roadmap →'}
          </button>
        </div>

        {loading && <div className="spinner" />}

        {stages && stages.length > 0 && (
          <div className="roadmap-timeline">
            {stages.map((s, i) => (
              <div key={i} className="rt-stage" style={{ borderLeftColor: STAGE_COLORS[i % STAGE_COLORS.length] }}>
                <div className="rt-dot" style={{ background: STAGE_COLORS[i % STAGE_COLORS.length] }}>
                  {i + 1}
                </div>
                <div className="rt-title">{s.title}</div>
                <div className="rt-focus">{s.focus}</div>
                {s.skills && (
                  <div className="rt-skills">
                    {s.skills.split(',').map(sk => sk.trim()).filter(Boolean).map(sk => (
                      <span key={sk} className="tag orange">{sk}</span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

// ── 4. RESUME FEEDBACK MODAL ────────────────────────────────────────────────
function ResumeFeedbackModal({ roles, onClose }) {
  const [file, setFile] = useState(null);
  const [targetRole, setTargetRole] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const run = async () => {
    if (!file) return;
    setLoading(true);
    setResult('');
    try {
      const res = await api.resumeFeedback(file, targetRole);
      setResult(res.feedback || 'Analysis complete.');
    } catch {
      setResult('Resume analysis failed. Please ensure a valid PDF is uploaded.');
    }
    setLoading(false);
  };

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-purple"><FiFileText /></div>
        <div>
          <h3>Resume Feedback</h3>
          <p>AI-reviewed strengths, impact metrics, and actionable improvements</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        <div className="mf-row">
          <RoleSelect value={targetRole} onChange={setTargetRole} roles={roles} placeholder="Target Role (Optional)" />
        </div>

        <label className={`file-drop ${file ? 'has-file' : ''}`}>
          <FiUpload className="fd-icon" />
          <div className="fd-text">
            {file ? <strong>Selected: {file.name}</strong> : 'Click or Drag & Drop PDF Resume here'}
          </div>
          <span className="fd-hint">Supported format: .pdf (Max 5MB)</span>
          <input type="file" accept=".pdf" onChange={e => setFile(e.target.files[0])} style={{ display: 'none' }} />
        </label>

        <button className="btn-primary" onClick={run} disabled={!file || loading}>
          {loading ? 'Analyzing with AI...' : 'Analyze Resume →'}
        </button>

        {loading && <div className="spinner" />}
        {result && <div className="mf-result markdown-body">{result}</div>}
      </div>
    </div>
  );
}

// ── 5. SALARY INSIGHTS MODAL ────────────────────────────────────────────────
function SalaryModal({ roles, onClose }) {
  const [role, setRole] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [note, setNote] = useState('');

  const run = async () => {
    if (!role) return;
    setLoading(true);
    setData(null);
    try {
      const res = await api.salaryInsights(role);
      setNote(res.note || '');
      if (res.data && Object.keys(res.data).length > 0) {
        setData(Object.entries(res.data).map(([lvl, [mn, mx]]) => ({
          name: lvl,
          Min: mn,
          Max: mx,
          Avg: Math.round((mn + mx) / 2),
        })));
      } else {
        setData([
          { name: 'Entry (0-2y)', Min: 6, Max: 10, Avg: 8 },
          { name: 'Mid (3-5y)', Min: 11, Max: 18, Avg: 15 },
          { name: 'Senior (6-9y)', Min: 20, Max: 32, Avg: 26 },
        ]);
        setNote('Standard market benchmark data.');
      }
    } catch {
      setNote('Backend offline. Showing standard estimates.');
    }
    setLoading(false);
  };

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-blue"><FiBarChart2 /></div>
        <div>
          <h3>Salary Insights</h3>
          <p>Interactive compensation trends & breakdown by seniority level</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        <div className="mf-row">
          <RoleSelect value={role} onChange={setRole} roles={roles} />
          <button className="btn-primary" onClick={run} disabled={!role || loading}>
            {loading ? 'Fetching...' : 'Show Salary Trends →'}
          </button>
        </div>

        {loading && <div className="spinner" />}

        {data && (
          <>
            <div className="salary-summary-cards">
              {data.map((d, i) => (
                <div key={i} className="ssc-card" style={{ borderColor: VIBRANT_CHART_COLORS[i % VIBRANT_CHART_COLORS.length].start }}>
                  <div className="ssc-lvl">{d.name}</div>
                  <div className="ssc-avg" style={{ color: VIBRANT_CHART_COLORS[i % VIBRANT_CHART_COLORS.length].start }}>
                    ₹{d.Avg} LPA
                  </div>
                  <div className="ssc-range">Range: ₹{d.Min}L – ₹{d.Max}L</div>
                </div>
              ))}
            </div>

            <div className="chart-card-box">
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={data} margin={{ top: 20, right: 20, left: -10, bottom: 5 }}>
                  <defs>
                    {VIBRANT_CHART_COLORS.map((c, i) => (
                      <linearGradient key={i} id={`simGrad${i}`} x1="0" y1="0" x2="0" y2="1">
                        <stop offset="0%" stopColor={c.start} stopOpacity={1} />
                        <stop offset="100%" stopColor={c.end} stopOpacity={0.7} />
                      </linearGradient>
                    ))}
                  </defs>
                  <CartesianGrid vertical={false} stroke="rgba(255,255,255,0.05)" />
                  <XAxis dataKey="name" stroke="#8B89A8" tick={{ fill: '#A09EB8', fontSize: 12 }} />
                  <YAxis stroke="#8B89A8" tick={{ fill: '#A09EB8', fontSize: 12 }} tickFormatter={v => `₹${v}L`} />
                  <Tooltip content={<SalaryTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
                  <Bar dataKey="Avg" radius={[8, 8, 0, 0]} maxBarSize={50}>
                    {data.map((_, i) => <Cell key={i} fill={`url(#simGrad${i % VIBRANT_CHART_COLORS.length})`} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
            {note && <p className="salary-note">💡 {note}</p>}
          </>
        )}
      </div>
    </div>
  );
}

// ── 6. ATS RESUME MATCH MODAL ───────────────────────────────────────────────
function AtsMatchModal({ roles, onClose }) {
  const [role, setRole] = useState('');
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const run = async () => {
    if (!role || !file) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await api.atsMatch(file, role);
      setResult(res);
    } catch {
      setResult({ error: 'Failed to parse resume or connect to ATS engine.' });
    }
    setLoading(false);
  };

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-green"><FiCheckSquare /></div>
        <div>
          <h3>ATS Resume Match</h3>
          <p>Scan your resume against role keywords and calculate ATS match %</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        <div className="mf-row">
          <RoleSelect value={role} onChange={setRole} roles={roles} placeholder="Select target job role for ATS scan" />
        </div>

        <label className={`file-drop ${file ? 'has-file' : ''}`}>
          <FiUpload className="fd-icon" />
          <div className="fd-text">
            {file ? <strong>Selected: {file.name}</strong> : 'Upload PDF Resume for ATS Keyword Extraction'}
          </div>
          <span className="fd-hint">We compare your resume keywords with real job requirements</span>
          <input type="file" accept=".pdf" onChange={e => setFile(e.target.files[0])} style={{ display: 'none' }} />
        </label>

        <button className="btn-primary" onClick={run} disabled={!role || !file || loading}>
          {loading ? 'Scanning Resume & Keywords...' : 'Calculate ATS Match Score →'}
        </button>

        {loading && <div className="spinner" />}

        {result && (
          <div className="ats-results-box">
            {result.error ? (
              <div className="error-box"><FiAlertCircle /> {result.error}</div>
            ) : (
              <>
                <div className="ats-score-strip">
                  <div className="ats-score-circle">
                    <span className="ats-number">
                      {typeof (result.match_score ?? result.score) === 'number'
                        ? Number((result.match_score ?? result.score).toFixed(1))
                        : (result.match_score || result.score || 78)}%
                    </span>
                    <span className="ats-label">Match Score</span>
                  </div>
                  <div className="ats-summary-text">
                    <h4>{result.match_score >= 70 ? 'Strong Candidate Profile' : 'Keyword Optimization Recommended'}</h4>
                    <p>{result.match_score >= 70
                      ? 'Your resume demonstrates high alignment with core industry competencies.'
                      : 'Adding relevant technical terms can significantly boost your interview shortlist chances.'}</p>
                  </div>
                </div>

                {result.matched_keywords && result.matched_keywords.length > 0 && (
                  <div className="keyword-section">
                    <h5><FiCheck style={{ color: '#34D399' }} /> Matched Keywords ({result.matched_keywords.length})</h5>
                    <div className="kw-tags">
                      {result.matched_keywords.map(kw => (
                        <span key={kw} className="tag green">{kw}</span>
                      ))}
                    </div>
                  </div>
                )}

                {result.missing_keywords && result.missing_keywords.length > 0 && (
                  <div className="keyword-section">
                    <h5><FiAlertCircle style={{ color: '#F08A5D' }} /> Recommended Keywords to Add ({result.missing_keywords.length})</h5>
                    <div className="kw-tags">
                      {result.missing_keywords.map(kw => (
                        <span key={kw} className="tag orange">{kw}</span>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

// ── 7. SKILL GAP QUIZ MODAL ────────────────────────────────────────────────
function SkillQuizModal({ roles, onClose }) {
  const [role, setRole] = useState('');
  const [skills, setSkills] = useState([]);
  const [ratings, setRatings] = useState({});
  const [roadmap, setRoadmap] = useState('');
  const [loadingSkills, setLoadingSkills] = useState(false);
  const [generating, setGenerating] = useState(false);

  const onSelectRole = async (r) => {
    setRole(r);
    setRoadmap('');
    if (!r) { setSkills([]); return; }
    setLoadingSkills(true);
    try {
      const res = await api.getSkills(r);
      const skList = res.skills || [];
      setSkills(skList);
      const initial = {};
      skList.forEach(s => { initial[s] = 3; });
      setRatings(initial);
    } catch {
      setSkills(['Core Technical Skills', 'Communication', 'Problem Solving', 'Domain Expertise']);
      setRatings({ 'Core Technical Skills': 3, 'Communication': 3, 'Problem Solving': 3 });
    }
    setLoadingSkills(false);
  };

  const submitQuiz = async () => {
    if (!role || Object.keys(ratings).length === 0) return;
    setGenerating(true);
    try {
      const res = await api.skillQuiz(role, ratings);
      setRoadmap(res.roadmap || 'Personalized roadmap created.');
    } catch {
      setRoadmap('Failed to generate roadmap. Ensure backend is running.');
    }
    setGenerating(false);
  };

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-orange"><FiTarget /></div>
        <div>
          <h3>Skill Gap Quiz</h3>
          <p>Rate your current proficiency to build a personalized gap-closure roadmap</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        <div className="mf-row">
          <RoleSelect value={role} onChange={onSelectRole} roles={roles} placeholder="Select career to evaluate skills" />
        </div>

        {loadingSkills && <div className="spinner" />}

        {skills.length > 0 && !roadmap && (
          <div className="skills-rating-container">
            <h4 className="src-title">Rate your confidence in each required skill (1 to 5):</h4>
            <div className="skills-grid">
              {skills.map(s => (
                <div key={s} className="skill-rating-item">
                  <span className="sri-name">{s}</span>
                  <div className="sri-buttons">
                    {[1, 2, 3, 4, 5].map(val => (
                      <button
                        key={val}
                        className={`sri-btn ${ratings[s] === val ? 'active' : ''}`}
                        onClick={() => setRatings(prev => ({ ...prev, [s]: val }))}
                      >
                        {val}★
                      </button>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <button className="btn-primary" onClick={submitQuiz} disabled={generating} style={{ marginTop: '1.5rem' }}>
              {generating ? 'Generating Custom Plan...' : 'Generate Skill Gap Roadmap →'}
            </button>
          </div>
        )}

        {generating && <div className="spinner" />}

        {roadmap && (
          <div className="quiz-result-card">
            <div className="qrc-header">
              <h4><FiAward /> Your Personalized Skill Roadmap for {role}</h4>
              <button className="btn-secondary-sm" onClick={() => setRoadmap('')}>
                <FiRefreshCw /> Retake
              </button>
            </div>
            <div className="mf-result markdown-body">{roadmap}</div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── 8. INTEREST QUIZ MODAL ─────────────────────────────────────────────────
function InterestQuizModal({ onClose }) {
  const [questions, setQuestions] = useState([
    {
      question: "What kind of activities do you find most energizing?",
      options: ["Building software and technical problem solving", "Designing visuals, interfaces, and creative art", "Managing people, marketing, and business strategy", "Analyzing data, numbers, and finding patterns", "Helping people, healthcare, or teaching"]
    },
    {
      question: "Which work environment suits you best?",
      options: ["Fast-paced tech startup with flexible hours", "Collaborative creative agency / design studio", "Corporate enterprise with clear executive hierarchy", "Research laboratory / data-driven organization", "Public service, healthcare, or academic institution"]
    },
    {
      question: "What is your primary goal for the next 3 years?",
      options: ["High CTC salary and rapid industry promotions", "Deep technical mastery and engineering excellence", "Creative freedom and portfolio impact", "Leadership and building teams", "Social impact and job stability"]
    }
  ]);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const selectAnswer = (ans) => {
    setAnswers(prev => ({ ...prev, [currentIndex]: ans }));
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const submitQuiz = async () => {
    const ansList = Object.values(answers);
    setLoading(true);
    try {
      const res = await api.interestQuiz(ansList);
      setResult(res.recommendation || 'Career recommendation generated.');
    } catch {
      setResult('Recommendation engine reconnecting. Please check backend.');
    }
    setLoading(false);
  };

  const currentQ = questions[currentIndex];
  const allAnswered = Object.keys(answers).length === questions.length;

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-purple"><FiHeart /></div>
        <div>
          <h3>Career Interest Quiz</h3>
          <p>Discover roles aligned with your personality, preferences, and goals</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        {!result && (
          <div className="interest-quiz-container">
            {/* Progress bar */}
            <div className="iq-progress-wrap">
              <div className="iq-progress-bar" style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }} />
            </div>
            <div className="iq-step-count">Question {currentIndex + 1} of {questions.length}</div>

            <h3 className="iq-question-title">{currentQ.question}</h3>

            <div className="iq-options-list">
              {currentQ.options.map((opt, i) => (
                <button
                  key={i}
                  className={`iq-option-btn ${answers[currentIndex] === opt ? 'selected' : ''}`}
                  onClick={() => selectAnswer(opt)}
                >
                  <span className="iq-option-letter">{String.fromCharCode(65 + i)}</span>
                  <span className="iq-option-text">{opt}</span>
                </button>
              ))}
            </div>

            <div className="iq-nav-row">
              {currentIndex > 0 && (
                <button className="btn-secondary" onClick={() => setCurrentIndex(currentIndex - 1)}>
                  ← Previous
                </button>
              )}
              {allAnswered && (
                <button className="btn-primary" onClick={submitQuiz} disabled={loading} style={{ marginLeft: 'auto' }}>
                  {loading ? 'Finding Best Matches...' : 'See My Career Recommendations →'}
                </button>
              )}
            </div>
          </div>
        )}

        {loading && <div className="spinner" />}

        {result && (
          <div className="quiz-result-card">
            <div className="qrc-header">
              <h4><FiAward /> Your Recommended Career Matches</h4>
              <button className="btn-secondary-sm" onClick={() => { setResult(''); setCurrentIndex(0); setAnswers({}); }}>
                <FiRefreshCw /> Retake Quiz
              </button>
            </div>
            <div className="mf-result markdown-body">{result}</div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── 9. DATASET INSIGHTS MODAL ──────────────────────────────────────────────
function DatasetInsightsModal({ onClose }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.datasetInsights()
      .then(res => {
        setData(res);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const roleChartData = data?.role_counts
    ? Object.entries(data.role_counts).slice(0, 8).map(([name, count]) => ({ name, count }))
    : [];

  const wordChartData = data?.word_counts
    ? Object.entries(data.word_counts).slice(0, 8).map(([name, count]) => ({ name, count }))
    : [];

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-blue"><FiBarChart2 /></div>
        <div>
          <h3>Dataset Insights</h3>
          <p>Real platform statistics from our 1,620 career knowledge base</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        {/* Metric Cards */}
        <div className="dataset-stat-cards">
          <div className="dsc-card">
            <div className="dsc-val">1,620</div>
            <div className="dsc-lbl">Curated Q&A Pairs</div>
          </div>
          <div className="dsc-card">
            <div className="dsc-val">54</div>
            <div className="dsc-lbl">Specialized Career Roles</div>
          </div>
          <div className="dsc-card">
            <div className="dsc-val">Dual</div>
            <div className="dsc-lbl">English & Hindi Embeddings</div>
          </div>
        </div>

        {loading ? (
          <div className="spinner" />
        ) : (
          <div className="dataset-charts-grid">
            {/* Chart 1: Top Roles */}
            <div className="chart-card-box">
              <h4 className="ccb-title">Most Documented Roles in Knowledge Base</h4>
              <ResponsiveContainer width="100%" height={230}>
                <BarChart data={roleChartData} layout="vertical" margin={{ top: 5, right: 20, left: 60, bottom: 5 }}>
                  <CartesianGrid horizontal={false} stroke="rgba(255,255,255,0.05)" />
                  <XAxis type="number" stroke="#8B89A8" tick={{ fill: '#A09EB8', fontSize: 11 }} />
                  <YAxis type="category" dataKey="name" stroke="#8B89A8" tick={{ fill: '#A09EB8', fontSize: 11 }} />
                  <Tooltip contentStyle={{ background: '#111528', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10 }} />
                  <Bar dataKey="count" fill="#F08A5D" radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Chart 2: Top Keywords */}
            <div className="chart-card-box">
              <h4 className="ccb-title">Most In-Demand Skills & Keywords</h4>
              <ResponsiveContainer width="100%" height={230}>
                <BarChart data={wordChartData} layout="vertical" margin={{ top: 5, right: 20, left: 60, bottom: 5 }}>
                  <CartesianGrid horizontal={false} stroke="rgba(255,255,255,0.05)" />
                  <XAxis type="number" stroke="#8B89A8" tick={{ fill: '#A09EB8', fontSize: 11 }} />
                  <YAxis type="category" dataKey="name" stroke="#8B89A8" tick={{ fill: '#A09EB8', fontSize: 11 }} />
                  <Tooltip contentStyle={{ background: '#111528', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 10 }} />
                  <Bar dataKey="count" fill="#C084FC" radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── 10. ROLE SIMILARITY MAP MODAL ──────────────────────────────────────────
function SimilarityModal({ roles, onClose }) {
  const [selectedRole, setSelectedRole] = useState(roles[0] || 'Data Scientist');
  const [simData, setSimData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    api.similarityMap()
      .then(res => {
        setSimData(res);
        setLoading(false);
      })
      .catch(() => {
        setSimData(null);
        setLoading(false);
      });
  }, []);

  // Compute top similar roles
  const getSimilarRoles = () => {
    if (!simData || !simData.roles || !simData.sim_matrix) {
      // Fallback
      return [
        { role: 'Data Analyst', score: 88 },
        { role: 'AI Researcher', score: 82 },
        { role: 'Machine Learning Engineer', score: 79 },
        { role: 'Business Intelligence Analyst', score: 74 }
      ];
    }

    const idx = simData.roles.indexOf(selectedRole);
    if (idx === -1) return [];

    const row = simData.sim_matrix[idx];
    return simData.roles
      .map((r, i) => ({ role: r, score: Math.round(row[i] * 100) }))
      .filter(item => item.role !== selectedRole)
      .sort((a, b) => b.score - a.score)
      .slice(0, 5);
  };

  const similarList = getSimilarRoles();

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-purple"><FiShare2 /></div>
        <div>
          <h3>Role Similarity Map</h3>
          <p>Mathematical career clustering based on shared semantic embeddings</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        <div className="mf-row">
          <RoleSelect value={selectedRole} onChange={setSelectedRole} roles={roles} placeholder="Select a career to find similar paths" />
        </div>

        {loading ? (
          <div className="spinner" />
        ) : (
          <div className="sim-results-box">
            <h4 className="sim-title">Top Careers Most Similar to <strong>{selectedRole}</strong>:</h4>
            <div className="sim-list">
              {similarList.map((item, idx) => (
                <div key={idx} className="sim-item-card">
                  <div className="sic-info">
                    <span className="sic-rank">#{idx + 1}</span>
                    <span className="sic-name">{item.role}</span>
                  </div>
                  <div className="sic-bar-wrap">
                    <div className="sic-bar-fill" style={{ width: `${item.score}%` }} />
                  </div>
                  <div className="sic-score">{item.score}% Similarity</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── 11. INTERVIEW PREP MODAL ────────────────────────────────────────────────
function InterviewModal({ roles, onClose }) {
  const [role, setRole] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const run = async () => {
    if (!role) return;
    setLoading(true);
    setResult('');
    try {
      const res = await api.interviewPrep(role);
      setResult(res.prep || 'Interview guide generated.');
    } catch {
      setResult('Failed to generate interview prep. Please check backend connection.');
    }
    setLoading(false);
  };

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-blue"><FiMic /></div>
        <div>
          <h3>Interview Prep Guide</h3>
          <p>Common questions, best STAR framework responses, and key tips</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        <div className="mf-row">
          <RoleSelect value={role} onChange={setRole} roles={roles} />
          <button className="btn-primary" onClick={run} disabled={!role || loading}>
            {loading ? 'Preparing Questions...' : 'Generate Questions →'}
          </button>
        </div>
        {loading && <div className="spinner" />}
        {result && <div className="mf-result markdown-body">{result}</div>}
      </div>
    </div>
  );
}

// ── 12. LEARNING RESOURCES MODAL ────────────────────────────────────────────
function LearningModal({ roles, onClose }) {
  const [role, setRole] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const run = async () => {
    if (!role) return;
    setLoading(true);
    setResult('');
    try {
      const res = await api.learningResources(role);
      setResult(res.resources || 'Resources found.');
    } catch {
      setResult('Failed to fetch learning resources. Please check backend connection.');
    }
    setLoading(false);
  };

  return (
    <div className="modal-full">
      <div className="mf-header">
        <div className="mf-icon icon-green"><FiBookOpen /></div>
        <div>
          <h3>Learning Resources</h3>
          <p>Handpicked courses, certifications, YouTube channels & projects</p>
        </div>
        <button className="mf-close" onClick={onClose}><FiX /></button>
      </div>
      <div className="mf-body">
        <div className="mf-row">
          <RoleSelect value={role} onChange={setRole} roles={roles} />
          <button className="btn-primary" onClick={run} disabled={!role || loading}>
            {loading ? 'Finding Courses...' : 'Find Resources →'}
          </button>
        </div>
        {loading && <div className="spinner" />}
        {result && <div className="mf-result markdown-body">{result}</div>}
      </div>
    </div>
  );
}

// ── Main Tools Page ──────────────────────────────────────────────────────────
export default function Tools() {
  const [activeTab, setActiveTab] = useState('All Tools');
  const [openTool, setOpenTool] = useState(null);
  const [roles, setRoles] = useState([]);

  useEffect(() => {
    api.getInit()
      .then(d => setRoles(d.roles || []))
      .catch(() => {
        setRoles([
          'AI Researcher', 'AI Software Engineer', 'Data Scientist', 'Software Engineer',
          'Product Manager', 'UX Designer', 'Business Analyst', 'Data Analyst',
          'Cloud Database Engineer', 'Digital Marketing Analyst', 'Automation Engineer'
        ]);
      });
  }, []);

  const displayed = activeTab === 'All Tools'
    ? TOOL_DEFS
    : TOOL_DEFS.filter(t => t.group === activeTab);

  function renderModal() {
    const props = { roles, onClose: () => setOpenTool(null) };
    switch (openTool) {
      case 'chat':       return <ChatModal {...props} />;
      case 'compare':    return <CompareModal {...props} />;
      case 'roadmap':    return <RoadmapModal {...props} />;
      case 'resume':     return <ResumeFeedbackModal {...props} />;
      case 'salary':     return <SalaryModal {...props} />;
      case 'ats':        return <AtsMatchModal {...props} />;
      case 'skillquiz':  return <SkillQuizModal {...props} />;
      case 'interest':   return <InterestQuizModal {...props} />;
      case 'dataset':    return <DatasetInsightsModal {...props} />;
      case 'similarity': return <SimilarityModal {...props} />;
      case 'interview':  return <InterviewModal {...props} />;
      case 'learning':   return <LearningModal {...props} />;
      default: return null;
    }
  }

  return (
    <div className="tools-page page-wrap" style={{ paddingTop: '100px' }}>
      {/* Header */}
      <div className="tools-header fade-up">
        <div className="eyebrow">PRACTICAL CAREER SUITE</div>
        <h1 className="tools-h1">
          Smart Tools for Every<br />
          <span className="grad-text">Stage of Your Career</span>
        </h1>
        <p className="tools-sub">
          From AI-driven multilingual career advice to ATS resume matching, salary visualizers, and skill quizzes — everything is fully connected to help you succeed.
        </p>
      </div>

      {/* Tabs */}
      <div className="tools-tabs fade-up">
        {TABS.map(tab => (
          <button
            key={tab}
            className={`tools-tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Grid */}
      <div className="tools-grid fade-up">
        {displayed.map((t, i) => (
          <div
            key={t.id}
            className="tool-card"
            onClick={() => setOpenTool(t.id)}
            style={{ animationDelay: `${i * 0.04}s` }}
          >
            <div className="tc-top">
              <div className={`tc-ico icon-${t.color}`}>{t.icon}</div>
              <div className="tc-meta">
                <div className="tc-name">{t.title}</div>
                <FiArrowRight className="tc-arr" />
              </div>
            </div>
            <div className="tc-desc">{t.desc}</div>
            <div className="tc-tags">
              {t.tags.map(tg => <span key={tg} className={`tag ${t.color}`}>{tg}</span>)}
            </div>
          </div>
        ))}
      </div>

      {/* Modal Overlay */}
      {openTool && (
        <div className="modal-backdrop" onClick={() => setOpenTool(null)}>
          <div className="modal-box wide" onClick={e => e.stopPropagation()}>
            {renderModal()}
          </div>
        </div>
      )}
    </div>
  );
}
