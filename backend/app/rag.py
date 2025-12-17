"""直接问答模式 - 不检索教材，直接调用 LLM"""
from typing import Dict
from .llm import get_llm_provider


def ask_direct(question: str) -> Dict:
    """
    直接问答模式：用户提问 → LLM 回答（基于 LLM 自身知识）。
    
    参数：
      - question: 用户问题
    
    返回：
      {
        "question": "...",
        "answer": "...",
        "llm_provider": "AlibabaProvider"
      }
    """
    try:
        # 调用 LLM
        llm_provider = get_llm_provider()
        answer = llm_provider.generate(question, max_tokens=1000)
        
        return {
            "question": question,
            "answer": answer,
            "llm_provider": type(llm_provider).__name__,
            "success": True
        }
    
    except Exception as e:
        return {
            "question": question,
            "answer": f"生成答案时出错：{str(e)}",
            "error": str(e),
            "success": False
        }
