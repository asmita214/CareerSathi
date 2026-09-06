import React from 'react';

const RES = [
  { cat: '📝 Resume Guides', items: ['How to format an ATS-friendly resume', 'Writing strong bullet points with STAR method', 'Tailoring your resume for each role'] },
  { cat: '🎤 Interview Prep Platforms', items: ['Pramp (free mock interviews)', 'Interviewing.io', 'LeetCode (technical rounds)'] },
  { cat: '🏛️ Government Career Portals', items: ['National Career Service (NCS) Portal', 'UPSC official website', 'State PSC websites'] },
  { cat: '🎓 Skill Certifications', items: ['Coursera', 'NPTEL', 'edX', 'Google Career Certificates'] },
  { cat: '▶️ YouTube & LinkedIn Learning', items: ['LinkedIn Learning (1 month free trial)', 'Google Activate on YouTube', 'Kurzgesagt for big-picture career thinking'] },
];

const FAQS = [
  ['How do I ask questions on CareerSaathi?', 'Go to Tools → Ask CareerSaathi. Type your question in English or Hindi.'],
  ['Which languages are supported?', 'English and Hindi are fully supported via multilingual sentence-transformer embeddings.'],
  ['How does resume feedback work?', 'You upload a PDF. The text is extracted using pdfplumber and sent to the AI model which gives structured feedback.'],
  ['Is my uploaded data stored?', 'No. PDFs are processed in-memory and immediately discarded. Nothing is persisted on the server.'],
];

const GLOSSARY = [
  ['ATS', 'Applicant Tracking System — software that filters resumes before they reach humans.'],
  ['CTC', 'Cost to Company — the total annual salary including base pay, bonuses, and perks.'],
  ['Notice Period', 'Time between resignation and your last working day (typically 1–3 months).'],
  ['ROI', 'Return on Investment — value gained vs cost of education/training.'],
  ['ESOP', 'Employee Stock Ownership Plan — company stock awarded to employees.'],
  ['LPA', 'Lakhs Per Annum — Indian salary denomination (1 LPA = ₹1,00,000/year).'],
];

export default function Resources() {
  return (
    <div className="page-wrap fade-up" style={{ paddingTop: '100px' }}>
      <div className="eyebrow">RESOURCES</div>
      <h1 style={{ fontFamily:'Playfair Display,serif', fontSize:'clamp(2rem,3.5vw,3rem)', marginBottom:'0.8rem' }}>
        Resources <span className="grad-text">Hub</span>
      </h1>
      <p style={{ color:'var(--text-muted)', marginBottom:'2.5rem', maxWidth:560, lineHeight:1.7 }}>
        Curated guides, tools, and references for your career journey.
      </p>

      {/* Resources */}
      <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(320px,1fr))', gap:'1.2rem', marginBottom:'2.5rem' }}>
        {RES.map(({ cat, items }) => (
          <div key={cat} className="glass-card" style={{ padding:'1.3rem' }}>
            <h3 style={{ fontFamily:'Inter,sans-serif', fontSize:'0.95rem', marginBottom:'0.8rem', color:'var(--text)' }}>{cat}</h3>
            <ul style={{ display:'flex', flexDirection:'column', gap:'0.5rem' }}>
              {items.map(it => (
                <li key={it} style={{ fontSize:'0.85rem', color:'var(--text-muted)', display:'flex', gap:'0.5rem' }}>
                  <span style={{ color:'var(--accent)', flexShrink:0 }}>›</span> {it}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      {/* FAQ */}
      <h2 style={{ fontFamily:'Playfair Display,serif', fontSize:'1.6rem', marginBottom:'1.2rem' }}>
        Frequently Asked <span className="grad-text">Questions</span>
      </h2>
      <div style={{ display:'flex', flexDirection:'column', gap:'0.8rem', marginBottom:'2.5rem' }}>
        {FAQS.map(([q, a]) => (
          <details key={q} className="glass-card" style={{ padding:'1.2rem', cursor:'pointer' }}>
            <summary style={{ fontWeight:600, fontSize:'0.95rem', listStyle:'none', display:'flex', justifyContent:'space-between' }}>
              {q} <span style={{ color:'var(--accent)' }}>+</span>
            </summary>
            <p style={{ marginTop:'0.8rem', color:'var(--text-muted)', fontSize:'0.88rem', lineHeight:1.7 }}>{a}</p>
          </details>
        ))}
      </div>

      {/* Glossary */}
      <h2 style={{ fontFamily:'Playfair Display,serif', fontSize:'1.6rem', marginBottom:'1.2rem' }}>
        Career <span className="grad-text">Glossary</span>
      </h2>
      <div style={{ display:'grid', gridTemplateColumns:'repeat(auto-fill,minmax(280px,1fr))', gap:'1rem' }}>
        {GLOSSARY.map(([term, def]) => (
          <div key={term} className="glass-card" style={{ padding:'1.1rem' }}>
            <div style={{ fontWeight:700, fontSize:'1rem', color:'#F08A5D', marginBottom:'0.4rem' }}>{term}</div>
            <div style={{ fontSize:'0.84rem', color:'var(--text-muted)', lineHeight:1.6 }}>{def}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
