export interface PathLessonSummary {
  id: string;
  number: number;
  title: string;
  goal: string;
  estimated_minutes: number;
}

export interface LearningDaySummary {
  day_number: number;
  level: number;
  difficulty: number;
  lesson_start: number;
  lesson_end: number;
  lesson_ids: string[];
  checkpoint_id: string;
  completed_lesson_count: number;
  topic_vocabulary_completed: boolean;
  checkpoint_completed: boolean;
  status: 'completed' | 'current';
}

export interface LearningPath {
  level: number;
  lessons: PathLessonSummary[];
  current_level: number;
  current_path_index: number;
  current_day_number: number;
  current_difficulty: number;
  checkpoint_start: number;
  completed_all_levels: boolean;
  level_exam_required?: boolean;
  level_exam_level?: number | null;
  days: LearningDaySummary[];
}

export interface DialogueLine {
  id: string;
  speaker: string;
  hanzi: string;
  audio_text: string;
  pinyin: string;
  translation_vi: string;
}

export interface ContentOption {
  id: string;
  text: string;
}

export interface ListeningActivity {
  id: string;
  audio_text: string;
  prompt_vi: string;
  options: ContentOption[];
  correct_option_id: string;
  transcript_zh: string;
  pinyin: string;
  translation_vi: string;
  explanation_vi: string;
}

export interface SentenceOrderActivity {
  id: string;
  prompt_vi: string;
  tokens: string[];
  correct_tokens: string[];
  pinyin: string;
  translation_vi: string;
  explanation_vi: string;
}

export interface LessonWord {
  id: string;
  hanzi: string;
  pinyin: string;
  meaning_vi: string;
}

export interface MultiActivityLesson extends PathLessonSummary {
  level: number;
  dialogue: DialogueLine[];
  listening: ListeningActivity;
  sentence_order: SentenceOrderActivity;
  vocabulary: LessonWord[];
  pronunciation_text: string;
}

export type CheckpointKind = 'listening' | 'vocabulary' | 'sentence-order';

export interface CheckpointQuestion {
  id: string;
  kind: CheckpointKind;
  prompt_vi: string;
  audio_text: string | null;
  options: ContentOption[];
  tokens: string[];
  correct_answer: string;
  explanation_vi: string;
}

export interface Checkpoint {
  id: string;
  title: string;
  lesson_ids: string[];
  questions: CheckpointQuestion[];
}

export interface DailyPathBundle {
  path_index: number;
  level: number;
  difficulty: number;
  lessons: MultiActivityLesson[];
  checkpoint: Checkpoint;
}
