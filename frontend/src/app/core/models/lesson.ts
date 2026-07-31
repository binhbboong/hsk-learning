export interface VocabularyCard {
  id: string;
  hanzi: string;
  pinyin: string;
  sino_vietnamese: string;
  meaning_vi: string;
  example_zh: string;
  example_vi: string;
}

export interface Lesson {
  id: string;
  level: 1;
  title: string;
  goal: string;
  estimated_minutes: number;
  cards: VocabularyCard[];
  source: 'ai' | 'fallback';
}
