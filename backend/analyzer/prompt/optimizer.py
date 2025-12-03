"""
토큰 최적화
텍스트 압축 및 토큰 수 계산
"""
import re
from typing import str


class TokenOptimizer:
    """토큰 최적화 클래스"""
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        대략적인 토큰 수 추정
        (한글: 1.5자당 1토큰, 영문: 4자당 1토큰)
        
        Args:
            text: 텍스트
            
        Returns:
            예상 토큰 수
        """
        korean_chars = len(re.findall(r'[가-힣]', text))
        other_chars = len(text) - korean_chars
        
        tokens = (korean_chars / 1.5) + (other_chars / 4)
        return int(tokens)
    
    @staticmethod
    def compress(text: str, max_tokens: int = 30000) -> str:
        """
        텍스트를 최대 토큰 수에 맞게 압축
        
        Args:
            text: 원본 텍스트
            max_tokens: 최대 토큰 수
            
        Returns:
            압축된 텍스트
        """
        current_tokens = TokenOptimizer.estimate_tokens(text)
        
        if current_tokens <= max_tokens:
            return text
        
        # 비율 계산
        ratio = max_tokens / current_tokens
        target_length = int(len(text) * ratio * 0.95)  # 5% 여유
        
        # 문장 단위로 자르기
        sentences = re.split(r'[.!?]\s+', text)
        compressed = ""
        
        for sentence in sentences:
            if len(compressed) + len(sentence) <= target_length:
                compressed += sentence + ". "
            else:
                break
        
        return compressed.strip()
    
    @staticmethod
    def prioritize_content(text: str, keywords: list = None) -> str:
        """
        키워드 기반 우선순위 압축
        
        Args:
            text: 원본 텍스트
            keywords: 우선순위 키워드 리스트
            
        Returns:
            우선순위 기반 압축 텍스트
        """
        if not keywords:
            return text
        
        sentences = re.split(r'[.!?]\s+', text)
        scored_sentences = []
        
        for sentence in sentences:
            score = sum(1 for keyword in keywords if keyword in sentence)
            scored_sentences.append((score, sentence))
        
        # 점수 순으로 정렬
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        
        # 상위 문장들 결합
        top_sentences = [s[1] for s in scored_sentences[:len(scored_sentences)//2]]
        
        return ". ".join(top_sentences)


# 전역 인스턴스
token_optimizer = TokenOptimizer()
