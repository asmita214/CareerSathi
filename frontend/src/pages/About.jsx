import React from 'react';

export default function About() {
  return (
    <div className="page-wrap fade-up" style={{ paddingTop: '100px' }}>
      <div className="eyebrow">ABOUT</div>
      <h1 style={{ fontFamily:'Playfair Display,serif', fontSize:'clamp(2rem,3.5vw,3rem)', marginBottom:'0.8rem' }}>
        About <span className="grad-text">CareerSaathi</span>
      </h1>
      <p style={{ color:'var(--text-muted)', marginBottom:'2.5rem', maxWidth:600, lineHeight:1.7 }}>
        How this platform works, and who built it.
      </p>

      {[
        { title: 'What is CareerSaathi?', body: 'CareerSaathi is an AI-powered bilingual career guidance platform designed to solve the problem of fragmented, English-only, and unreliable career information. Get personalized guidance in English or हिंदी.' },
        { title: 'How It Works (RAG Pipeline)', body: '1. A dataset of 1,620 career Q&A pairs is converted into vector embeddings using a multilingual sentence-transformer model.\n2. These embeddings are indexed in FAISS for lightning-fast similarity search.\n3. When you ask a question, it\'s embedded the same way, and the most relevant chunks are retrieved.\n4. Those chunks are passed to Llama 3.3 70B (via Groq) to generate a grounded, natural answer — in the same language you asked in.' },
        { title: 'Tech Stack', body: 'Frontend: React, Vite, Vanilla CSS, Recharts\nBackend: Python, FastAPI, Uvicorn\nAI & Data: Sentence-Transformers (multilingual), FAISS, Groq API (Llama 3.3 70B), pdfplumber, Plotly' },
        { title: 'Dataset', body: '1,620 Q&A pairs across 50+ career roles — sourced from Hugging Face. Covers skills, salaries, growth paths, interview tips, and more.' },
        { title: 'Limitations', body: 'Salary data is approximate and illustrative. This platform is an AI assistant, not a replacement for professional career counseling or placement services.' },
      ].map(({ title, body }) => (
        <div key={title} className="glass-card" style={{ marginBottom:'1.2rem', padding:'1.5rem' }}>
          <h3 style={{ fontFamily:'Inter,sans-serif', fontSize:'1.05rem', marginBottom:'0.8rem', color:'var(--text)' }}>{title}</h3>
          <p style={{ color:'var(--text-muted)', lineHeight:1.8, fontSize:'0.92rem', whiteSpace:'pre-line' }}>{body}</p>
        </div>
      ))}
    </div>
  );
}
