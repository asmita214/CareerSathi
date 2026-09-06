import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def compare_careers(role1, role2, index, chunks, retrieve_fn):
    q1 = f"What does a {role1} do, what skills are needed, and what is the career growth?"
    q2 = f"What does a {role2} do, what skills are needed, and what is the career growth?"

    chunks1 = retrieve_fn(q1, index, chunks, top_k=3)
    chunks2 = retrieve_fn(q2, index, chunks, top_k=3)
    context1 = "\n".join([c["text"] for c in chunks1])
    context2 = "\n".join([c["text"] for c in chunks2])

    prompt = f"""Compare these two careers for a student deciding between them.

{role1} — relevant info:
{context1}

{role2} — relevant info:
{context2}

Format exactly as:

**{role1}**
- Core skills:
- Responsibilities:
- Growth path:

**{role2}**
- Core skills:
- Responsibilities:
- Growth path:

**Which one might suit you better?**
(2-3 sentences of balanced, practical guidance)"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content