from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class AnalysisSummary(BaseModel):
    expected_effects: List[str] = Field(description="프로젝트 수행 시 기대되는 이점 및 효과 목록")
    project_name: str = Field(description="제안요청서에 명시된 사업명")
    period: str = Field(description="사업 수행 기간")
    budget: str = Field(description="사업 예산 (명시되지 않은 경우 '내용 없음' 등의 텍스트)")
    total_requirements_count: int = Field(description="추출된 전체 요구사항의 총 개수")

class StrategyConfig(BaseModel):
    win_strategy: List[str] = Field(description="분석 내용을 기반으로 한 수주 전략 및 제언")
    references: List[str] = Field(description="유사 사업 수행 경험 또는 참고할 만한 레퍼런스 제안")

class RequirementCategory(BaseModel):
    category: str = Field(description="요구사항 카테고리 명칭 (예: '기능 요구사항', '보안 요구사항' 등 RFP 목차 그대로)")
    items: List[str] = Field(description="해당 카테고리의 상세 요구사항 목록")

class AnalysisResult(BaseModel):
    summary: AnalysisSummary
    requirements: List[RequirementCategory] = Field(
        description="제안서의 요구사항을 카테고리별로 분류한 리스트"
    )
    strategy: StrategyConfig
    todo_list: List[str] = Field(description="이 제안 작업을 완료하기 위해 수행해야 할 구체적인 할 일 목록 (8개 내외)")
