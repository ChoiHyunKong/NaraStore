// 구조화된 분석 결과 인터페이스 (Backend Pydantic 모델과 일치)
export interface AnalysisSummary {
  overview: string;
  purpose: string;
  key_keywords: string[];
  client_priorities: string[];
  expected_effects: string[];
  project_name: string;
  period: string;
  budget: string;
  total_requirements_count: number;
}

export interface StrategyConfig {
  anchor_points: string[];
  differentiation: string[];
  risk_mitigation: string[];
  win_strategy: string[];
  references: string[];
}

export interface RequirementCategory {
  category: string;
  items: string[];
}

export interface AnalysisResultData {
  summary: AnalysisSummary;
  requirements: RequirementCategory[]; // 리스트 형태로 변경
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

// Dashboard Types
export type PeriodType = '7days' | '1month' | '1year';

export interface ActivityData {
  date: string;      // ISO date string or month label
  count: number;     // Number of analyses
}

export interface DashboardStats {
  totalRFPs: number;
  completedCount: number;
  pendingCount: number;
  errorCount: number;

  activityData: ActivityData[];
  todoCompletionRate: number;
}

export interface Personnel {
  id: string;
  name: string;
  position: string;
  role?: string; // e.g. 팀장, 파트장, 선임 (직위)
  experience: number;
  techStack: string[];
  registeredAt?: string;
}
