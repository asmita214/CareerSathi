import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_interview_questions(role):
    prompt = f"""Generate 5 common interview questions for a {role} position, each with a brief
sample-answer approach (guidance on what to cover, not a scripted answer).

Format as:
Q1: ...
A1: ...

Q2: ...
A2: ...

(continue through Q5/A5)"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content