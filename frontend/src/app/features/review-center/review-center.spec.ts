import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, provideRouter } from '@angular/router';
import { vi } from 'vitest';

import { LearningProfileRepository } from '../../core/services/learning-profile.repository';
import { MistakeService } from '../../core/services/mistake.service';
import { ReviewCenter } from './review-center';

describe('ReviewCenter', () => {
  beforeEach(async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [ReviewCenter],
      providers: [
        provideRouter([]),
        { provide: ActivatedRoute, useValue: { snapshot: { queryParamMap: { get: () => null } } } },
      ],
    }).compileComponents();
  });

  it('reviews only due cards and reschedules a remembered card', () => {
    TestBed.inject(LearningProfileRepository).update((profile) => ({
      ...profile,
      reviewCards: [
        {
          id: 'due',
          hanzi: '你',
          pinyin: 'nǐ',
          meaningVi: 'bạn',
          sourceLessonId: 'lesson-1',
          repetitions: 0,
          intervalDays: 1,
          dueDate: '2000-01-01',
        },
        {
          id: 'later',
          hanzi: '好',
          pinyin: 'hǎo',
          meaningVi: 'tốt',
          sourceLessonId: 'lesson-1',
          repetitions: 1,
          intervalDays: 7,
          dueDate: '2999-01-01',
        },
      ],
    }));
    const fixture = TestBed.createComponent(ReviewCenter);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('你');
    expect(fixture.nativeElement.textContent).not.toContain('好');
    fixture.componentInstance.chooseAnswer(fixture.componentInstance.currentCard()!.meaningVi);
    fixture.componentInstance.continueReview();
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Đã hoàn thành lượt ôn hôm nay');
  });

  it('automatically advances to the next flashcard after a correct answer', () => {
    vi.useFakeTimers();
    try {
      TestBed.inject(LearningProfileRepository).update((profile) => ({
        ...profile,
        reviewCards: [
          {
            id: 'first',
            hanzi: '你',
            pinyin: 'nǐ',
            meaningVi: 'bạn',
            sourceLessonId: 'lesson-1',
            repetitions: 0,
            intervalDays: 1,
            dueDate: '2000-01-01',
          },
          {
            id: 'second',
            hanzi: '好',
            pinyin: 'hǎo',
            meaningVi: 'tốt',
            sourceLessonId: 'lesson-1',
            repetitions: 0,
            intervalDays: 1,
            dueDate: '2000-01-01',
          },
        ],
      }));
      const fixture = TestBed.createComponent(ReviewCenter);
      fixture.detectChanges();

      fixture.componentInstance.chooseAnswer(fixture.componentInstance.currentCard()!.meaningVi);

      expect(fixture.componentInstance.currentCard()?.id).toBe('first');
      expect(fixture.componentInstance.revealed()).toBe(true);

      vi.advanceTimersByTime(1000);
      fixture.detectChanges();

      expect(fixture.componentInstance.currentCard()?.id).toBe('second');
      expect(fixture.nativeElement.textContent).toContain('好');
    } finally {
      vi.useRealTimers();
    }
  });

  it('automatically advances to the next notebook word after a correct answer', () => {
    vi.useFakeTimers();
    try {
      TestBed.inject(LearningProfileRepository).update((profile) => ({
        ...profile,
        notebook: [
          {
            id: 'notebook-first',
            hanzi: '你',
            pinyin: 'nǐ',
            meaningVi: 'bạn',
            sourceLessonId: 'lesson-1',
            savedAt: '2026-07-01T00:00:00Z',
          },
          {
            id: 'notebook-second',
            hanzi: '好',
            pinyin: 'hǎo',
            meaningVi: 'tốt',
            sourceLessonId: 'lesson-1',
            savedAt: '2026-07-01T00:00:00Z',
          },
        ],
      }));
      const fixture = TestBed.createComponent(ReviewCenter);
      fixture.componentInstance.setMode('notebook');
      fixture.detectChanges();

      fixture.componentInstance.chooseAnswer(fixture.componentInstance.currentCard()!.meaningVi);
      vi.advanceTimersByTime(1000);
      fixture.detectChanges();

      expect(fixture.componentInstance.currentCard()?.id).toBe('notebook-second');
      expect(fixture.nativeElement.textContent).toContain('好');
    } finally {
      vi.useRealTimers();
    }
  });

  it('shows notebook review completion after the last word is answered', () => {
    vi.useFakeTimers();
    try {
      TestBed.inject(LearningProfileRepository).update((profile) => ({
        ...profile,
        notebook: [
          {
            id: 'only-notebook-word',
            hanzi: '你',
            pinyin: 'nǐ',
            meaningVi: 'bạn',
            sourceLessonId: 'lesson-1',
            savedAt: '2026-07-01T00:00:00Z',
          },
        ],
      }));
      const fixture = TestBed.createComponent(ReviewCenter);
      fixture.componentInstance.setMode('notebook');
      fixture.detectChanges();

      fixture.componentInstance.chooseAnswer('bạn');
      vi.advanceTimersByTime(1000);
      fixture.detectChanges();

      expect(fixture.nativeElement.textContent).toContain('Đã ôn xong các từ trong sổ');
      expect(fixture.nativeElement.textContent).not.toContain('Sổ từ chưa có từ để ôn');
    } finally {
      vi.useRealTimers();
    }
  });

  it('does not claim completion when the learner has no flashcards yet', () => {
    const fixture = TestBed.createComponent(ReviewCenter);
    fixture.detectChanges();
    const text = fixture.nativeElement.textContent;

    expect(text).toContain('Chưa có từ để ôn');
    expect(text).toContain('Học Bài 1');
    expect(text).not.toContain('Đã ôn xong');
  });

  it('resolves a wrong-answer item when answered correctly', () => {
    TestBed.inject(MistakeService).add({
      id: 'q1',
      sourceLessonId: 'lesson-1',
      kind: 'listening',
      prompt: 'Người nói tên gì?',
      correctAnswer: 'Vương Minh',
      explanationVi: 'Nghe cụm 王明.',
    });
    const fixture = TestBed.createComponent(ReviewCenter);
    fixture.detectChanges();
    fixture.componentInstance.setMode('mistakes');
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Người nói tên gì?');
    fixture.componentInstance.answerMistake('Vương Minh');
    fixture.detectChanges();

    expect(TestBed.inject(MistakeService).items()).toHaveLength(0);
  });

  it('lets the learner rebuild a sentence-order mistake from suggested word cards', () => {
    TestBed.inject(MistakeService).add({
      id: 'sentence-1',
      sourceLessonId: 'lesson-1',
      kind: 'sentence-order',
      prompt: 'Sắp xếp câu “Tôi là học sinh”.',
      correctAnswer: '我 是 学生',
      explanationVi: 'Trật tự: chủ ngữ + 是 + danh từ.',
    });
    const fixture = TestBed.createComponent(ReviewCenter);
    fixture.detectChanges();
    fixture.componentInstance.setMode('mistakes');
    fixture.detectChanges();

    const tokenButtons = Array.from(
      fixture.nativeElement.querySelectorAll('[data-testid="mistake-token"]'),
    ) as HTMLButtonElement[];
    expect(tokenButtons.map((button) => button.textContent?.trim()).sort()).toEqual(
      ['学生', '我', '是'].sort(),
    );
    expect(fixture.nativeElement.querySelector('[data-testid="mistake-answer"]')).toBeNull();

    for (const token of ['我', '是', '学生']) {
      tokenButtons.find((button) => button.textContent?.trim() === token)?.click();
    }
    fixture.detectChanges();
    (
      fixture.nativeElement.querySelector(
        '[data-testid="submit-mistake-review"]',
      ) as HTMLButtonElement
    ).click();
    fixture.detectChanges();

    expect(TestBed.inject(MistakeService).items()).toHaveLength(0);
  });

  it('opens the mistake queue directly from its source query', () => {
    TestBed.resetTestingModule();
    TestBed.configureTestingModule({
      imports: [ReviewCenter],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: { snapshot: { queryParamMap: { get: () => 'mistakes' } } },
        },
      ],
    });
    const fixture = TestBed.createComponent(ReviewCenter);

    expect(fixture.componentInstance.mode()).toBe('mistakes');
  });
});
