"""
프롬프트 빌더
동적 프롬프트 생성 및 변수 치환
"""
from typing import Dict, Optional
from backend.analyzer.prompt.templates import prompt_templates
from backend.utils.logger import logger


class PromptBuilder:
    """프롬프트 생성 클래스"""
    
    @staticmethod
    def build(template_name: str, key: str, variables: Dict[str, str] = None) -> Optional[str]:
        """
        템플릿과 변수로 프롬프트 생성
        
        Args:
            template_name: 템플릿 파일명
            key: 템플릿 키
            variables: 치환할 변수 딕셔너리
            
        Returns:
            생성된 프롬프트 또는 None
        """
        # 템플릿 로드
        template = prompt_templates.get(template_name, key)
        if not template:
            logger.error(f"템플릿을 찾을 수 없습니다: {template_name}.{key}")
            return None
        
        # 변수 치환
        if variables:
            try:
                prompt = template.format(**variables)
            except KeyError as e:
                logger.error(f"변수 치환 실패: {str(e)}")
                return None
        else:
            prompt = template
        
        logger.debug(f"프롬프트 생성 완료: {template_name}.{key}")
        return prompt
    
    @staticmethod
    def build_analysis_prompt(document_text: str) -> Optional[str]:
        """
        제안서 분석 프롬프트 생성
        
        Args:
            document_text: 문서 텍스트
            
        Returns:
            분석 프롬프트
        """
        return PromptBuilder.build(
            "analysis",
            "analysis_prompt",
            {"document_text": document_text}
        )
    
    @staticmethod
    def build_summary_prompt(analysis_result: str) -> Optional[str]:
        """
        요약 프롬프트 생성
        
        Args:
            analysis_result: 분석 결과
            
        Returns:
            요약 프롬프트
        """
        return PromptBuilder.build(
            "summary",
            "summary_prompt",
            {"analysis_result": analysis_result}
        )
    
    @staticmethod
    def build_strategy_prompt(analysis_result: str) -> Optional[str]:
        """
        전략 수립 프롬프트 생성
        
        Args:
            analysis_result: 분석 결과
            
        Returns:
            전략 프롬프트
        """
        return PromptBuilder.build(
            "strategy",
            "strategy_prompt",
            {"analysis_result": analysis_result}
        )


# 전역 인스턴스
prompt_builder = PromptBuilder()
