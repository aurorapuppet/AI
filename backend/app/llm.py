"""LLM 抽象层 - 支持多个 LLM 供应商（OpenAI、Alibaba 等）"""
from abc import ABC, abstractmethod
from typing import List
import os


class LLMProvider(ABC):
    """LLM 提供商基类"""
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 800) -> str:
        """生成回答"""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API 实现"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set in environment")
        from openai import OpenAI
        self.client = OpenAI(api_key=self.api_key)
    
    def generate(self, prompt: str, max_tokens: int = 800) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个有用的教材问答助手。根据提供的资料准确回答用户的问题。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()


class AlibabaProvider(LLMProvider):
    """阿里云通义千问实现（使用 dashscope SDK）"""
    
    def __init__(self):
        self.api_key = os.getenv('ALIBABA_API_KEY')
        self.model = os.getenv('ALIBABA_MODEL', 'qwen-turbo')
        if not self.api_key:
            raise ValueError("ALIBABA_API_KEY not set in environment")
        import dashscope
        dashscope.api_key = self.api_key
    
    def generate(self, prompt: str, max_tokens: int = 800) -> str:
        import dashscope
        from dashscope import Generation
        
        response = Generation.call(
            model=self.model,
            messages=[
                {'role': 'system', 'content': '你是一个有用的教材问答助手。根据提供的资料准确回答用户的问题。'},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=max_tokens
        )
        
        if response.status_code == 200:
            return response.output.choices[0]['message']['content'].strip()
        else:
            raise RuntimeError(f"Alibaba API error: {response.code} - {response.message}")


class LocalLLMProvider(LLMProvider):
    """本地 LLM 实现（使用 transformers 或 llama.cpp）"""
    
    def __init__(self):
        # 这里可以集成 llama.cpp / transformers
        # 目前为占位符实现
        self.model_name = os.getenv('LOCAL_MODEL', 'gpt2')
    
    def generate(self, prompt: str, max_tokens: int = 800) -> str:
        # 简单示例：使用 transformers pipeline
        try:
            from transformers import pipeline
            generator = pipeline('text-generation', model=self.model_name)
            result = generator(prompt, max_length=max_tokens, do_sample=True)
            return result[0]['generated_text'].strip()
        except Exception as e:
            return f"Local LLM error: {str(e)}"


def get_llm_provider() -> LLMProvider:
    """根据环境变量选择 LLM 提供商"""
    provider_name = os.getenv('LLM_PROVIDER', 'openai').lower()
    
    if provider_name == 'openai':
        return OpenAIProvider()
    elif provider_name == 'alibaba':
        return AlibabaProvider()
    elif provider_name == 'local':
        return LocalLLMProvider()
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")
