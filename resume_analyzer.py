import pdfplumber

def extract_resume_text(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text, target_role=None):
    role_context = f" for a {target_role} role" if target_role else ""

    prompt = f"""You are an experienced career coach and resume reviewer.
Analyze the following resume{role_context} and give clear, structured feedback.

Resume:
{resume_text}

Give your feedback in this exact format:

**Strengths:**
- (2-4 bullet points)

**Areas to Improve:**
- (2-4 bullet points)

**Missing Elements:**
- (things a strong resume in this field usually has but this one lacks)

**Overall Score:** X/10

Keep it concise, specific to the actual content of this resume, and actionable."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    with open("test_resume.pdf", "rb") as f:
        text = extract_resume_text(f)
        print(f"Extracted {len(text)} characters\n")

        feedback = analyze_resume(text, target_role="Frontend Developer")
        print(feedback)