export type PlacementSkill = 'vocabulary' | 'grammar' | 'listening' | 'pronunciation';

export interface PlacementOption { id: string; text: string; }

export interface PlacementQuestion {
  id: string;
  skill: PlacementSkill;
  level: number;
  prompt_vi: string;
  options: PlacementOption[];
  target_text: string | null;
  target_pinyin: string | null;
  number: number;
  total: 20;
}

export interface PlacementSkillResult {
  skill: PlacementSkill;
  estimated_level: number;
  correct: number;
  assessed: number;
}

export interface PlacementResult {
  recommended_level: number;
  confidence: 'low' | 'medium' | 'high';
  confidence_vi: string;
  summary_vi: string;
  skills: PlacementSkillResult[];
  completed_at: string;
  advisory_only: boolean;
  disclaimer_vi: string;
}

export interface PlacementAttempt {
  attempt_id: string;
  status: 'in_progress' | 'completed';
  question: PlacementQuestion | null;
  result: PlacementResult | null;
}

export interface PlacementStatus {
  can_take: boolean;
  in_progress: PlacementAttempt | null;
  latest_result: PlacementResult | null;
  retake_available_at: string | null;
  selected_level: number | null;
  can_apply_level: boolean;
}
