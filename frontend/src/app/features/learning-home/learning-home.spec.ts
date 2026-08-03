import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';
import { vi } from 'vitest';

import { LearningPathApiService } from '../../core/services/learning-path-api.service';
import { LearningProfileRepository } from '../../core/services/learning-profile.repository';
import { LearningHome } from './learning-home';
import { LearningAnalyticsService } from '../../core/services/learning-analytics.service';


const path = {
  level: 1 as const,
  current_level: 1,
  current_path_index: 1,
  current_day_number: 1,
  current_difficulty: 1,
  checkpoint_start: 1,
  completed_all_levels: false,
  days: [{
    day_number: 1,
    level: 1,
    difficulty: 1,
    lesson_start: 1,
    lesson_end: 5,
    lesson_ids: Array.from({ length: 5 }, (_, index) => `hsk1-lesson-${index + 1}`),
    checkpoint_id: 'hsk1-checkpoint-1-5',
    completed_lesson_count: 0,
    topic_vocabulary_completed: true,
    checkpoint_completed: false,
    status: 'current' as const,
  }],
  lessons: Array.from({ length: 5 }, (_, index) => ({
    id: `hsk1-lesson-${index + 1}`,
    number: index + 1,
    title: `Bài ${index + 1}`,
    goal: 'Mục tiêu',
    estimated_minutes: 10,
  })),
};

const insights = {
  activity_days: [
    { date: '2026-07-25', active: false, count: 0 },
    { date: '2026-07-26', active: false, count: 0 },
    { date: '2026-07-27', active: true, count: 1 },
    { date: '2026-07-28', active: false, count: 0 },
    { date: '2026-07-29', active: true, count: 2 },
    { date: '2026-07-30', active: true, count: 1 },
    { date: '2026-07-31', active: true, count: 2 },
  ],
  retention_30d: {
    rate: 0.75,
    sample_size: 12,
    remembered: 9,
    label_vi: 'Nhớ 9/12 từ trong 30 ngày',
  },
  weaknesses: [{
    skill: 'listening' as const,
    label_vi: 'Nghe',
    evidence_count: 3,
    severity: 3,
    reason_vi: 'Có 3 dấu hiệu cần luyện thêm.',
  }],
  recommendation: {
    title: 'Ôn lại nghe',
    reason_vi: 'Có 3 dấu hiệu cần luyện thêm.',
    route: '/learn/review',
    query_params: { source: 'mistakes' },
  },
};

