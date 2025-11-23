from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json
import os

# Import our new modules
from .llm_client import generate_response
from .prompts import (
    SYSTEM_PROMPT_TEMPLATE, 
    NEXT_QUESTION_PROMPT, 
    INITIAL_QUESTION_PROMPT, 
    FEEDBACK_PROMPT
)
from .resume_parser import parse_resume

app = FastAPI(title="Interview Practice Partner API")

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount frontend directory
app.mount("/app", StaticFiles(directory="frontend", html=True), name="frontend")

# In-memory session store
sessions = {}

class StartSessionRequest(BaseModel):
    role: str
    experience_level: str = "Junior"
    resume_text: Optional[str] = None

class ChatRequest(BaseModel):
    session_id: str
    user_message: str

class ChatResponse(BaseModel):
    agent_message: str
    is_interview_over: bool = False

class FeedbackResponse(BaseModel):
    feedback: dict

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Interview Partner Backend is running"}

# --- Resume Handling ---
@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()
    resume_text = parse_resume(content, file.filename)
    return {"resume_text": resume_text}

@app.post("/start_session")
def start_session(request: StartSessionRequest):
    session_id = str(uuid.uuid4())
    
    # Store resume text if provided
    resume_context = request.resume_text or ""
    
    sessions[session_id] = {
        "role": request.role,
        "experience_level": request.experience_level,
        "resume_text": resume_context,
        "history": [],
        "question_count": 0,
        "max_questions": 15,
        "is_over": False
    }
    
    # Generate initial greeting/question using LLM
    resume_prompt_part = f"\nCandidate Resume:\n{resume_context}\n" if resume_context else ""
    
    system_instruction = SYSTEM_PROMPT_TEMPLATE.format(
        role=request.role,
        experience_level=request.experience_level,
        current_question_num=1,
        max_questions=15
    ) + resume_prompt_part
    
    initial_message = generate_response(INITIAL_QUESTION_PROMPT.format(role=request.role), system_instruction=system_instruction)
    
    sessions[session_id]["history"].append({"role": "model", "content": initial_message})
    
    return {"session_id": session_id, "initial_message": initial_message}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id = request.session_id
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    if session["is_over"]:
        return ChatResponse(agent_message="The interview is already over. Please request feedback.", is_interview_over=True)

    # Record user message
    session["history"].append({"role": "user", "content": request.user_message})
    
    # Detect persona
    from .persona_logic import detect_persona, get_persona_instruction
    persona = detect_persona(request.user_message, session["history"])
    persona_instruction = get_persona_instruction(persona)
    
    # Prepare context for LLM
    conversation_history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in session["history"]])
    
    session["question_count"] += 1
    
    # Check if we should end the interview
    if session["question_count"] >= session["max_questions"]:
        session["is_over"] = True
        response_text = "Thank you for your time today. That covers all the questions I had planned. Let me now provide you with detailed feedback on your performance."
        session["history"].append({"role": "model", "content": response_text})
        return ChatResponse(agent_message=response_text, is_interview_over=True)
    
    # Generate next question with persona awareness
    resume_context = session.get("resume_text", "")
    resume_prompt_part = f"\nCandidate Resume:\n{resume_context}\n" if resume_context else ""

    system_instruction = SYSTEM_PROMPT_TEMPLATE.format(
        role=session["role"],
        experience_level=session["experience_level"],
        current_question_num=session["question_count"] + 1,
        max_questions=session["max_questions"]
    ) + resume_prompt_part + f"\n\nDETECTED PERSONA: {persona.upper()}\n{persona_instruction}"
    
    prompt = NEXT_QUESTION_PROMPT.format(conversation_history=conversation_history_str)
    response_text = generate_response(prompt, system_instruction=system_instruction)
    
    session["history"].append({"role": "model", "content": response_text})
    
    return ChatResponse(agent_message=response_text, is_interview_over=False)

@app.post("/feedback", response_model=FeedbackResponse)
def get_feedback(request: ChatRequest):
    session_id = request.session_id
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[session_id]
    
    conversation_history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in session["history"]])
    
    prompt = FEEDBACK_PROMPT.format(conversation_history=conversation_history_str)
    
    feedback_text = generate_response(prompt)
    
    # Return as plain text in a simple dict
    return FeedbackResponse(feedback={"spoken_feedback": feedback_text})
