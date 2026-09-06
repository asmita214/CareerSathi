import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# A small set of core skills per role — used to build the quiz questions
ROLE_SKILLS = {
    "Data Scientist": ["Python", "Statistics", "Machine Learning", "SQL", "Data Visualization"],
    "Software Engineer": ["Data Structures & Algorithms", "System Design", "Version Control (Git)", "OOP", "Testing/Debugging"],
    "Product Manager": ["Market Research", "Roadmapping", "Stakeholder Communication", "Data-Driven Decision Making", "Wireframing/Prototyping"],
    "UX Designer": ["User Research", "Wireframing", "Prototyping Tools (Figma)", "Visual Design", "Usability Testing"],
    "Marketing Manager": ["Content Strategy", "SEO/SEM", "Analytics Tools", "Campaign Management", "Brand Positioning"],
    "Business Analyst": ["Requirement Gathering", "SQL", "Data Analysis", "Process Mapping", "Stakeholder Communication"],
}

def get_skills_for_role(role):
    return ROLE_SKILLS.get(role, ["Communication", "Domain Knowledge", "Problem Solving", "Tools Proficiency", "Adaptability"])

def generate_roadmap(role, skill_ratings):
    """
    skill_ratings: dict like {"Python": 3, "Statistics": 2, ...} on a 1-5 scale
    """
    ratings_text = "\n".join([f"- {skill}: {rating}/5" for skill, rating in skill_ratings.items()])

    prompt = f"""You are a career mentor. A user wants to become a {role}.
They rated their current skill level (1=beginner, 5=expert) as follows:

{ratings_text}

Based on this, give a personalized learning roadmap in this format:

**Your Skill Gap Summary:**
(1-2 sentences on their overall readiness)

**Priority Areas (weakest skills first):**
- List 2-3 skills to focus on, with one specific, actionable suggestion for each (a type of resource, project idea, or practice method — no need for exact course names)

**You're Already Strong In:**
- List their highest-rated skills briefly

**Suggested Next Step:**
(One concrete action they can take this week)

Keep it encouraging, specific, and concise."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    role = "Data Scientist"
    skills = get_skills_for_role(role)
    print("Skills to rate:", skills)

    # simulate ratings for testing
    test_ratings = {skill: 3 for skill in skills}
    roadmap = generate_roadmap(role, test_ratings)
    print("\n" + roadmap)