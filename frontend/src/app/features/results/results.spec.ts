import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';

import { Lesson } from '../../core/models/lesson';
import { StudySessionService } from '../../core/services/study-session.service';
import { Results } from './results';

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

describe('Results', () => {
  let fixture: ComponentFixture<Results>;
  let session: StudySessionService;

  beforeEach(async () => {
    sessionStorage.clear();
    await TestBed.configureTestingModule({
      imports: [Results],
      providers: [provideRouter([])],
    }).compileComponents();
    session = TestBed.inject(StudySessionService);
    session.start(lesson);
    for (const rating of ['remembered', 'review', 'remembered', 'review', 'remembered'] as const) {
      session.reveal();
      session.rate(rating);
    }
    fixture = TestBed.createComponent(Results);
    fixture.detectChanges();
  });

  it('shows consistent totals and the words that need review', () => {
    const element = fixture.nativeElement as HTMLElement;
    const text = element.textContent ?? '';

    expect(text).toContain('5 thẻ');
    expect(text).toContain('3 đã nhớ');
    expect(text).toContain('2 cần ôn');
    expect(text).toContain('字2');
    expect(text).toContain('字4');
    expect(element.querySelector('[data-testid="review-cards"]')).not.toBeNull();
    expect(
      element.querySelector('[data-testid="back-dashboard"]')?.getAttribute('href'),
    ).toBe('/');
  });

  it('starts review with only the unremembered words', () => {
    vi.spyOn(TestBed.inject(Router), 'navigate').mockResolvedValue(true);
    const button = (fixture.nativeElement as HTMLElement).querySelector(
      '[data-testid="review-cards"]',
    ) as HTMLButtonElement;

    button.click();

    expect(session.totalCards()).toBe(2);
    expect(session.currentCard()?.id).toBe('card-2');
  });
});
