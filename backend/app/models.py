from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from datetime import datetime
from .db import Base


class Question(Base):
    """用户问题及其答案存储"""
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_embedding = Column(ARRAY(Float), nullable=True)
    answer_text = Column(Text, nullable=False)
    llm_provider = Column(String, default='openai')  # 记录使用的 LLM
    rating = Column(Integer, nullable=True)  # 用户评分（1-5）
    feedback = Column(Text, nullable=True)  # 用户反馈
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
