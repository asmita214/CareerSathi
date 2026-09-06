import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

INTEREST_QUESTIONS = [
    {"q": "What kind of work energizes you most?",
     "options": ["Solving analytical/logical problems", "Creating visual or creative designs", "Talking to and persuading people", "Organizing plans and processes"]},
    {"q": "Which environment do you prefer?",
     "options": ["Working deeply focused alone with data/code", "Collaborating closely in a team", "Leading and coordinating others", "A mix of independent and team work"]},
    {"q": "What matters most to you in a career?",
     "options": ["Intellectual challenge", "Creative expression", "Impact on people/business", "Stability and structure"]},
    {"q": "Pick a task you'd enjoy:",
     "options": ["Analyzing a dataset to find patterns", "Designing a beautiful app screen", "Pitching an idea to stakeholders", "Planning a project timeline"]},
]

def recommend_careers(answers, available_roles):
    answers_text = "\n".join([f"- {a}" for a in answers])
    roles_text = ", ".join(available_roles)
    prompt = f"""A student answered a career-interest quiz as follows:
{answers_text}

From this list of available career roles: {roles_text}

Recommend the TOP 3 roles from this exact list that best match their interests.
Format as:

**1. [Role Name]** - (1 sentence why it fits)
**2. [Role Name]** - (1 sentence why it fits)
**3. [Role Name]** - (1 sentence why it fits)

Only choose roles from the given list."""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content