import { TestBed } from '@angular/core/testing';

import { Lesson } from '../models/lesson';
import { StudySessionService } from './study-session.service';

const lesson: Lesson = {
  id: 'lesson',
  level: 1,
  title: 'Bài học',
  goal: 'Mục tiêu',
  estimated_minutes: 5,
  source: 'fallback',
  cards: Array.from({ length: 5 }, (_, index) => ({
    id: `card-${index + 1}`,
    hanzi: `字${index + 1}`,
    pinyin: 'zì',
    sino_vietnamese: 'tự',
    meaning_vi: `từ ${index + 1}`,
    example_zh: '例子',
    example_vi: 'Ví dụ',
  })),
};

describe('StudySessionService', () => {
  beforeEach(() => {
    sessionStorage.clear();
    TestBed.configureTestingModule({});
  });

  it('starts at the first hidden card and rejects rating before reveal', () => {
    const service = TestBed.inject(StudySessionService);

    service.start(lesson);

    expect(service.currentCard()?.id).toBe('card-1');
    expect(service.currentPosition()).toBe(1);
    expect(service.totalCards()).toBe(5);
    expect(service.revealed()).toBe(false);
    expect(() => service.rate('remembered')).toThrowError(/lật thẻ/i);
  });

  it('advances exactly once after a revealed card is rated', () => {
    const service = TestBed.inject(StudySessionService);
    service.start(lesson);

    service.reveal();
    const completed = service.rate('remembered');

    expect(completed).toBe(false);
    expect(service.currentCard()?.id).toBe('card-2');
    expect(service.currentPosition()).toBe(2);
    expect(service.revealed()).toBe(false);
  });

  it('calculates results and completes after the fifth rating', () => {
    const service = TestBed.inject(StudySessionService);
    service.start(lesson);

    const ratings = ['remembered', 'review', 'remembered', 'review', 'remembered'] as const;
    ratings.forEach((rating, index) => {
      service.reveal();
      expect(service.rate(rating)).toBe(index === 4);
    });

    expect(service.results()).toEqual({
      total: 5,
      remembered: 3,
      review: 2,
      reviewCards: [lesson.cards[1], lesson.cards[3]],
    });
  });

  it('starts a review session with only unremembered cards', () => {
    const service = TestBed.inject(StudySessionService);
    service.start(lesson);
    for (const rating of ['remembered', 'review', 'remembered', 'review', 'remembered'] as const) {
      service.reveal();
      service.rate(rating);
    }

    service.startReview();

    expect(service.totalCards()).toBe(2);
    expect(service.currentCard()?.id).toBe('card-2');
  });

  it('restores an active session from browser session storage', () => {
    const first = TestBed.inject(StudySessionService);
    first.start(lesson);
    first.reveal();
    first.rate('remembered');
    TestBed.resetTestingModule();
    TestBed.configureTestingModule({});

    const restored = TestBed.inject(StudySessionService);

    expect(restored.currentCard()?.id).toBe('card-2');
    expect(restored.currentPosition()).toBe(2);
    expect(restored.results().remembered).toBe(1);
  });
});
