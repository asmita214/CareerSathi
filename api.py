from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import io

# Import existing backend modules
from analytics import dataset_stats, role_embedding_similarity, ats_match_score
from rag_engine import load_index, retrieve, generate_answer
from resume_analyzer import extract_resume_text, analyze_resume
from skill_quiz import get_skills_for_role, generate_roadmap, ROLE_SKILLS
from career_compare import compare_careers
from career_roadmap import generate_roadmap_stages, parse_roadmap
from interview_prep import generate_interview_questions
from learning_resources import generate_learning_resources
from career_quiz import INTEREST_QUESTIONS, recommend_careers
from salary_data import SALARY_DATA, NOTE as SALARY_NOTE

app = FastAPI(title="CareerSaathi API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load index and chunks at startup
index, chunks = load_index()
ALL_ROLES = sorted(list(set(c["role"] for c in chunks)))

class ChatRequest(BaseModel):
    query: str

class CompareRequest(BaseModel):
    role1: str
    role2: str

class RoadmapRequest(BaseModel):
    role: str

class SkillQuizRequest(BaseModel):
    role: str
    ratings: Dict[str, int]

class InterestQuizRequest(BaseModel):
    answers: List[str]

class RoleRequest(BaseModel):
    role: str

@app.get("/api/init")
def get_init_data():
    return {
        "roles": ALL_ROLES,
        "salary_roles": list(SALARY_DATA.keys()),
        "quiz_roles": list(ROLE_SKILLS.keys()),
        "interest_questions": INTEREST_QUESTIONS
    }

@app.post("/api/chat")
def chat(req: ChatRequest):
    retrieved = retrieve(req.query, index, chunks)
    answer = generate_answer(req.query, retrieved)
    sources = sorted(list(set(c["role"] for c in retrieved)))
    return {"answer": answer, "sources": sources}

@app.post("/api/compare")
def compare(req: CompareRequest):
    if req.role1 == req.role2:
        raise HTTPException(status_code=400, detail="Roles must be different")
    result = compare_careers(req.role1, req.role2, index, chunks, retrieve)
    return {"comparison": result}

@app.post("/api/roadmap")
def roadmap(req: RoadmapRequest):
    raw = generate_roadmap_stages(req.role)
    stages = parse_roadmap(raw)
    return {"stages": stages}

@app.post("/api/resume-feedback")
async def resume_feedback(
    target_role: Optional[str] = Form(None),
    file: UploadFile = File(...)
):
    content = await file.read()
    # Mocking file object for pdfplumber
    file_like = io.BytesIO(content)
    file_like.name = file.filename
    
    resume_text = extract_resume_text(file_like)
    if len(resume_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Couldn't extract enough text from PDF.")
    
    feedback = analyze_resume(resume_text, target_role)
    return {"feedback": feedback}

@app.post("/api/ats-match")
async def ats_match(
    role: str = Form(...),
    file: UploadFile = File(...)
):
    content = await file.read()
    file_like = io.BytesIO(content)
    file_like.name = file.filename
    
    resume_text = extract_resume_text(file_like)
    extra_kw = ROLE_SKILLS.get(role, [])
    result = ats_match_score(resume_text, role, chunks, extra_keywords=extra_kw)
    return result

@app.get("/api/dataset-insights")
def dataset_insights():
    role_counts, word_counter = dataset_stats(chunks)
    return {
        "role_counts": dict(role_counts.most_common(15)),
        "word_counts": dict(word_counter.most_common(20))
    }

@app.get("/api/similarity-map")
def similarity_map():
    roles, sim_matrix = role_embedding_similarity(index, chunks)
    return {"roles": roles, "sim_matrix": sim_matrix.tolist()}

@app.post("/api/skill-quiz")
def skill_quiz(req: SkillQuizRequest):
    roadmap_text = generate_roadmap(req.role, req.ratings)
    return {"roadmap": roadmap_text}

@app.get("/api/skills")
def get_skills(role: str):
    skills = get_skills_for_role(role)
    return {"skills": skills}

@app.post("/api/interest-quiz")
def interest_quiz(req: InterestQuizRequest):
    result = recommend_careers(req.answers, ALL_ROLES)
    return {"recommendation": result}

@app.post("/api/interview-prep")
def interview_prep(req: RoleRequest):
    result = generate_interview_questions(req.role)
    return {"prep": result}

@app.post("/api/learning-resources")
def learning_resources(req: RoleRequest):
    result = generate_learning_resources(req.role)
    return {"resources": result}

@app.post("/api/salary-insights")
def salary_insights(req: RoleRequest):
    data = SALARY_DATA.get(req.role, {})
    return {"data": data, "note": SALARY_NOTE}
