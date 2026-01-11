"""
제안서 분석기
Gemini API를 사용한 제안서 요약 및 분석
"""
import json
from typing import Dict
from backend.analyzer.schemas import AnalysisResult
from backend.analyzer.gemini.client import create_client
from backend.analyzer.gemini.request import create_request_handler
from backend.utils.logger import logger
from backend.utils.cache import analysis_cache


class ProposalAnalyzer:
    """제안서 분석 클래스"""
    
    def __init__(self, api_key: str = None, use_cache: bool = True):
        """
        분석기 초기화
        
        Args:
            api_key: Gemini API 키
            use_cache: 캐싱 사용 여부
        """
        self.client = create_client(api_key)
        self.request_handler = create_request_handler(self.client)
        self.use_cache = use_cache
    
    def analyze_structured(self, document_text: str) -> tuple[bool, Dict | str]:
        """
        제안서 구조화 분석 (통합)
        요약, 상세 분석(동적 요구사항), 수주 전략, To-Do 리스트를 한 번에 생성
        """

        try:
            logger.info("제안서 구조화 분석 시작")
            
            # 캐시 확인
            if self.use_cache:
                cached = analysis_cache.get(document_text, "structured_analysis")
                if cached:
                    logger.info("캐시에서 구조화 분석 결과 반환")
                    return True, cached
            
            prompt = self._build_structured_analysis_prompt(document_text)
            
            # Gemini API 호출 (Structured Output)
            generation_config = {
                "response_mime_type": "application/json",
                "response_schema": AnalysisResult
            }
            
            success, response_text = self.request_handler.send(prompt, generation_config=generation_config)
            
            if not success:
                return False, response_text
            
            # JSON 파싱
            try:
                parsed = json.loads(response_text)
            except json.JSONDecodeError:
                # 가끔 모델이 마크다운 코드 블록(```json ... ```)을 포함할 수 있음
                import re
                match = re.search(r'```json\s*({.*})\s*```', response_text, re.DOTALL)
                if match:
                    parsed = json.loads(match.group(1))
                else:
                    # 그냥 text일 수도 있음 (스키마 강제 실패 시)
                    logger.error(f"JSON 파싱 실패. 원본 응답:\n{response_text}")
                    return False, "AI 응답을 구조화된 데이터로 변환하는데 실패했습니다. (JSON Parsing Error)"


            # 캐시 저장
            if self.use_cache:
                analysis_cache.set(document_text, "structured_analysis", parsed)
            
            logger.info("제안서 구조화 분석 완료")
            return True, parsed

        except Exception as e:
            logger.error(f"구조화 분석 중 오류: {str(e)}")
            return False, f"분석 실패: {str(e)}"

    def _build_structured_analysis_prompt(self, document_text: str) -> str:
        """구조화 분석 프롬프트 생성"""
        prompt = f"""
당신은 대한민국 최고의 공공 제안서 분석 전문가이자 수주 컨설턴트입니다.
다음 제안요청서(RFP)를 정밀 분석하여, 수주를 위한 핵심 정보를 추출하고 전략을 수립해주세요.

[분석 목표]
1. **종합 요약(overview)**: 이 사업의 배경, 핵심 내용, 중요성을 3~5문장으로 종합 요약하세요. 단순 나열이 아닌, 스토리텔링 형식으로 작성하세요.
2. **사업 목적(purpose)**: 이 사업이 왜 발주되었는지, 최종적으로 무엇을 달성하고자 하는지 명확히 기술하세요.
3. 사업명, 예산, 기간, 기대효과 등 핵심 메타데이터를 추출하세요.
4. **요구사항을 빠짐없이 추출하여 목차별로 분류**하세요.
5. 경쟁 우위를 점할 수 있는 수주 전략을 제시하세요.
6. 실무자가 수행해야 할 구체적인 To-Do 리스트를 작성하세요.

[중요: 동적 요구사항 추출]
- 제안요청서에 있는 **'요구사항' 관련 목차나 테이블**을 찾으세요. (예: '기능 요구사항', '시스템 장비 구성 요구사항', '보안 요구사항' 등)
- 각 분류를 카테고리(category)와 항목(items)을 가진 리스트 형태로 추출하십시오.
- **제안서에 명시된 카테고리 명칭 그대로** 사용하십시오.
- 임의로 카테고리를 통합하거나 누락하지 마십시오. 제안서에 있는 그대로의 구조를 유지하는 것이 핵심입니다.
- 각 카테고리별 상세 요구사항 내용을 구체적으로 리스트업 하십시오.

[제안요청서 내용]
{document_text}
"""
        return prompt


def create_analyzer(api_key: str = None) -> ProposalAnalyzer:
    """분석기 생성"""
    return ProposalAnalyzer(api_key)
