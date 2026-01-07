// 구조화된 분석 결과 인터페이스 (Backend Pydantic 모델과 일치)
export interface AnalysisSummary {
  expected_effects: string[];
  project_name: string;
  period: string;
  budget: string;
  total_requirements_count: number;
}

export interface StrategyConfig {
  win_strategy: string[];
  references: string[];
}

export interface AnalysisResultData {
  summary: AnalysisSummary;
  requirements: Record<string, string[]>; // 동적 키 (예: "기능 요구사항": [...])
  strategy: StrategyConfig;
  todo_list: string[];
}

export interface RFP {
  id: string;
  title: string;
  analysisDate: string;
  status: 'pending' | 'completed' | 'error';

  // New Structured Data (optional for backward compatibility with old records)
  structuredAnalysis?: AnalysisResultData;

  // Legacy fields (kept for backward compatibility display if needed)
  summary?: string;
  strategy?: string;
  analysis?: string;
}

export interface TodoItem {
  id: string;
  text: string;
  completed: boolean;
}

export type TabType = 'summary' | 'analysis' | 'strategy';
