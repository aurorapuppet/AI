from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="AI Q&A Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str

class RatingRequest(BaseModel):
    question_id: int
    rating: int  # 1-5
    feedback: str = None

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(req: AskRequest):
    """
    直接问答模式：提问 → 存储问题向量 → 调用 LLM → 存储问题-答案对 → 返回答案
    """
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    from .embedding import embed_single
    from .rag import ask_direct
    from .db import SessionLocal, create_tables
    from .models import Question
    
    create_tables()
    db = SessionLocal()
    try:
        # 1. 生成问题向量
        question_embedding = embed_single(question)
        
        # 2. 调用 LLM 生成答案
        result = ask_direct(question)
        
        if result['success']:
            # 3. 存储问题-答案对到数据库
            q_record = Question(
                question_text=question,
                question_embedding=question_embedding,
                answer_text=result['answer'],
                llm_provider=result['llm_provider'],
                metadata={}
            )
            db.add(q_record)
            db.commit()
            
            return {
                "id": q_record.id,
                "question": question,
                "answer": result['answer'],
                "llm_provider": result['llm_provider']
            }
        else:
            raise HTTPException(status_code=500, detail=result.get('error', 'Unknown error'))
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@app.get("/questions")
async def list_questions(skip: int = 0, limit: int = 20):
    """
    列出问答历史
    """
    from .db import SessionLocal, create_tables
    from .models import Question
    
    create_tables()
    db = SessionLocal()
    try:
        questions = db.query(Question).order_by(Question.created_at.desc()).offset(skip).limit(limit).all()
        return [
            {
                "id": q.id,
                "question": q.question_text,
                "answer": q.answer_text,
                "rating": q.rating,
                "feedback": q.feedback,
                "llm_provider": q.llm_provider,
                "created_at": q.created_at.isoformat()
            }
            for q in questions
        ]
    finally:
        db.close()


@app.get("/questions/{question_id}")
async def get_question(question_id: int):
    """
    获取单个问答记录
    """
    from .db import SessionLocal, create_tables
    from .models import Question
    
    create_tables()
    db = SessionLocal()
    try:
        q = db.query(Question).filter(Question.id == question_id).first()
        if not q:
            raise HTTPException(status_code=404, detail="Question not found")
        return {
            "id": q.id,
            "question": q.question_text,
            "answer": q.answer_text,
            "rating": q.rating,
            "feedback": q.feedback,
            "llm_provider": q.llm_provider,
            "created_at": q.created_at.isoformat()
        }
    finally:
        db.close()


@app.post("/questions/{question_id}/rate")
async def rate_answer(question_id: int, req: RatingRequest):
    """
    为答案评分/反馈
    """
    from .db import SessionLocal, create_tables
    from .models import Question
    
    create_tables()
    db = SessionLocal()
    try:
        q = db.query(Question).filter(Question.id == question_id).first()
        if not q:
            raise HTTPException(status_code=404, detail="Question not found")
        
        q.rating = req.rating
        q.feedback = req.feedback
        db.commit()
        
        return {
            "id": q.id,
            "rating": q.rating,
            "feedback": q.feedback,
            "message": "Rating saved successfully"
        }
    finally:
        db.close()


@app.delete("/questions/{question_id}")
async def delete_question(question_id: int):
    """
    删除问答记录
    """
    from .db import SessionLocal, create_tables
    from .models import Question
    
    create_tables()
    db = SessionLocal()
    try:
        q = db.query(Question).filter(Question.id == question_id).first()
        if not q:
            raise HTTPException(status_code=404, detail="Question not found")
        
        db.delete(q)
        db.commit()
        
        return {"message": "Question deleted successfully"}
    finally:
        db.close()
