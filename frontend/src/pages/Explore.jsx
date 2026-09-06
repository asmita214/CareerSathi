import React, { useState, useEffect, useMemo } from 'react';
import { FiSearch, FiArrowRight, FiX, FiTrendingUp, FiBarChart2, FiMap, FiBookOpen, FiAward, FiDollarSign } from 'react-icons/fi';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from 'recharts';
import { api } from '../api';
import './Explore.css';

// ── Role metadata: images, categories, and salary ranges ────────────────────
const ROLE_IMAGE_MAP = {
  'AI Researcher': '/images/careers/ai_researcher.jpg',
  'AI Software Engineer': '/images/careers/ai_software_engineer.jpg',
  'Machine Learning Engineer': '/images/careers/machine_learning.jpg',
  'Software Engineer': '/images/careers/tech_software.jpg',
  'Web Developer': '/images/careers/tech_software.jpg',
  'Mobile App Developer': '/images/careers/tech_software.jpg',
  'Game Developer': '/images/careers/tech_software.jpg',
  'Frontend Developer': '/images/careers/tech_software.jpg',
  'Backend Developer': '/images/careers/tech_software.jpg',
  'Automation Engineer': '/images/careers/tech_cyber.jpg',
  'Robotics Engineer': '/images/careers/tech_cyber.jpg',
  'Data Scientist': '/images/careers/tech_data.jpg',
  'Data Analyst': '/images/careers/tech_data.jpg',
  'Data Visualization Specialist': '/images/careers/tech_data.jpg',
  'Cloud Database Engineer': '/images/careers/tech_cloud.jpg',
  'Cloud Consultant (Junior level)': '/images/careers/tech_cloud.jpg',
  'Product Manager (Entry-level)': '/images/careers/business_management.jpg',
  'Product Owner (Entry-level)': '/images/careers/business_management.jpg',
  'Scrum Master (Junior level)': '/images/careers/business_management.jpg',
  'Business Analyst': '/images/careers/business_analyst.jpg',
  'Business Intelligence Analyst': '/images/careers/business_analyst.jpg',
  'Financial Analyst': '/images/careers/business_finance.jpg',
  'Claims Adjuster': '/images/careers/business_finance.jpg',
  'Insurance Underwriter (Junior level)': '/images/careers/business_finance.jpg',
  'Digital Marketing Manager (Junior level)': '/images/careers/marketing_digital.jpg',
  'Digital Marketing Analyst': '/images/careers/marketing_digital.jpg',
  'Affiliate Marketing Manager (Junior level)': '/images/careers/marketing_digital.jpg',
  'Advertising Manager (Junior level)': '/images/careers/marketing_digital.jpg',
  'SEO Specialist': '/images/careers/marketing_digital.jpg',
  'SEM (Search Engine Marketing) Specialist': '/images/careers/marketing_digital.jpg',
  'Social Media Analyst': '/images/careers/marketing_digital.jpg',
  'Media Buyer': '/images/careers/marketing_digital.jpg',
  'Content Strategist': '/images/careers/content_creator.jpg',
  'UX/UI Designer': '/images/careers/design_ux.jpg',
  'UX Researcher': '/images/careers/design_ux.jpg',
  'Corporate Social Responsibility (CSR) Manager (Entry-level)': '/images/careers/government_civil.jpg',
  'Policy Advisor (Junior level)': '/images/careers/government_civil.jpg',
  'Legal Assistant': '/images/careers/business_finance.jpg',
};

const CATEGORY_IMAGE_MAP = {
  'AI & Data': '/images/careers/tech_data.jpg',
  'Software & Cloud': '/images/careers/tech_software.jpg',
  'Product & Operations': '/images/careers/business_management.jpg',
  'Marketing & Growth': '/images/careers/marketing_digital.jpg',
  'Business & Strategy': '/images/careers/business_finance.jpg',
  'Design & UX': '/images/careers/design_ux.jpg',
};

const CATEGORIES = ['All', 'AI & Data', 'Software & Cloud', 'Product & Operations', 'Marketing & Growth', 'Business & Strategy', 'Design & UX'];

