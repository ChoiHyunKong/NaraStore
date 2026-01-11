from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class AnalysisSummary(BaseModel):
    project_name: str = Field(description="제안요청서에 명시된 사업명")
    overview: str = Field(description="사업의 배경, 핵심 내용, 중요성을 종합적으로 서술한 요약문 (3~5문장)")
    purpose: str = Field(description="이 사업이 발주된 목적과 달성하고자 하는 최종 목표")
    key_keywords: List[str] = Field(description="이 사업의 핵심 키워드 3~5개 (필수 생성)")
    client_priorities: List[str] = Field(description="발주처가 가장 중요시하는 포인트 3~5개 (필수 생성)")
    period: str = Field(description="사업 수행 기간")
    budget: str = Field(description="사업 예산 (명시되지 않은 경우 '내용 없음' 등의 텍스트)")
    expected_effects: List[str] = Field(description="프로젝트 수행 시 기대되는 이점 및 효과 목록")
    total_requirements_count: int = Field(description="추출된 전체 요구사항의 총 개수")

class StrategyConfig(BaseModel):
    anchor_points: List[str] = Field(description="발주처 핵심 요구사항 기반 앵커 포인트 (3~5개, 발주처가 중시하는 요소를 충족하는 구체적 방안)")
    differentiation: List[str] = Field(description="경쟁사 대비 차별화 요소 (3~5개, 우리의 강점 및 경쟁 우위)")
    risk_mitigation: List[str] = Field(description="사업 수행 리스크 및 완화 전략 (3~5개, 예상 리스크와 대응 방안)")
    win_strategy: List[str] = Field(description="분석 내용을 기반으로 한 종합 수주 전략 및 제언")
    references: List[str] = Field(description="유사 사업 수행 경험 또는 참고할 만한 레퍼런스 제안")

class RequirementCategory(BaseModel):
    category: str = Field(description="요구사항 카테고리 명칭 (예: '기능 요구사항', '보안 요구사항' 등 RFP 목차 그대로)")
    items: List[str] = Field(description="해당 카테고리의 상세 요구사항 목록")

class TodoItem(BaseModel):
    task: str = Field(description="구체적인 할 일 내용")

class ResourceRequirement(BaseModel):
    role: str = Field(description="필요 역할 (예: PM, PL, FE개발, BE개발, 디자인)")
    count: int = Field(description="필요 인원 수")
    required_skills: List[str] = Field(description="이 역할에 필요한 핵심 기술 스택")
    reason: str = Field(description="이 인력이 필요한 구체적인 이유 및 담당 업무")

class AnalysisResult(BaseModel):
    summary: AnalysisSummary
    requirements: List[RequirementCategory] = Field(
        description="제안서의 요구사항을 카테고리별로 분류한 리스트"
    )
    strategy: StrategyConfig
    resource_requirements: List[ResourceRequirement] = Field(
        description="프로젝트 수행을 위해 필요한 인력 구성 및 요건 (Phase 4)",
        default=[] 
    )
    todo_list: List[str] = Field(description="이 제안 작업을 완료하기 위해 수행해야 할 구체적인 할 일 목록 (8개 내외)")
