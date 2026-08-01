import { ContentOption } from './learning-content';

export type LevelExamSkill = 'vocabulary' | 'grammar' | 'reading' | 'listening';
export interface LevelExamQuestion { id: string; skill: LevelExamSkill; prompt_vi: string; options: ContentOption[]; }
export interface LevelExamSkillResult { skill: LevelExamSkill; correct: number; total: number; percent: number; }
export interface LevelExamResult { level: number; correct: number; total: number; overall_percent: number; passed: boolean; skills: LevelExamSkillResult[]; completed_at: string; }
export interface LevelExamAttempt {
  attempt_id: string; exam_id: string; level: number; status: 'in_progress' | 'completed';
  questions: LevelExamQuestion[]; selections: Record<string, string>;
  flagged_question_ids: string[]; current_index: number; started_at: string;
  result: LevelExamResult | null;
}
export interface LevelExamStatus {
  eligible: boolean; level: number; passed: boolean; in_progress: LevelExamAttempt | null;
  latest_result: LevelExamResult | null; reason_vi: string;
}
