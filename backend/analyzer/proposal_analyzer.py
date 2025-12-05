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
    
    def summarize(self, document_text: str) -> tuple[bool, Dict | str]:
        """
        제안서 요약 (캐싱 지원)
        """
        try:
            logger.info("제안서 요약 시작")
            
            # 캐시 확인
            if self.use_cache:
                cached = analysis_cache.get(document_text, "summary")
                if cached:
                    logger.info("캐시에서 요약 결과 반환")
                    return True, cached
            
            # 요약 프롬프트 생성
            prompt = self._build_summary_prompt(document_text)
            
            # Gemini API 호출
            success, response = self.request_handler.send(prompt)
            
            if not success:
                return False, response
            
            # JSON 응답 파싱
            success, parsed = response_parser.parse_json(response)
            
            if not success:
                return True, {"raw_text": response}
            
            # 캐시 저장
            if self.use_cache:
                analysis_cache.set(document_text, "summary", parsed)
            
            logger.info("제안서 요약 완료")
            return True, parsed
            
        except Exception as e:
            logger.error(f"제안서 요약 중 오류: {str(e)}")
            return False, f"요약 실패: {str(e)}"
    
    def analyze_detailed(self, document_text: str) -> tuple[bool, Dict | str]:
        """제안서 상세 분석 (캐싱 지원)"""
        try:
            logger.info("제안서 상세 분석 시작")
            
            # 캐시 확인
            if self.use_cache:
                cached = analysis_cache.get(document_text, "analysis")
                if cached:
                    logger.info("캐시에서 분석 결과 반환")
                    return True, cached
            
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
            
            # 캐시 저장
            if self.use_cache:
                analysis_cache.set(document_text, "analysis", parsed)
            
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
            
            # 분석 결과를 문자열로 변환 (문자열이면 그대로 사용)
            if isinstance(analysis_result, str):
                analysis_text = analysis_result
            else:
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
            
            # 분석 결과를 문자열로 변환 (문자열이면 그대로 사용)
            if isinstance(analysis_result, str):
                analysis_text = analysis_result
            else:
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
당신은 전문 제안서 분석가입니다. 다음 제안요청서(RFP)를 상세히 분석하여 핵심 정보를 JSON 형식으로 추출해주세요.
각 항목을 가능한 상세하게 작성해주세요. 특히 예산, 일정, 인력 정보는 정확하게 추출해주세요.

[제안요청서 내용]
{document_text}

다음 정보를 추출하여 JSON으로 반환해주세요:
{{
    "project_title": "프로젝트 정식 명칭 (사업명)",
    "project_overview": "프로젝트 개요를 4-5문장으로 상세히 설명. 어떤 시스템/서비스를 구축하는지, 주요 특징은 무엇인지 설명",
    
    "client_info": {{
        "organization": "발주 기관명",
        "department": "담당 부서",
        "contact": "담당자 연락처"
    }},
    
    "background": {{
        "current_issues": "현재 문제점 또는 개선 필요성을 2-3가지 구체적으로 설명",
        "necessity": "이 프로젝트가 필요한 이유를 2-3문장으로 설명"
    }},
    
    "project_goal": {{
        "main_goal": "프로젝트의 핵심 목표를 1-2문장으로 명확하게",
        "sub_goals": ["세부 목표 1", "세부 목표 2", "세부 목표 3"]
    }},
    
    "scope": {{
        "target_users": "서비스 대상자/이용자 설명",
        "coverage": "서비스 범위 또는 적용 범위",
        "exclusions": "과업 범위에서 제외되는 사항 (있다면)"
    }},
    
    "budget": {{
        "total_amount": "총 사업비 금액 (원 단위로 정확히, 예: 150,000,000원)",
        "vat_included": "부가세 포함 여부 (포함/별도/미명시)",
        "budget_type": "예산 유형 (정액/추정가격 등)",
        "breakdown": "예산 세부 내역이 있다면 기재 (인건비, 직접경비 등)"
    }},
    
    "schedule": {{
        "total_period": "총 사업 기간 (정확히, 예: 100일, 6개월 등)",
        "start_date": "착수 예정일 또는 계약 시작일",
        "end_date": "완료 예정일 또는 계약 종료일",
        "proposal_deadline": "제안서 제출 마감일시",
        "presentation_date": "제안설명회/PT 예정일 (있다면)",
        "key_milestones": ["착수보고", "중간보고", "최종보고 등 주요 일정"]
    }},
    
    "personnel": {{
        "onsite_required": "상주 인력 필요 여부 (필요/불필요/협의)",
        "onsite_count": "상주 인력 수 (명시된 경우)",
        "onsite_location": "상주 장소 (명시된 경우)",
        "pm_required": "PM(프로젝트 관리자) 필수 여부",
        "key_personnel": ["필수 투입 인력 역할 (PM, PL, 개발자 등)"],
        "qualification_requirements": ["투입 인력 자격 요건 (경력, 자격증 등)"]
    }},
    
    "main_tasks": [
        {{
            "task_name": "주요 과업 1",
            "description": "과업에 대한 2-3줄 설명",
            "deliverables": ["산출물 1", "산출물 2"]
        }}
    ],
    
    "technical_requirements": [
        "기술 요구사항 (개발 언어, 프레임워크, 플랫폼 등)"
    ],
    
    "qualification": {{
        "mandatory": ["필수 자격 요건 (등록증, 인증 등)"],
        "preferred": ["우대 사항"],
        "restrictions": ["참여 제한 사항 (있다면)"]
    }},
    
    "evaluation_criteria": [
        {{"criteria": "평가 항목", "weight": "배점"}},
        {{"criteria": "기술 능력", "weight": "00점"}},
        {{"criteria": "수행 실적", "weight": "00점"}}
    ],
    
    "contract_info": {{
        "contract_type": "계약 방식 (일반경쟁/제한경쟁/협상에 의한 계약 등)",
        "payment_terms": "대금 지급 조건 (선급금, 중도금, 잔금 비율)",
        "warranty_period": "하자보수 기간"
    }},
    
    "expected_effects": [
        "기대 효과 1",
        "기대 효과 2"
    ],
    
    "key_considerations": [
        "입찰 시 반드시 확인해야 할 핵심 사항",
        "주의 사항"
    ],
    
    "attachments": [
        "첨부된 서식 또는 문서 목록 (있다면)"
    ]
}}

[중요 지침]
1. 예산 금액은 문서에 명시된 정확한 금액을 추출하세요. 추정하지 마세요.
2. 상주 인력, PM 필수 여부 등 인력 관련 정보를 주의 깊게 확인하세요.
3. 일정은 문서에 명시된 날짜를 정확히 추출하세요.
4. 정보가 명시되지 않은 경우 "정보 없음" 또는 "미명시"로 표시하세요.
5. 응답은 반드시 유효한 JSON 형식이어야 합니다.
"""
        return prompt


def create_analyzer(api_key: str = None) -> ProposalAnalyzer:
    """분석기 생성"""
    return ProposalAnalyzer(api_key)
