export type SkillKind =
  | 'vocabulary'
  | 'grammar'
  | 'listening'
  | 'pronunciation';

export interface SkillSummary {
  kind: SkillKind;
  title: string;
  goal: string;
  estimated_minutes: number;
  route: string;
}

export interface SkillCatalog {
  level: 1;
  items: SkillSummary[];
}

export interface AnswerOption {
  id: string;
  text: string;
}

export interface ChineseExample {
  hanzi: string;
  pinyin: string;
  meaning_vi: string;
}

interface SkillLessonBase {
  id: string;
  level: 1;
  kind: Exclude<SkillKind, 'vocabulary'>;
  title: string;
  goal: string;
  estimated_minutes: number;
}

export interface GrammarQuestion {
  id: string;
  prompt_vi: string;
  options: AnswerOption[];
  correct_option_id: string;
  explanation_vi: string;
}

export interface GrammarLesson extends SkillLessonBase {
  kind: 'grammar';
  pattern: string;
  explanation_vi: string;
  examples: ChineseExample[];
  questions: GrammarQuestion[];
}

export interface ListeningLesson extends SkillLessonBase {
  kind: 'listening';
  utterance_zh: string;
  pinyin: string;
  meaning_vi: string;
  question_vi: string;
  options: AnswerOption[];
  correct_option_id: string;
  explanation_vi: string;
}

export interface PronunciationLesson extends SkillLessonBase {
  kind: 'pronunciation';
  hanzi: string;
  pinyin: string;
  meaning_vi: string;
  tone_path: string[];
  common_mistake_vi: string;
  correction_tip_vi: string;
}

export type SkillLesson =
  | GrammarLesson
  | ListeningLesson
  | PronunciationLesson;
