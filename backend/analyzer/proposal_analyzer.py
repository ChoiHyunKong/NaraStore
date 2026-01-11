"""
제안서 분석기
Gemini API를 사용한 제안서 요약 및 분석
"""
import json
from typing import Dict, Any
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
                    # 캐시된 데이터도 누락 필드 보완
                    self._apply_field_completion(cached)
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

            # 누락 필드 보완 적용
            self._apply_field_completion(parsed)

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

[중요: 동적 요구사항 추출 - 정확도 최우선]

**1. 완전성 (Completeness) - 모든 요구사항 빠짐없이 추출**
- 제안요청서의 "요구사항", "과업범위", "제안 내용", "납품 사양", "기술 규격", "성능 기준" 등 **모든 관련 섹션**을 찾으세요
- 명시적 요구사항뿐만 아니라 **암묵적 요구사항**도 추론하여 포함하세요
- 각 카테고리별로 **최소 3개 이상**의 항목을 추출하세요
- 작은 세부사항도 놓치지 마세요 (예: "한글/영문 지원", "IE11 호환성" 등)

**2. 구체성 (Specificity) - 추상적 표현 금지**
- ❌ 나쁜 예: "시스템 구축", "보안 강화", "성능 개선"
- ✅ 좋은 예: "사용자 인증 및 권한관리 시스템 구축 (SSO 연동, LDAP 지원)", "SSL/TLS 1.3 암호화 적용", "응답시간 2초 이내"
- 기술명, 버전, 수치, 기준을 **반드시 포함**하세요
- "등", "기타" 같은 모호한 표현은 구체적으로 풀어쓰세요

**3. 중복 제거 (No Duplication)**
- 같은 내용을 다른 표현으로 반복하지 마세요
- 유사한 항목은 하나로 통합하되, **모든 상세 정보는 포함**하세요
- 예: "DB 구축" + "데이터베이스 설계" → "데이터베이스 설계 및 구축 (ERD, 정규화, 백업 정책 포함)"

**4. 원문 충실성 (Fidelity)**
- 제안서에 명시된 **카테고리 명칭을 그대로** 사용하세요 (절대 변경 금지)
- 제안서의 **용어를 그대로 인용**하세요 (예: "모바일 앱" → "모바일 애플리케이션" 변경 금지)
- 카테고리 순서도 제안서와 동일하게 유지하세요
- 임의로 카테고리를 통합하거나 분리하지 마세요

**5. 구조화 (Structure)**
- 각 카테고리별로 논리적으로 그룹화하세요
- 우선순위가 높은 요구사항을 먼저 나열하세요
- 하위 항목이 있는 경우 계층 구조를 명확히 표현하세요

**예시:**
```
카테고리: "기능 요구사항"
항목:
- "사용자 인증 시스템 (OAuth 2.0, LDAP 연동, 2단계 인증 지원)"
- "실시간 알림 기능 (푸시 알림, 이메일, SMS 지원, 읽음 확인 기능)"
- "다국어 지원 (한국어, 영어, 일본어, 중국어 - UTF-8 인코딩)"
```

[제안요청서 내용]
{document_text}
"""
        return prompt
    
    def _apply_field_completion(self, parsed: Dict[str, Any]):
        """누락된 필드 자동 보완 (캐시/신규 분석 모두 적용)"""
        # Summary 필드 보완
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
            words = [w for w in project_name.replace('사업', '').replace('구축', '').replace('용역', '').split() if len(w) > 1]
            summary['key_keywords'] = words[:3] if len(words) >= 3 else ['디지털 혁신', '서비스 개선', '시스템 구축']
        
        # client_priorities 누락 시 일반적인 우선순위 제공
        if not summary.get('client_priorities') or len(summary.get('client_priorities', [])) == 0:
            missing_fields.append('client_priorities')
            summary['client_priorities'] = [
                "사업 일정 준수 및 기대 품질 확보",
                "시스템 안정성 및 보안 강화",
                "사용자 편의성 극대화"
            ]
        
        if missing_fields:
            logger.warning(f"누락된 필드 보완됨: {', '.join(missing_fields)}")
        
        parsed['summary'] = summary

        # Strategy 필드 보완 (Phase 3)
        strategy = parsed.get('strategy', {})
        strategy_missing = []
        
        # anchor_points 누락 시 기본 전략 제공
        if not strategy.get('anchor_points') or len(strategy.get('anchor_points', [])) == 0:
            strategy_missing.append('anchor_points')
            strategy['anchor_points'] = [
                "발주처 핵심 요구사항 충족을 위한 맞춤형 솔루션 제공",
                "사업 일정 및 품질 목표 달성을 위한 체계적 프로젝트 관리",
                "발주처와의 긴밀한 협업 및 커뮤니케이션 체계 구축"
            ]
        
        # differentiation 누락 시 기본 차별화 요소 제공
        if not strategy.get('differentiation') or len(strategy.get('differentiation', [])) == 0:
            strategy_missing.append('differentiation')
            strategy['differentiation'] = [
                "유사 프로젝트 수행 경험 및 검증된 방법론 보유",
                "최신 기술 트렌드 적용 역량 및 전문 인력 확보",
                "안정적인 시스템 구축 및 운영 지원 체계"
            ]
        
        # risk_mitigation 누락 시 기본 리스크 완화 전략 제공
        if not strategy.get('risk_mitigation') or len(strategy.get('risk_mitigation', [])) == 0:
            strategy_missing.append('risk_mitigation')
            strategy['risk_mitigation'] = [
                "일정 지연 방지를 위한 버퍼 기간 확보 및 우선순위 관리",
                "품질 이슈 최소화를 위한 단계별 검수 및 테스트 강화",
                "긴급 상황 대응을 위한 비상 연락망 및 지원 체계 구축"
            ]
        
        if strategy_missing:
            logger.warning(f"전략 필드 보완됨: {', '.join(strategy_missing)}")
        
        parsed['strategy'] = strategy


def create_analyzer(api_key: str = None) -> ProposalAnalyzer:
    """분석기 생성"""
    return ProposalAnalyzer(api_key)