function getRoleMeta(role) {
  const t = role.toLowerCase();
  let cat = 'Business & Strategy';
  let sal = [7, 16, 30];
  let growth = 'High';

  if (t.includes('ai ') || t.includes('machine learning') || t.includes('data') || t.includes('intelligence')) {
    cat = 'AI & Data';
    sal = (t.includes('researcher') || t.includes('scientist')) ? [12, 26, 45] : [9, 20, 38];
    growth = 'Very High';
  } else if (t.includes('design') || t.includes('ux') || t.includes('ui')) {
    cat = 'Design & UX';
    sal = [7, 16, 32];
    growth = 'High';
  } else if (t.includes('marketing') || t.includes('content') || t.includes('seo') || t.includes('sem') || t.includes('media') || t.includes('e-commerce') || t.includes('advertising') || t.includes('affiliate')) {
    cat = 'Marketing & Growth';
    sal = [6, 15, 28];
    growth = 'Growing';
  } else if (t.includes('product') || t.includes('scrum') || t.includes('operations') || t.includes('procurement') || t.includes('retail') || t.includes('franchise') || t.includes('quality')) {
    cat = 'Product & Operations';
    sal = t.includes('product') ? [12, 24, 44] : [8, 16, 30];
    growth = 'High';
  } else if (t.includes('software') || t.includes('developer') || t.includes('engineer') || t.includes('cloud') || t.includes('administrator') || t.includes('technical support') || t.includes('support analyst') || t.includes('sre') || t.includes('qa')) {
    cat = 'Software & Cloud';
    sal = [8, 18, 36];
    growth = 'Very High';
  } else {
    cat = 'Business & Strategy';
    sal = [7, 15, 28];
    growth = 'High';
  }

  const image = ROLE_IMAGE_MAP[role] || CATEGORY_IMAGE_MAP[cat] || CATEGORY_IMAGE_MAP['Software & Cloud'];
  return { cat, sal, growth, image };
}

// ── Interactive Salary Chart Tooltip ────────────────────────────────────────
const SalaryTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="salary-chart-tooltip">
        <div className="sct-label">{label} Experience</div>
        <div className="sct-val">
          <span className="sct-badge">₹{payload[0].value} LPA</span>
        </div>
        <div className="sct-sub">Estimated Annual CTC in India</div>
      </div>
    );
  }
  return null;
};

