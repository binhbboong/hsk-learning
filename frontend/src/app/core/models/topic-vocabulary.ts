export interface TopicRecommendation {
  id: string;
  name_vi: string;
  description_vi: string;
  reason_vi: string;
  word_count: 10;
  level: number;
  learned_count: number;
  remembered_count: number;
}

export interface TopicRecommendationsResponse {
  source: 'ai' | 'curated';
  items: TopicRecommendation[];
}

export interface TopicVocabularyWord {
  id: string;
  hanzi: string;
  pinyin: string;
  sino_vietnamese: string;
  meaning_vi: string;
  example_zh: string;
  example_vi: string;
  audio_text: string;
  example_audio_text: string;
  is_extension: boolean;
}

export interface TopicVocabularySession {
  id: string;
  topic_id: string;
  topic_name_vi: string;
  level: number;
  source: 'ai' | 'curated';
  words: TopicVocabularyWord[];
}
