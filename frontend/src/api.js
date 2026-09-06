const BASE = import.meta.env.VITE_API_URL || '/api';

export const api = {
  async getInit() {
    const res = await fetch(`${BASE}/init`);
    if (!res.ok) throw new Error('Backend offline');
    return res.json();
  },

  async chat(query) {
    const res = await fetch(`${BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query }),
    });
    if (!res.ok) throw new Error('Chat failed');
    return res.json();
  },

  async compare(role1, role2) {
    const res = await fetch(`${BASE}/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role1, role2 }),
    });
    if (!res.ok) throw new Error('Compare failed');
    return res.json();
  },

  async roadmap(role) {
    const res = await fetch(`${BASE}/roadmap`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role }),
    });
    if (!res.ok) throw new Error('Roadmap failed');
    return res.json();
  },

  async salaryInsights(role) {
    const res = await fetch(`${BASE}/salary-insights`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role }),
    });
    if (!res.ok) throw new Error('Salary failed');
    return res.json();
  },

  async datasetInsights() {
    const res = await fetch(`${BASE}/dataset-insights`);
    if (!res.ok) throw new Error('Dataset failed');
    return res.json();
  },

  async interviewPrep(role) {
    const res = await fetch(`${BASE}/interview-prep`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role }),
    });
    if (!res.ok) throw new Error('Interview prep failed');
    return res.json();
  },

  async learningResources(role) {
    const res = await fetch(`${BASE}/learning-resources`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role }),
    });
    if (!res.ok) throw new Error('Learning resources failed');
    return res.json();
  },

  async skillQuiz(role, ratings) {
    const res = await fetch(`${BASE}/skill-quiz`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role, ratings }),
    });
    if (!res.ok) throw new Error('Skill quiz failed');
    return res.json();
  },

  async getSkills(role) {
    const res = await fetch(`${BASE}/skills?role=${encodeURIComponent(role)}`);
    if (!res.ok) throw new Error('Skills failed');
    return res.json();
  },

  async interestQuiz(answers) {
    const res = await fetch(`${BASE}/interest-quiz`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ answers }),
    });
    if (!res.ok) throw new Error('Interest quiz failed');
    return res.json();
  },

  async resumeFeedback(file, targetRole) {
    const form = new FormData();
    form.append('file', file);
    if (targetRole) form.append('target_role', targetRole);
    const res = await fetch(`${BASE}/resume-feedback`, { method: 'POST', body: form });
    if (!res.ok) throw new Error('Resume feedback failed');
    return res.json();
  },

  async atsMatch(file, role) {
    const form = new FormData();
    form.append('file', file);
    form.append('role', role);
    const res = await fetch(`${BASE}/ats-match`, { method: 'POST', body: form });
    if (!res.ok) throw new Error('ATS match failed');
    return res.json();
  },

  async similarityMap() {
    const res = await fetch(`${BASE}/similarity-map`);
    if (!res.ok) throw new Error('Similarity map failed');
    return res.json();
  },
};
