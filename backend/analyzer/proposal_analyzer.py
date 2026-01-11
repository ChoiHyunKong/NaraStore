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

            # 누락 필드 보완 (Gemini API가 생성하지 않은 필드 추가)
            summary = parsed.get('summary', {})
            missing_fields = []
            
            # overview 누락 시 간단한 요약 생성
            if not summary.get('overview'):
                missing_fields.append('overview')
                summary['overview'] = f"{summary.get('project_name', '본 사업')}은/는 디지털 혁신과 서비스 향상을 목표로 발주되었습니다."
            
            # purpose 누락 시 기본값 생성
            if not summary.get('purpose'):
                missing_fields.append('purpose')
                summary['purpose'] = "디지털 전환 및 서비스 품질 향상을 통한 사용자 만족도 제고"
            
            # key_keywords 누락 시 프로젝트명에서 추출
            if not summary.get('key_keywords') or len(summary.get('key_keywords', [])) == 0:
                missing_fields.append('key_keywords')
                project_name = summary.get('project_name', '')
                # 간단한 키워드 추출 (공백 기준)
                words = project_name.replace('사업', '').replace('구축', '').replace('용역', '').split()
                summary['key_keywords'] = words[:3] if len(words) >= 3 else ['디지털 혁신', '서비스 개선', '시스템 구축']
            
            # client_priorities 누락 시 일반적인 우선순위 제공
            if not summary.get('client_priorities') or len(summary.get('client_priorities', [])) == 0:
                missing_fields.append('client_priorities')
                summary['client_priorities'] = [
                    "사업 일정 준수 및기대 품질 확보",
                    "시스템 안정성 및 보안 강화",
                    "사용자 편의성 극대화"
                ]
            
            if missing_fields:
                logger.warning(f"누락된 필드 보완됨: {', '.join(missing_fields)}")
            
            parsed['summary'] = summary

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

[분석 목표 - 모든 항목 필수 생성]
1. **종합 요약(overview)**: 이 사업의 배경, 핵심 내용, 중요성을 3~5문장으로 종합 요약하세요. 단순 나열이 아닌, 스토리텔링 형식으로 작성하세요.

2. **사업 목적(purpose)**: 이 사업이 왜 발주되었는지, 최종적으로 무엇을 달성하고자 하는지 명확히 기술하세요.

3. **핵심 키워드(key_keywords) - 필수**: 이 사업을 대표하는 핵심 키워드를 **반드시 3~5개** 추출하세요.
   - 예시: ['AI 기반 챗봇', '다국어 지원', '실시간 알림', 'RAG 기술', '자연어 처리']
   - 제안요청서의 주요 기술, 목표, 특징을 키워드로 축약하세요.
   - 이 필드를 비워두지 마세요. 반드시 리스트 형태로 생성하세요.

4. **발주처 중점 포인트(client_priorities) - 필수**: 발주처가 가장 중요시하는 핵심 요구사항 또는 성공 기준을 **반드시 3~5개** 도출하세요.
   - 예시: ['사용자 편의성 극대화', '시스템 안정성 및 보안', '일정 준수', '데이터 정확도 향상']
   - 제안요청서에서 발주처가 강조한 핵심 가치, 우선순위를 추출하세요.
   - 이 필드를 비워두지 마세요. 반드시 리스트 형태로 생성하세요.

5. 사업명, 예산, 기간, 기대효과 등 핵심 메타데이터를 추출하세요.

6. **요구사항을 빠짐없이 추출하여 목차별로 분류**하세요.

7. 경쟁 우위를 점할 수 있는 수주 전략을 제시하세요.

8. 실무자가 수행해야 할 구체적인 To-Do 리스트를 작성하세요.

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