describe('LearningHome', () => {
  it('shows topic vocabulary as a required day step before the checkpoint', async () => {
    localStorage.clear();
    const topicRequiredPath = {
      ...path,
      days: [{ ...path.days[0], topic_vocabulary_completed: false }],
    };
    await TestBed.configureTestingModule({
      imports: [LearningHome],
      providers: [
        provideRouter([]),
        { provide: LearningPathApiService, useValue: { getPath: () => of(topicRequiredPath) } },
        { provide: LearningAnalyticsService, useValue: { getInsights: () => of(insights) } },
      ],
    }).compileComponents();
    TestBed.inject(LearningProfileRepository).update((profile) => ({
      ...profile,
      completedLessonIds: path.lessons.map((lesson) => lesson.id),
    }));

    const fixture = TestBed.createComponent(LearningHome);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    expect(element.querySelector('[data-testid="next-action"]')?.getAttribute('href'))
      .toContain('/learn/topics');
    expect(element.querySelector('[data-testid="mandatory-topic-step"]')?.textContent)
      .toContain('10 từ theo chủ đề');
    expect(element.querySelector('[data-testid="mandatory-topic-step"]')?.textContent)
      .toContain('Bắt buộc');
    expect(element.textContent).toContain('Hoàn thành 10 từ theo chủ đề để mở checkpoint');
  });

  it('shows streak, lesson progress and the prioritized next action', async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [LearningHome],
      providers: [
        provideRouter([]),
        { provide: LearningPathApiService, useValue: { getPath: () => of(path) } },
        { provide: LearningAnalyticsService, useValue: { getInsights: () => of(insights) } },
      ],
    }).compileComponents();
    const repository = TestBed.inject(LearningProfileRepository);
    repository.update((profile) => ({
      ...profile,
      completedLessonIds: ['hsk1-lesson-1', 'hsk1-lesson-2'],
      streak: { current: 3, longest: 3, lastActiveDate: '2026-07-30' },
    }));

    const fixture = TestBed.createComponent(LearningHome);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    expect(element.textContent).toContain('Chuỗi 3 ngày');
    expect(element.textContent).toContain('2 / 5 bài');
    expect(element.textContent).toContain('40%');
    expect(element.textContent).toContain('Ngày 1');
    expect(element.querySelector('[data-testid="learning-day-1"]')).not.toBeNull();
    expect(element.querySelector('[data-testid="next-action"]')?.getAttribute('href')).toBe('/learn/lesson/3');
    expect(element.querySelector('[data-testid="open-notebook"]')?.getAttribute('href')).toBe('/learn/notebook');
    const flipcardLink = element.querySelector('[data-testid="open-flipcard-review"]');
    expect(flipcardLink?.getAttribute('href')).toContain('/learn/review');
    expect(flipcardLink?.getAttribute('href')).toContain('source=srs');
    expect(flipcardLink?.textContent).toContain('Ôn từ bằng flipcard');
    expect(element.querySelector('[data-testid="open-mistake-review"]')?.getAttribute('href'))
      .toContain('source=mistakes');
    expect(element.querySelector('[data-testid="open-placement"]')?.getAttribute('href'))
      .toBe('/learn/placement');
  });

  it('prioritizes the optional placement test before a new learner starts', async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [LearningHome],
      providers: [
        provideRouter([]),
        { provide: LearningPathApiService, useValue: { getPath: () => of(path) } },
        { provide: LearningAnalyticsService, useValue: { getInsights: () => of(insights) } },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(LearningHome);
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelector('[data-testid="placement-entry"]')).not.toBeNull();
    expect(fixture.nativeElement.textContent).toContain('Xác định điểm bắt đầu phù hợp');
  });

  it('automatically requests and displays the next five-lesson chunk', async () => {
    localStorage.clear();
    const nextPath = {
      ...path,
      current_level: 2,
      current_path_index: 2,
      current_day_number: 2,
      checkpoint_start: 6,
      days: [
        {
          ...path.days[0],
          completed_lesson_count: 5,
          checkpoint_completed: true,
          status: 'completed' as const,
        },
        {
          day_number: 2,
          level: 2,
          difficulty: 1,
          lesson_start: 6,
          lesson_end: 10,
          lesson_ids: Array.from({ length: 5 }, (_, index) => `hsk2-lesson-${index + 6}`),
          checkpoint_id: 'hsk2-checkpoint-6-10',
          completed_lesson_count: 0,
          checkpoint_completed: false,
          status: 'current' as const,
        },
      ],
      lessons: [
        ...path.lessons,
        ...Array.from({ length: 5 }, (_, index) => ({
          id: `hsk2-lesson-${index + 6}`,
          number: index + 6,
          title: `Bài ${index + 6}`,
          goal: 'Mục tiêu mới',
          estimated_minutes: 10,
        })),
      ],
    };
    const getPath = vi
      .fn()
      .mockReturnValueOnce(of(path))
      .mockReturnValueOnce(of(nextPath));
    const createNextPath = vi.fn().mockReturnValue(of({}));
    await TestBed.configureTestingModule({
      imports: [LearningHome],
      providers: [
        provideRouter([]),
        {
          provide: LearningPathApiService,
          useValue: { getPath, createNextPath },
        },
        { provide: LearningAnalyticsService, useValue: { getInsights: () => of(insights) } },
      ],
    }).compileComponents();
    TestBed.inject(LearningProfileRepository).update((profile) => ({
      ...profile,
      completedLessonIds: path.lessons.map((lesson) => lesson.id),
      checkpointResults: [
        {
          checkpointId: 'hsk1-checkpoint-1-5',
          score: 5,
          total: 5,
          completedAt: '2026-07-30',
        },
      ],
    }));

    const fixture = TestBed.createComponent(LearningHome);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();

    expect(createNextPath).toHaveBeenCalledOnce();
    expect(fixture.nativeElement.textContent).toContain('5 / 10 bài');
    expect(fixture.nativeElement.textContent).toContain('HSK 2');
    expect(fixture.nativeElement.textContent).toContain('Ngày 2');
    expect(
      fixture.nativeElement.querySelectorAll('[data-testid^="learning-day-"]'),
    ).toHaveLength(2);
    expect(
      fixture.nativeElement
        .querySelector('[data-testid="next-action"]')
        ?.getAttribute('href'),
    ).toBe('/learn/lesson/6');
  });

  it('keeps the completed day and offers a Vietnamese retry when generation fails', async () => {
    localStorage.clear();
    const createNextPath = vi.fn().mockReturnValue(
      throwError(() => ({ error: {} })),
    );
    await TestBed.configureTestingModule({
      imports: [LearningHome],
      providers: [
        provideRouter([]),
        {
          provide: LearningPathApiService,
          useValue: { getPath: () => of(path), createNextPath },
        },
        { provide: LearningAnalyticsService, useValue: { getInsights: () => of(insights) } },
      ],
    }).compileComponents();
    TestBed.inject(LearningProfileRepository).update((profile) => ({
      ...profile,
      completedLessonIds: path.lessons.map((lesson) => lesson.id),
      checkpointResults: [
        {
          checkpointId: 'hsk1-checkpoint-1-5',
          score: 5,
          total: 5,
          completedAt: '2026-07-30',
        },
      ],
    }));

    const fixture = TestBed.createComponent(LearningHome);
    fixture.detectChanges();

    expect(createNextPath).toHaveBeenCalledOnce();
    expect(fixture.nativeElement.textContent).toContain(
      'AI chưa thể tạo Ngày 2. Vui lòng thử lại.',
    );
    expect(
      fixture.nativeElement.querySelector('[data-testid="learning-day-1"]'),
    ).not.toBeNull();
    expect(
      fixture.nativeElement.querySelector('[data-testid="generate-next-path"]')
        ?.textContent,
    ).toContain('Thử lại');
  });

  it('shows 7-day activity, 30-day retention and one weakness recommendation', async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [LearningHome],
      providers: [
        provideRouter([]),
        { provide: LearningPathApiService, useValue: { getPath: () => of(path) } },
        { provide: LearningAnalyticsService, useValue: { getInsights: () => of(insights) } },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(LearningHome);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    expect(element.querySelectorAll('[data-testid="activity-day"]')).toHaveLength(7);
    expect(element.textContent).toContain('Nhớ 9/12 từ trong 30 ngày');
    expect(element.textContent).toContain('Kỹ năng cần ưu tiên');
    expect(element.textContent).toContain('Ôn lại nghe');
    expect(
      element.querySelector('[data-testid="insight-recommendation"]')
        ?.getAttribute('href'),
    ).toContain('source=mistakes');
  });

  it('keeps the learning path usable when analytics fails', async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [LearningHome],
      providers: [
        provideRouter([]),
        { provide: LearningPathApiService, useValue: { getPath: () => of(path) } },
        {
          provide: LearningAnalyticsService,
          useValue: { getInsights: () => throwError(() => new Error('offline')) },
        },
      ],
    }).compileComponents();

    const fixture = TestBed.createComponent(LearningHome);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Phân tích tiến độ tạm thời chưa có');
    expect(
      fixture.nativeElement.querySelector('[data-testid="next-action"]')
        ?.getAttribute('href'),
    ).toBe('/learn/lesson/1');
  });
});
