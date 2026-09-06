import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_learning_resources(role):
    prompt = f"""Suggest learning resources for someone pursuing a career as a {role}.
Do NOT invent specific URLs. Recommend resource TYPES and well-known platform names only
(e.g., "Coursera", "YouTube channels covering X", "freeCodeCamp", "official docs of Y",
"practice on LeetCode/Kaggle" etc.).

Format as:
**Free Resources:**
- ...

**Paid/Certification Options:**
- ...

**Practice Platforms:**
- ...

Keep it concise (2-3 bullets per section)."""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content