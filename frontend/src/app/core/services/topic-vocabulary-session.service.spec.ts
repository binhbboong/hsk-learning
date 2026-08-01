import { TestBed } from '@angular/core/testing';

import { TopicVocabularySession } from '../models/topic-vocabulary';
import { LearningProfileRepository } from './learning-profile.repository';
import { ProgressService } from './progress.service';
import { ReviewQuizService } from './review-quiz.service';
import { SrsService } from './srs.service';
import { TopicVocabularySessionService } from './topic-vocabulary-session.service';


const session: TopicVocabularySession = {
  id: 'greetings-session-1',
  topic_id: 'greetings',
  topic_name_vi: 'Chào hỏi',
  level: 1,
  source: 'curated',
  words: Array.from({ length: 10 }, (_, index) => ({
    id: `word:${index}`,
    hanzi: `词${index}`,
    pinyin: `cí ${index}`,
    sino_vietnamese: 'TỪ',
    meaning_vi: `nghĩa ${index}`,
    example_zh: `这是词${index}。`,
    example_vi: `Đây là từ ${index}.`,
    audio_text: `词${index}`,
    example_audio_text: `这是词${index}。`,
    is_extension: false,
  })),
};

describe('TopicVocabularySessionService', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({});
  });

  it('moves from ten viewed flipcards to the active-recall round', () => {
    const service = TestBed.inject(TopicVocabularySessionService);
    service.open(session);

    for (let index = 0; index < 10; index += 1) service.completeCurrentCard();

    expect(service.progress()?.phase).toBe('quiz');
    expect(service.progress()?.cardIndex).toBe(10);
    expect(service.progress()?.quizIndex).toBe(0);
  });

  it('creates four unique answers and only advances when continued', () => {
    const service = TestBed.inject(TopicVocabularySessionService);
    service.open(session);
    for (let index = 0; index < 10; index += 1) service.completeCurrentCard();

    expect(service.options()).toHaveLength(4);
    expect(new Set(service.options()).size).toBe(4);
    expect(service.answer('sai').correct).toBe(false);
    expect(service.progress()?.quizIndex).toBe(0);

    service.continueQuiz();
    expect(service.progress()?.quizIndex).toBe(1);
  });

  it('completes once, schedules unique SRS cards and records topic activity', () => {
    const service = TestBed.inject(TopicVocabularySessionService);
    const repository = TestBed.inject(LearningProfileRepository);
    service.open(session);
    for (let index = 0; index < 10; index += 1) service.completeCurrentCard();
    for (let index = 0; index < 10; index += 1) {
      service.answer(session.words[index].meaning_vi);
      service.continueQuiz('2026-08-01');
    }

    const profile = repository.profile();
    expect(service.progress()?.phase).toBe('completed');
    expect(profile.reviewCards).toHaveLength(10);
    expect(new Set(profile.reviewCards.map((card) => card.id)).size).toBe(10);
    expect(profile.activityEvents.filter((event) => event.kind === 'topic-vocabulary')).toHaveLength(1);
    expect(profile.completedLessonIds).toEqual([]);
    expect(profile.checkpointResults).toEqual([]);
  });

  it('restores the saved phase and index when the session is reopened', () => {
    const first = TestBed.inject(TopicVocabularySessionService);
    first.open(session);
    first.completeCurrentCard();
    first.completeCurrentCard();

    const restored = new TopicVocabularySessionService(
      TestBed.inject(LearningProfileRepository),
      TestBed.inject(ReviewQuizService),
      TestBed.inject(SrsService),
      TestBed.inject(ProgressService),
    );
    restored.open(session);

    expect(restored.progress()?.cardIndex).toBe(2);
  });

  it('reuses an existing notebook word identity instead of creating a duplicate', () => {
    const repository = TestBed.inject(LearningProfileRepository);
    repository.update((profile) => ({
      ...profile,
      notebook: [{
        id: 'lesson-existing-word',
        hanzi: session.words[0].hanzi,
        pinyin: session.words[0].pinyin,
        meaningVi: session.words[0].meaning_vi,
        sourceLessonId: 'hsk1-lesson-1',
        savedAt: '2026-07-01T00:00:00Z',
      }],
    }));
    const service = TestBed.inject(TopicVocabularySessionService);
    service.open(session);
    for (let index = 0; index < 10; index += 1) service.completeCurrentCard();

    service.answer(session.words[0].meaning_vi);

    expect(repository.profile().reviewCards).toHaveLength(1);
    expect(repository.profile().reviewCards[0].id).toBe('lesson-existing-word');
  });
});
