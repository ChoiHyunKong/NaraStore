"""
텍스트 정제 유틸리티
불필요한 문자 제거 및 정규화
"""
import re
from typing import List, Optional


class TextCleaner:
    """텍스트 정제 클래스"""
    
    @staticmethod
    def clean(text: str) -> str:
        """
        텍스트 전체 정제
        
        Args:
            text: 원본 텍스트
            
        Returns:
            정제된 텍스트
        """
        if not text:
            return ""
        
        # 연속된 공백 제거
        text = TextCleaner.normalize_whitespace(text)
        
        # 특수문자 정리
        text = TextCleaner.remove_special_chars(text)
        
        # 연속된 줄바꿈 정리
        text = TextCleaner.normalize_newlines(text)
        
        return text.strip()
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """연속된 공백을 하나로 정규화"""
        # 탭을 공백으로 변환
        text = text.replace('\t', ' ')
        
        # 연속된 공백을 하나로
        text = re.sub(r' +', ' ', text)
        
        return text
    
    @staticmethod
    def normalize_newlines(text: str) -> str:
        """연속된 줄바꿈 정리"""
        # 3개 이상의 연속된 줄바꿈을 2개로
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 줄 끝의 공백 제거
        lines = [line.rstrip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text
    
    @staticmethod
    def remove_special_chars(text: str) -> str:
        """불필요한 특수문자 제거"""
        # 제어 문자 제거 (줄바꿈, 탭 제외)
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # 특정 특수문자 제거
        text = text.replace('\uf0b7', '•')  # 총알 기호 정규화
        text = text.replace('\u200b', '')   # 폭 없는 공백 제거
        
        return text
    
    @staticmethod
    def extract_sentences(text: str) -> list[str]:
        """텍스트를 문장 단위로 분리"""
        # 마침표, 느낌표, 물음표로 문장 분리
        sentences = re.split(r'[.!?]\s+', text)
        
        # 빈 문장 제거
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    @staticmethod
    def truncate(text: str, max_length: int = 10000) -> str:
        """
        텍스트를 최대 길이로 자르기
        
        Args:
            text: 원본 텍스트
            max_length: 최대 길이
            
        Returns:
            잘린 텍스트
        """
        if len(text) <= max_length:
            return text
        
        # 문장 단위로 자르기 시도
        truncated = text[:max_length]
        last_period = truncated.rfind('.')
        
        if last_period > max_length * 0.8:  # 80% 이상 위치에 마침표가 있으면
            return truncated[:last_period + 1]
        
        return truncated + "..."


# 전역 인스턴스
text_cleaner = TextCleaner()
