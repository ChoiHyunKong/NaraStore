"""
제안서 분석기
Gemini API를 사용한 제안서 요약 및 분석
"""
import json
from typing import Dict, Optional
from backend.analyzer.gemini.client import create_client
from backend.analyzer.gemini.request import create_request_handler
from backend.analyzer.gemini.response import response_parser
from backend.analyzer.prompt.builder import prompt_builder
from backend.utils.logger import logger


class ProposalAnalyzer:
    """제안서 분석 클래스"""
    
    def __init__(self, api_key: str = None):
        """
        분석기 초기화
        
        Args:
            api_key: Gemini API 키
        """
        self.client = create_client(api_key)
        self.request_handler = create_request_handler(self.client)
    
    def summarize(self, document_text: str) -> tuple[bool, Dict | str]:
        """
        제안서 요약
        
        Args:
            document_text: 통합된 제안서 텍스트
            
        Returns:
            (성공 여부, 요약 결과 또는 에러 메시지)
        """
        try:
            logger.info("제안서 요약 시작")
            
            # 요약 프롬프트 생성
            prompt = self._build_summary_prompt(document_text)
            
            # Gemini API 호출
            success, response = self.request_handler.send(prompt)
            
            if not success:
                return False, response
            
            # JSON 응답 파싱
            success, parsed = response_parser.parse_json(response)
            
            if not success:
                # JSON 파싱 실패 시 원본 텍스트 반환
                return True, {"raw_text": response}
            
            logger.info("제안서 요약 완료")
            return True, parsed
            
        except Exception as e:
            logger.error(f"제안서 요약 중 오류: {str(e)}")
            return False, f"요약 실패: {str(e)}"
    
    def analyze_detailed(self, document_text: str) -> tuple[bool, Dict | str]:
        """
        제안서 상세 분석
        
        Args:
            document_text: 통합된 제안서 텍스트
            
        Returns:
            (성공 여부, 분석 결과 또는 에러 메시지)
        """
        try:
            logger.info("제안서 상세 분석 시작")
            
            # 분석 프롬프트 생성
            prompt = prompt_builder.build_analysis_prompt(document_text)
            
            if not prompt:
                return False, "프롬프트 생성 실패"
            
            # Gemini API 호출
            success, response = self.request_handler.send(prompt)
            
            if not success:
                return False, response
            
            # JSON 응답 파싱
            success, parsed = response_parser.parse_json(response)
            
            if not success:
                return True, {"raw_text": response}
            
            logger.info("제안서 상세 분석 완료")
            return True, parsed
            
        except Exception as e:
            logger.error(f"제안서 분석 중 오류: {str(e)}")
            return False, f"분석 실패: {str(e)}"
    
    def generate_strategy(self, analysis_result: Dict) -> tuple[bool, str | Dict]:
        """
        수주 전략 생성
        
        Args:
            analysis_result: 분석 결과
            
        Returns:
            (성공 여부, 전략 또는 에러 메시지)
        """
        try:
            logger.info("수주 전략 생성 시작")
            
            # 분석 결과를 문자열로 변환
            analysis_text = json.dumps(analysis_result, ensure_ascii=False, indent=2)
            
            # 전략 프롬프트 생성
            prompt = prompt_builder.build_strategy_prompt(analysis_text)
            
            if not prompt:
                return False, "프롬프트 생성 실패"
            
            # Gemini API 호출
            success, response = self.request_handler.send(prompt)
            
            if not success:
                return False, response
            
            logger.info("수주 전략 생성 완료")
            return True, response
            
        except Exception as e:
            logger.error(f"전략 생성 중 오류: {str(e)}")
            return False, f"전략 생성 실패: {str(e)}"

    def generate_references(self, analysis_result: Dict) -> tuple[bool, Dict | str]:
        """
        유사 프로젝트 레퍼런스 생성
        
        Args:
            analysis_result: 분석 결과
            
        Returns:
            (성공 여부, 레퍼런스 결과 또는 에러 메시지)
        """
        try:
            logger.info("유사 프로젝트 레퍼런스 생성 시작")
            
            # 분석 결과를 문자열로 변환
            analysis_text = json.dumps(analysis_result, ensure_ascii=False, indent=2)
            
            # 레퍼런스 프롬프트 생성
            prompt = prompt_builder.build_reference_prompt(analysis_text)
            
            if not prompt:
                return False, "프롬프트 생성 실패"
            
            # Gemini API 호출
            success, response = self.request_handler.send(prompt)
            
            if not success:
                return False, response
            
            # JSON 응답 파싱
            success, parsed = response_parser.parse_json(response)
            
            if not success:
                return True, {"raw_text": response}
            
            logger.info("유사 프로젝트 레퍼런스 생성 완료")
            return True, parsed
            
        except Exception as e:
            logger.error(f"레퍼런스 생성 중 오류: {str(e)}")
            return False, f"레퍼런스 생성 실패: {str(e)}"
    
    def _build_summary_prompt(self, document_text: str) -> str:
        """요약용 프롬프트 생성"""
        prompt = f"""
다음 제안요청서(RFP)를 분석하여 핵심 정보를 JSON 형식으로 추출해주세요.

{document_text}

다음 정보를 추출하여 JSON으로 반환해주세요:
{{
    "project_overview": "프로젝트 개요 (2-3문장)",
    "project_goal": "프로젝트 목표 및 목적",
    "background": "왜 이 프로젝트를 수행하는지 (배경 및 필요성)",
    "main_tasks": ["주요 과업 1", "주요 과업 2", ...],
    "budget": "프로젝트 금액 (명시되어 있다면)",
    "deadline": "마감 날짜 (명시되어 있다면)",
    "key_requirements": ["핵심 요구사항 1", "핵심 요구사항 2", ...]
}}

응답은 반드시 유효한 JSON 형식이어야 합니다.
"""
        return prompt


def create_analyzer(api_key: str = None) -> ProposalAnalyzer:
    """분석기 생성"""
    return ProposalAnalyzer(api_key)