// ── Role Detail Modal ───────────────────────────────────────────────────────
function RoleModal({ role, onClose }) {
  const [salaryData, setSalaryData] = useState(null);
  const [roadmap, setRoadmap] = useState('');
  const [loading, setLoading] = useState(true);
  const meta = getRoleMeta(role);

  useEffect(() => {
    setLoading(true);
    // Fetch live salary from backend
    api.salaryInsights(role)
      .then(res => {
        if (res.data && Object.keys(res.data).length > 0) {
          const chartData = Object.entries(res.data).map(([level, [min, max]]) => ({
            name: level,
            avg: Math.round((min + max) / 2),
            min,
            max,
          }));
          setSalaryData(chartData);
        } else {
          // Fallback realistic salary projection
          setSalaryData([
            { name: 'Entry Level (0-2y)', avg: meta.sal[0], min: Math.max(3, meta.sal[0] - 2), max: meta.sal[0] + 3 },
            { name: 'Mid Level (3-5y)', avg: meta.sal[1], min: meta.sal[1] - 3, max: meta.sal[1] + 4 },
            { name: 'Senior (6-9y)', avg: meta.sal[2], min: meta.sal[2] - 4, max: meta.sal[2] + 7 },
            { name: 'Lead / Principal (10y+)', avg: Math.round(meta.sal[2] * 1.35), min: meta.sal[2], max: Math.round(meta.sal[2] * 1.6) },
          ]);
        }
      })
      .catch(() => {
        setSalaryData([
          { name: 'Entry Level (0-2y)', avg: meta.sal[0], min: meta.sal[0] - 2, max: meta.sal[0] + 2 },
          { name: 'Mid Level (3-5y)', avg: meta.sal[1], min: meta.sal[1] - 3, max: meta.sal[1] + 4 },
          { name: 'Senior (6-9y)', avg: meta.sal[2], min: meta.sal[2] - 4, max: meta.sal[2] + 7 },
        ]);
      })
      .finally(() => setLoading(false));

    api.roadmap(role)
      .then(res => setRoadmap(res.stages?.map(s => s.title || s).join(' → ') || ''))
      .catch(() => setRoadmap('Foundation & Fundamentals → Practical Projects & Internships → Specialized Skills → Senior Leadership'));
  }, [role]);

  const VIBRANT_BAR_COLORS = [
    { start: '#FF7A00', end: '#FF512F' }, // Neon Orange
    { start: '#C084FC', end: '#9333EA' }, // Vivid Purple
    { start: '#38BDF8', end: '#2563EB' }, // Electric Blue
    { start: '#34D399', end: '#059669' }, // Vibrant Emerald
  ];

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-box role-modal-box" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}><FiX /></button>

        {/* Modal Banner with Real Photo */}
        <div className="modal-photo-header">
          <img src={meta.image} alt={role} className="modal-header-img" />
          <div className="modal-header-gradient" />
          <div className="modal-header-content">
            <div className="modal-tag"><FiTrendingUp /> Trending in 2025</div>
            <h2 className="modal-role-title">{role}</h2>
            <div className="modal-role-meta">
              <span className="mrm-badge">{meta.cat}</span>
              <span className="mrm-dot">•</span>
              <span className="mrm-growth">{meta.growth} Career Growth</span>
            </div>
          </div>
        </div>

        <div className="modal-body">
          {/* Key Metrics Strip */}
          <div className="modal-stats-grid">
            <div className="ms-card">
              <div className="ms-icon icon-orange"><FiDollarSign /></div>
              <div>
                <div className="ms-val">₹{meta.sal[0]} – ₹{meta.sal[2]} LPA</div>
                <div className="ms-lbl">Expected Salary Range</div>
              </div>
            </div>
            <div className="ms-card">
              <div className="ms-icon icon-purple"><FiTrendingUp /></div>
              <div>
                <div className="ms-val">{meta.growth}</div>
                <div className="ms-lbl">Industry Demand</div>
              </div>
            </div>
            <div className="ms-card">
              <div className="ms-icon icon-blue"><FiAward /></div>
              <div>
                <div className="ms-val">{meta.cat}</div>
                <div className="ms-lbl">Primary Field</div>
              </div>
            </div>
          </div>

          {/* Interactive Salary Trend Section */}
          <div className="chart-interactive-card">
            <div className="cic-header">
              <div>
                <h4 className="cic-title"><FiBarChart2 /> Salary Progression Trend (₹ Lakhs per Annum)</h4>
                <p className="cic-sub">Interactive compensation by experience level based on Indian market data</p>
              </div>
              <div className="cic-badge">Live Market Benchmarks</div>
            </div>

            {loading ? (
              <div className="spinner" />
            ) : (
              <div className="cic-chart-wrap">
                <ResponsiveContainer width="100%" height={260}>
                  <BarChart data={salaryData} margin={{ top: 20, right: 20, left: -10, bottom: 5 }}>
                    <defs>
                      {VIBRANT_BAR_COLORS.map((col, idx) => (
                        <linearGradient key={idx} id={`barGrad${idx}`} x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor={col.start} stopOpacity={1} />
                          <stop offset="100%" stopColor={col.end} stopOpacity={0.8} />
                        </linearGradient>
                      ))}
                    </defs>
                    <CartesianGrid vertical={false} stroke="rgba(255, 255, 255, 0.05)" />
                    <XAxis
                      dataKey="name"
                      stroke="#8B89A8"
                      tick={{ fill: '#A09EB8', fontSize: 12, fontWeight: 500 }}
                      axisLine={{ stroke: 'rgba(255, 255, 255, 0.1)' }}
                      tickLine={false}
                    />
                    <YAxis
                      stroke="#8B89A8"
                      tick={{ fill: '#A09EB8', fontSize: 12 }}
                      axisLine={false}
                      tickLine={false}
                      tickFormatter={val => `₹${val}L`}
                    />
                    <Tooltip content={<SalaryTooltip />} cursor={{ fill: 'rgba(255, 255, 255, 0.04)' }} />
                    <Bar dataKey="avg" radius={[8, 8, 2, 2]} maxBarSize={55} animationDuration={1000}>
                      {salaryData?.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={`url(#barGrad${index % VIBRANT_BAR_COLORS.length})`} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>

                {/* Level chips showing min-max */}
                <div className="salary-pill-breakdown">
                  {salaryData?.map((item, idx) => (
                    <div key={idx} className="sp-card">
                      <div className="sp-level">{item.name.split(' ')[0]}</div>
                      <div className="sp-avg" style={{ color: VIBRANT_BAR_COLORS[idx % VIBRANT_BAR_COLORS.length].start }}>
                        ₹{item.avg} LPA
                      </div>
                      <div className="sp-range">{item.min && item.max ? `₹${item.min}L - ₹${item.max}L` : 'Average'}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Career Path Roadmap */}
          {roadmap && (
            <div className="roadmap-card">
              <h4 className="rc-heading"><FiMap /> Recommended Career Milestones</h4>
              <div className="roadmap-flow">
                {roadmap.split(' → ').map((step, i) => (
                  <React.Fragment key={i}>
                    <div className="rf-step">
                      <div className="rf-number">{i + 1}</div>
                      <div className="rf-text">{step}</div>
                    </div>
                    {i < roadmap.split(' → ').length - 1 && <div className="rf-arrow">➔</div>}
                  </React.Fragment>
                ))}
              </div>
            </div>
          )}

          {/* Modal Action CTA */}
          <div className="modal-footer-actions">
            <a href="/tools" className="btn-primary" style={{ textDecoration: 'none', justifyContent: 'center' }}>
              <FiBookOpen /> Open Tools for {role}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Main Explore Page ──────────────────────────────────────────────────────
export default function Explore() {
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [activeCategory, setActiveCategory] = useState('All');
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    api.getInit()
      .then(d => {
        setRoles(d.roles || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    return roles.filter(r => {
      const matchSearch = r.toLowerCase().includes(search.toLowerCase());
      if (activeCategory === 'All') return matchSearch;
      return matchSearch && getRoleMeta(r).cat === activeCategory;
    });
  }, [roles, search, activeCategory]);

  return (
    <div className="explore-page page-wrap" style={{ paddingTop: '100px' }}>
      {/* Header Banner */}
      <div className="exp-header fade-up">
        <div className="eyebrow">CAREER DIRECTORY</div>
        <h1 className="exp-h1">
          Explore Real Careers<br />
          <span className="grad-text">With Live Insights & Salaries</span>
        </h1>
        <p className="exp-sub">
          Discover {roles.length || '54'} curated professions with real photographic previews, live compensation trends, growth prospects, and learning roadmaps.
        </p>
      </div>

      {/* Category Pills Bar */}
      <div className="cat-pills fade-up">
        {CATEGORIES.map(c => (
          <button
            key={c}
            className={`cat-pill ${activeCategory === c ? 'active' : ''}`}
            onClick={() => setActiveCategory(c)}
          >
            {c}
          </button>
        ))}
      </div>

      {/* Search Bar */}
      <div className="exp-search glass-card fade-up">
        <FiSearch className="exp-search-icon" />
        <input
          placeholder="Search careers (e.g., Data Scientist, AI Researcher, Product Manager...)"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        {search && (
          <button className="clear-search-btn" onClick={() => setSearch('')}>
            <FiX />
          </button>
        )}
        <button className="btn-primary" onClick={() => {}}>Search</button>
      </div>

      <div className="exp-count fade-up">
        Showing <strong>{filtered.length}</strong> of <strong>{roles.length}</strong> careers
      </div>

      {/* Career Cards Grid with Real Photography */}
      {loading ? (
        <div className="spinner" />
      ) : (
        <div className="roles-grid fade-up">
          {filtered.length === 0 ? (
            <div className="no-results">
              <h3>No careers found matching "{search}"</h3>
              <p>Try searching for a different job title or pick "All" categories.</p>
            </div>
          ) : filtered.map((role, idx) => {
            const meta = getRoleMeta(role);
            return (
              <div
                key={idx}
                className="role-card"
                onClick={() => setSelected(role)}
                style={{ animationDelay: `${(idx % 12) * 0.04}s` }}
              >
                {/* Photo Top with gradient overlay */}
                <div className="rc-img-container">
                  <img src={meta.image} alt={role} className="rc-photo" loading="lazy" />
                  <div className="rc-photo-overlay" />
                  <div className="rc-trending-tag">
                    <FiTrendingUp /> Trending
                  </div>
                  <div className="rc-domain-badge">{meta.cat}</div>
                </div>

                {/* Card Body */}
                <div className="rc-body">
                  <h3 className="rc-title">{role}</h3>
                  <p className="rc-desc">
                    Comprehensive compensation trends, verified skill requirements, and stage-by-stage progression.
                  </p>

                  <div className="rc-tags">
                    <span className="tag purple">{meta.growth} Growth</span>
                    <span className="tag blue">In Demand</span>
                  </div>

                  <div className="rc-footer">
                    <div>
                      <div className="rc-sal-lbl">Avg Salary</div>
                      <div className="rc-sal">₹{meta.sal[0]}–{meta.sal[2]} LPA</div>
                    </div>
                    <button className="rc-action-btn" title="View details & salary chart">
                      <FiArrowRight />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Role Details Modal */}
      {selected && <RoleModal role={selected} onClose={() => setSelected(null)} />}
    </div>
  );
}
