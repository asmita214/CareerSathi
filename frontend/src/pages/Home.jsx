import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FiArrowRight, FiMessageSquare, FiTrendingUp, FiMap, FiFileText,
  FiTarget, FiHeart, FiCheckSquare, FiMic, FiBookOpen, FiBarChart2
} from 'react-icons/fi';
import heroImg from '../assets/hero.png';
import './Home.css';

const TOOLS = [
  { icon: <FiMessageSquare />, title: 'Ask CareerSaathi', desc: 'Get grounded answers on skills, growth paths and careers.', tags: ['AI Chat', 'Multilingual'], color: 'orange' },
  { icon: <FiTrendingUp />,    title: 'Compare Careers',   desc: 'Weigh two roles side-by-side with real insights.', tags: ['Salary', 'Skills', 'Growth'], color: 'blue' },
  { icon: <FiMap />,           title: 'Career Roadmap',    desc: 'See your stage-by-stage growth path.', tags: ['Personalized', 'Step-by-step'], color: 'green' },
  { icon: <FiFileText />,      title: 'Resume Feedback',   desc: 'Get AI-reviewed strengths and improvement tips.', tags: ['ATS Score', 'Actionable Tips'], color: 'purple' },
  { icon: <FiTarget />,        title: 'Skill Gap Quiz',    desc: 'Evaluate your skills and find learning paths.', tags: ['Skill Analysis', 'Recommendations'], color: 'orange' },
  { icon: <FiHeart />,         title: 'Interest Quiz',     desc: 'Discover careers that match your interests.', tags: ['Personality Based', 'Career Matches'], color: 'purple' },
];

const BRANDS = ['Google', 'Microsoft', 'Coursera', 'LinkedIn', 'Kaggle', 'Udemy'];

const JOURNEY_STEPS = [
  { icon: '🔍', label: 'Explore', sub: 'Discover possibilities' },
  { icon: '📚', label: 'Learn',   sub: 'Build in-demand skills' },
  { icon: '🗺️', label: 'Plan',    sub: 'Make informed choices' },
  { icon: '🚀', label: 'Grow',    sub: 'Achieve your goals' },
];

export default function Home() {
  const nav = useNavigate();
  const [cursorPos, setCursorPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const move = e => setCursorPos({ x: e.clientX, y: e.clientY });
    window.addEventListener('mousemove', move);
    return () => window.removeEventListener('mousemove', move);
  }, []);

  return (
    <div className="home">
      {/* Cursor glow */}
      <div
        className="cursor-glow"
        style={{ left: cursorPos.x, top: cursorPos.y }}
      />

      {/* ── HERO ── */}
      <section className="hero">
        <div className="hero-left fade-up">
          <div className="eyebrow">✦ AI-Powered Career Guidance</div>
          <h1 className="hero-h1">
            Discover <span className="grad-text">a Future</span><br />
            That Feels Like <span className="italic-text">You.</span>
          </h1>
          <p className="hero-sub">
            Personalized guidance. Real insights. Practical tools.<br />
            All in one place — in English or हिंदी.
          </p>
          <div className="hero-ctas">
            <button className="btn-primary" onClick={() => nav('/tools')}>
              Start Your Journey <FiArrowRight />
            </button>
            <button className="btn-ghost" onClick={() => nav('/explore')}>
              ▷ Explore Careers
            </button>
          </div>
        </div>

        <div className="hero-img-wrap fade-up" style={{ animationDelay: '0.2s' }}>
          <img src={heroImg} alt="Career guidance illustration" className="hero-img" />
          <div className="hero-float-card top-right glass-card">
            <div className="float-icon">🎯</div>
            <div>
              <div className="float-title">Turn your curiosity</div>
              <div className="float-sub">into a career you love.</div>
            </div>
          </div>
        </div>

        <div className="hero-right fade-up" style={{ animationDelay: '0.3s' }}>
          <div className="quick-card glass-card">
            <div className="quick-title">Quick Access</div>
            {[['🔎','Explore Careers'],[' 📊','Build Skills'],['📄','Improve Resume'],['📈','Get Real Insights']].map(([icon, label]) => (
              <button key={label} className="quick-item" onClick={() => nav('/tools')}>
                <span>{icon}</span><span>{label}</span><FiArrowRight className="qi-arrow" />
              </button>
            ))}
          </div>
          <div className="hero-stats glass-card">
            {[['50+','Career Roles'],['1,600+','Q&A Entries'],['10','AI Tools'],['2','Languages']].map(([n, l]) => (
              <div key={l} className="hs-item">
                <div className="hs-num">{n}</div>
                <div className="hs-label">{l}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── TOOLS SECTION ── */}
      <section className="tools-sec fade-up">
        <div className="sec-header">
          <div>
            <div className="eyebrow">EXPLORE WHAT YOU CAN DO</div>
            <h2 className="sec-h2">Everything you need, in one place.</h2>
          </div>
          <button className="btn-ghost" onClick={() => nav('/tools')}>
            View All Tools <FiArrowRight />
          </button>
        </div>

        <div className="tools-scroll">
          {TOOLS.map((t, i) => (
            <div key={i} className="tool-chip glass-card" onClick={() => nav('/tools')}>
              <div className={`tc-icon icon-${t.color}`}>{t.icon}</div>
              <div className="tc-body">
                <div className="tc-title">{t.title}</div>
                <div className="tc-desc">{t.desc}</div>
                <div className="tc-tags">
                  {t.tags.map(tg => <span key={tg} className={`tag ${t.color}`}>{tg}</span>)}
                </div>
              </div>
              <FiArrowRight className="tc-arrow" />
            </div>
          ))}
        </div>
      </section>

      {/* ── JOURNEY SECTION ── */}
      <section className="journey fade-up">
        <div className="journey-text">
          <div className="eyebrow">NOT JUST CAREERS.</div>
          <h2 className="journey-h">
            Guidance for<br/>every stage of <em className="grad-text">your journey.</em>
          </h2>
        </div>
        <div className="journey-steps">
          {JOURNEY_STEPS.map((s, i) => (
            <React.Fragment key={s.label}>
              <div className="journey-step glass-card">
                <div className="js-icon">{s.icon}</div>
                <div className="js-label">{s.label}</div>
                <div className="js-sub">{s.sub}</div>
              </div>
              {i < JOURNEY_STEPS.length - 1 && <div className="journey-line" />}
            </React.Fragment>
          ))}
        </div>
      </section>
    </div>
  );
}
