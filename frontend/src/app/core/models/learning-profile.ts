export interface StreakState {
  current: number;
  longest: number;
  lastActiveDate: string | null;
}

export interface ReviewCard {
  id: string;
  hanzi: string;
  pinyin: string;
  meaningVi: string;
  sourceLessonId: string;
  repetitions: number;
  intervalDays: number;
  dueDate: string;
  lastReviewedAt?: string;
}

export interface ActivityEvent {
  kind: 'lesson' | 'checkpoint' | 'review' | 'pronunciation';
  occurredAt: string;
  score?: number;
}

export interface MistakeRecord {
  id: string;
  sourceLessonId: string;
  kind: 'listening' | 'sentence-order' | 'checkpoint';
  prompt: string;
  correctAnswer: string;
  explanationVi: string;
}

export interface NotebookWord {
  id: string;
  hanzi: string;
  pinyin: string;
  meaningVi: string;
  sourceLessonId: string;
  savedAt: string;
}

export interface CheckpointResult {
  checkpointId: string;
  score: number;
  total: number;
  completedAt: string;
}

export interface LearningProfile {
  version: 1;
  completedLessonIds: string[];
  streak: StreakState;
  reviewCards: ReviewCard[];
  mistakes: MistakeRecord[];
  notebook: NotebookWord[];
  checkpointResults: CheckpointResult[];
  activityEvents: ActivityEvent[];
}

export const createEmptyLearningProfile = (): LearningProfile => ({
  version: 1,
  completedLessonIds: [],
  streak: { current: 0, longest: 0, lastActiveDate: null },
  reviewCards: [],
  mistakes: [],
  notebook: [],
  checkpointResults: [],
  activityEvents: [],
});
