"""分段（Chunking）与清理策略"""
import re
from typing import List


def clean_text(text: str) -> str:
    """去噪：移除多余空白、特殊符号、重复换行等。"""
    if not text:
        return ''
    # 去除多个连续空白符
    text = re.sub(r'\s+', ' ', text)
    # 去除页眉页脚（通常是短行且重复）
    # 简单启发式：如果超过 50% 的行短于 20 字符，可能是页眉/脚，但这里我们保留所有内容
    text = text.strip()
    return text


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[dict]:
    """
    按 token（单词/字符）数分段，支持重叠。
    返回 [{'text': '...', 'start': 0, 'end': 50}, ...]
    """
    if not text:
        return []
    
    text = clean_text(text)
    words = text.split()
    chunks = []
    start_idx = 0
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk_words = words[i : i + chunk_size]
        chunk_text = ' '.join(chunk_words)
        
        if chunk_text.strip():
            chunks.append({
                'text': chunk_text,
                'start': start_idx,
                'end': start_idx + len(chunk_text)
            })
        start_idx += len(chunk_text) + 1  # +1 for space
    
    return chunks


def chunk_by_paragraph(text: str) -> List[dict]:
    """按段落分段（适合学科材料）。"""
    if not text:
        return []
    
    text = clean_text(text)
    # 按多个换行符分割段落
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    start_idx = 0
    for para in paragraphs:
        if para:
            chunks.append({
                'text': para,
                'start': start_idx,
                'end': start_idx + len(para)
            })
            start_idx += len(para) + 2
    
    return chunks
