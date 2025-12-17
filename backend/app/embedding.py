"""Embedding 生成（使用本地 sentence-transformers 模型）"""
from sentence_transformers import SentenceTransformer
import os

# 模型缓存路径（可选，避免重复下载）
MODEL_NAME = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
_model = None


def get_embedding_model():
    """延迟加载 embedding 模型"""
    global _model
    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME}")
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed_texts(texts: list) -> list:
    """
    对文本列表生成 embedding。
    返回 [[float, ...], [float, ...], ...]
    """
    if not texts:
        return []
    model = get_embedding_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()


def embed_single(text: str) -> list:
    """生成单个文本的 embedding"""
    if not text:
        return []
    model = get_embedding_model()
    emb = model.encode([text], show_progress_bar=False)
    return emb[0].tolist()


def cosine_similarity(vec1: list, vec2: list) -> float:
    """计算两个向量的余弦相似度"""
    import math
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    dot = sum(v1 * v2 for v1, v2 in zip(vec1, vec2))
    norm1 = math.sqrt(sum(v ** 2 for v in vec1))
    norm2 = math.sqrt(sum(v ** 2 for v in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)
