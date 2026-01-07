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
        # [MOCK MODE] UI 테스트를 위한 가짜 데이터 강제 반환
        # API Quota 초과 문제로 인해 임시 추가됨
        USE_MOCK = True
        
        if USE_MOCK:
            logger.info("[MOCK MODE] 가짜 데이터를 반환합니다.")
            mock_data = {
                "summary": {
                    "expected_effects": [
                        "기상 정보 전달 속도 30% 향상 및 대국민 만족도 제고",
                        "클라우드 네이티브 전환을 통한 시스템 안정성 확보 (가용성 99.99%)",
                        "유지보수 효율성 증대 및 운영 비용 15% 절감"
                    ],
                    "project_name": "기상청 날씨알리미 앱 고도화 사업 (MOCK)",
                    "period": "2025.04.01 ~ 2025.12.31 (9개월)",
                    "budget": "595,000,000원 (VAT 포함)",
                    "total_requirements_count": 42
                },
                "requirements": [
                    {
                        "category": "기능 요구사항 (Functional)",
                        "items": [
                            "사용자 위치 기반 실시간 푸시 알림 속도 1초 이내 보장",
                            "위젯 기능 고도화 (크기별, 날씨 정보별 커스텀 위젯 제공)",
                            "SNS 로그인 (네이버, 카카오, 애플) 연동 및 통합 인증 구현",
                            "시각 장애인을 위한 대체 텍스트 및 음성 안내 기능 (웹 접근성 준수)"
                        ]
                    },
                    {
                        "category": "시스템 장비 구성 요구사항",
                        "items": [
                            "클라우드 인프라(AWS/GCP) 기반의 오토스케일링 아키텍처 구성",
                            "이중화된 DB 구성 및 실시간 백업 체계 마련 (RPO 5분 이내)",
                            "대용량 트래픽 처리를 위한 Redis 캐싱 레이어 도입"
                        ]
                    },
                    {
                        "category": "보안 요구사항 (Security)",
                        "items": [
                            "개인정보 암호화 저장 (AES-256) 및 전송 구간 암호화 (TLS 1.3)",
                            "관리자 페이지 2차 인증(MFA) 적용",
                            "모의해킹 분기별 1회 수행 및 취약점 조치 이행"
                        ]
                    }
                ],
                "strategy": {
                    "win_strategy": [
                        "**[차별화 1] 넷플릭스 유례 아키텍처 적용**: MSA(Microservice Architecture) 도입으로 장애 격리 및 무중단 배포 구현",
                        "**[차별화 2] 3D 날씨 시각화**: 유니티(Unity) 엔진 기반의 실감형 날씨 정보 제공으로 사용자 경험 극대화",
                        "**[신뢰성] 공공사업 수행 노하우**: 유사 기상청 사업 3회 수행 경험을 보유한 PM 및 전담 인력 배치"
                    ],
                    "references": [
                        "2023 기상청 지진 조기 경보 시스템 고도화 사업",
                        "2024 행정안전부 재난 안전 문자 발송 시스템 구축"
                    ]
                },
                "todo_list": [
                    "AWS 클라우드 구성도 및 예상 비용 산출 (내일까지)",
                    "기존 날씨 앱 사용자 리뷰 분석 (불만 사항 Top 10 도출)",
                    "UI/UX 시안 작업 (메인 화면, 위젯 화면) - 피그마 공유 필요",
                    "제안서 목차 초안 작성 및 팀원 R&R 배분",
                    "유사 사업 실적 증명서 발급 신청"
                ]
            }
            return True, mock_data

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
당신은 대한민국 최고의 공공 제안서 분석 전문가입니다.
다음 제안요청서(RFP)를 정밀 분석하여, 수주를 위한 핵심 정보를 추출하고 전략을 수립해주세요.

[분석 목표]
1. 제안요청서의 핵심 내용을 요약하고 (예산, 기간 등)
2. **요구사항을 빠짐없이 추출하여 목차별로 분류**하고
3. 경쟁 우위를 점할 수 있는 수주 전략을 제시하고
4. 실무자가 수행해야 할 구체적인 To-Do 리스트를 작성하십시오.

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
