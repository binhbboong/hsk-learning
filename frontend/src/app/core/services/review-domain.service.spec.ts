import { TestBed } from '@angular/core/testing';

import { LearningProfileRepository } from './learning-profile.repository';
import { MistakeService } from './mistake.service';
import { NotebookService } from './notebook.service';
import { SrsService } from './srs.service';


describe('review domain services', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({});
  });

  it('schedules first reviews at 1, 3 and 7 days', () => {
    const srs = TestBed.inject(SrsService);
    const word = {
      id: 'ni',
      hanzi: '你',
      pinyin: 'nǐ',
      meaningVi: 'bạn',
      sourceLessonId: 'hsk1-lesson-1',
    };

    expect(srs.schedule(word, 'forgot', '2026-07-20').dueDate).toBe('2026-07-21');
    expect(srs.schedule(word, 'hard', '2026-07-20').dueDate).toBe('2026-07-23');
    expect(srs.schedule(word, 'remembered', '2026-07-20').dueDate).toBe('2026-07-27');
  });

  it('increases remembered intervals and resets on forgotten', () => {
    const srs = TestBed.inject(SrsService);
    const word = {
      id: 'ni',
      hanzi: '你',
      pinyin: 'nǐ',
      meaningVi: 'bạn',
      sourceLessonId: 'hsk1-lesson-1',
    };
    srs.schedule(word, 'remembered', '2026-07-20');
    const second = srs.rate('ni', 'remembered', '2026-07-27');
    expect(second.intervalDays).toBeGreaterThan(7);

    const reset = srs.rate('ni', 'forgot', '2026-08-15');
    expect(reset.repetitions).toBe(0);
    expect(reset.intervalDays).toBe(1);
  });

  it('returns only due cards by default', () => {
    const repository = TestBed.inject(LearningProfileRepository);
    repository.update((profile) => ({
      ...profile,
      reviewCards: [
        { id: 'due', hanzi: '你', pinyin: 'nǐ', meaningVi: 'bạn', sourceLessonId: '1', repetitions: 0, intervalDays: 1, dueDate: '2026-07-20' },
        { id: 'later', hanzi: '好', pinyin: 'hǎo', meaningVi: 'tốt', sourceLessonId: '1', repetitions: 0, intervalDays: 7, dueDate: '2026-07-30' },
      ],
    }));

    expect(TestBed.inject(SrsService).dueCards('2026-07-20').map((card) => card.id)).toEqual(['due']);
  });

  it('adds and resolves mistakes', () => {
    const mistakes = TestBed.inject(MistakeService);
    mistakes.add({
      id: 'q1',
      sourceLessonId: 'lesson-1',
      kind: 'listening',
      prompt: 'Người nói tên gì?',
      correctAnswer: 'Vương Minh',
      explanationVi: 'Nghe cụm 我是王明.',
    });
    mistakes.add(mistakes.items()[0]);
    expect(mistakes.items()).toHaveLength(1);

    mistakes.resolve('q1');
    expect(mistakes.items()).toHaveLength(0);
  });

  it('adds and removes personal vocabulary without duplicates', () => {
    const notebook = TestBed.inject(NotebookService);
    const word = {
      id: 'ni',
      hanzi: '你',
      pinyin: 'nǐ',
      meaningVi: 'bạn',
      sourceLessonId: 'lesson-1',
    };
    notebook.add(word, '2026-07-20T08:00:00Z');
    notebook.add(word, '2026-07-20T08:00:00Z');
    expect(notebook.words()).toHaveLength(1);

    notebook.remove('ni');
    expect(notebook.words()).toHaveLength(0);
  });
});
