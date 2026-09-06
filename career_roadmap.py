import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_roadmap_stages(role):
    prompt = f"""Give a career roadmap for becoming a {role}, structured in exactly 3 stages.
Format strictly as:

STAGE: Entry-Level (0-2 years)
FOCUS: (one sentence)
SKILLS: (comma-separated list of 3-4 skills to build)

STAGE: Mid-Level (2-5 years)
FOCUS: (one sentence)
SKILLS: (comma-separated list of 3-4 skills to build)

STAGE: Senior-Level (5+ years)
FOCUS: (one sentence)
SKILLS: (comma-separated list of 3-4 skills to build)

Do not add any extra text outside this format."""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content


def parse_roadmap(raw_text):
    stages = []
    blocks = raw_text.split("STAGE:")[1:]
    for block in blocks:
        lines = block.strip().split("\n")
        title = lines[0].strip()
        focus, skills = "", ""
        for line in lines[1:]:
            if line.startswith("FOCUS:"):
                focus = line.replace("FOCUS:", "").strip()
            elif line.startswith("SKILLS:"):
                skills = line.replace("SKILLS:", "").strip()
        stages.append({"title": title, "focus": focus, "skills": skills})
    return stages