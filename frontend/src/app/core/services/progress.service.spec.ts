import { TestBed } from '@angular/core/testing';

import { LearningPath } from '../models/learning-content';
import { LearningProfileRepository } from './learning-profile.repository';
import { ProgressService } from './progress.service';


function pathWith(count: number, currentLevel = 1): LearningPath {
  return {
    level: currentLevel,
    current_level: currentLevel,
    current_path_index: count / 5,
    current_day_number: count / 5,
    current_difficulty: 1,
    checkpoint_start: count - 4,
    completed_all_levels: false,
    lessons: Array.from({ length: count }, (_, index) => ({
      id: `hsk${index < 5 ? 1 : currentLevel}-lesson-${index + 1}`,
      number: index + 1,
      title: `Bài ${index + 1}`,
      goal: 'Mục tiêu',
      estimated_minutes: 10,
    })),
    days: Array.from({ length: count / 5 }, (_, dayIndex) => {
      const start = dayIndex * 5 + 1;
      const level = dayIndex === 0 ? 1 : currentLevel;
      return {
        day_number: dayIndex + 1,
        level,
        difficulty: 1,
        lesson_start: start,
        lesson_end: start + 4,
        lesson_ids: Array.from(
          { length: 5 },
          (_, lessonIndex) =>
            `hsk${level}-lesson-${start + lessonIndex}`,
        ),
        checkpoint_id: `hsk${level}-checkpoint-${start}-${start + 4}`,
        completed_lesson_count: 0,
        checkpoint_completed: false,
        status: dayIndex === count / 5 - 1 ? 'current' as const : 'completed' as const,
      };
    }),
  };
}

describe('ProgressService', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({});
  });

  it('unlocks the checkpoint for the latest five-lesson chunk', () => {
    const progress = TestBed.inject(ProgressService);
    const path = pathWith(10, 2);
    for (let lesson = 1; lesson <= 10; lesson += 1) {
      progress.completeLesson(
        `hsk${lesson <= 5 ? 1 : 2}-lesson-${lesson}`,
        '2026-07-25',
      );
    }

    expect(progress.completedCountFor(path)).toBe(10);
    expect(progress.completionRateFor(path)).toBe(100);
    expect(progress.pendingCheckpointIdFor(path)).toBe('hsk2-checkpoint-6-10');
  });

  it('increments consecutive days and resets after a missed day', () => {
    const progress = TestBed.inject(ProgressService);
    progress.recordActivity('2026-07-20');
    progress.recordActivity('2026-07-21');
    expect(progress.streak()).toBe(2);

    progress.recordActivity('2026-07-23');
    expect(progress.streak()).toBe(1);
    expect(TestBed.inject(LearningProfileRepository).profile().streak.longest).toBe(2);
  });

  it('does not increment the streak twice when two learning days finish on one date', () => {
    const progress = TestBed.inject(ProgressService);

    progress.recordActivity('2026-07-20');
    progress.recordActivity('2026-07-20');
    progress.completeCheckpoint('hsk1-checkpoint-1-5', 5, 5, '2026-07-20');
    progress.completeCheckpoint('hsk1-checkpoint-6-10', 5, 5, '2026-07-20');

    expect(progress.streak()).toBe(1);
  });

  it('continues with lesson 6 when the generated chunk is available', () => {
    const progress = TestBed.inject(ProgressService);
    const path = pathWith(10, 2);
    for (let lesson = 1; lesson <= 5; lesson += 1) {
      progress.completeLesson(`hsk1-lesson-${lesson}`, '2026-07-20');
    }
    progress.completeCheckpoint('hsk1-checkpoint-1-5', 5, 5, '2026-07-20');

    expect(progress.nextAction(path, '2026-07-20')).toEqual({
      kind: 'lesson',
      title: 'Tiếp tục Bài 6',
      route: '/learn/lesson/6',
    });
  });

  it('requests generation after finishing the current chunk and checkpoint', () => {
    const progress = TestBed.inject(ProgressService);
    const path = pathWith(5);
    for (let lesson = 1; lesson <= 5; lesson += 1) {
      progress.completeLesson(`hsk1-lesson-${lesson}`, '2026-07-20');
    }
    progress.completeCheckpoint('hsk1-checkpoint-1-5', 5, 5, '2026-07-20');

    expect(progress.nextAction(path, '2026-07-20')).toEqual({
      kind: 'generate',
      title: 'Đang chuẩn bị Ngày 2',
      route: '/learn',
    });
  });

  it('routes to the level exam before generating a promoted path', () => {
    const progress = TestBed.inject(ProgressService);
    const path = { ...pathWith(5), level_exam_required: true, level_exam_level: 1 };
    for (const lesson of path.lessons) progress.completeLesson(lesson.id, '2026-07-20');
    progress.completeCheckpoint(path.days[0].checkpoint_id, 5, 5, '2026-07-20');
    expect(progress.nextAction(path, '2026-07-20')).toEqual({
      kind: 'level-exam', title: 'Làm bài thi tổng kết HSK 1', route: '/learn/level-exam',
    });
  });

  it('routes to the latest checkpoint with its start number', () => {
    const progress = TestBed.inject(ProgressService);
    const path = pathWith(10, 2);
    for (let lesson = 1; lesson <= 10; lesson += 1) {
      progress.completeLesson(
        `hsk${lesson <= 5 ? 1 : 2}-lesson-${lesson}`,
        '2026-07-20',
      );
    }

    expect(progress.nextAction(path, '2026-07-20')).toEqual({
      kind: 'checkpoint',
      title: 'Làm checkpoint Bài 6–10',
      route: '/learn/checkpoint',
      queryParams: { start: 6 },
    });
  });

  it('stops generating days after the HSK 6 journey is complete', () => {
    const progress = TestBed.inject(ProgressService);
    const path = {
      ...pathWith(5, 6),
      current_level: 6,
      completed_all_levels: true,
    };
    for (const lesson of path.lessons) {
      progress.completeLesson(lesson.id, '2026-07-20');
    }
    progress.completeCheckpoint(
      path.days[0].checkpoint_id,
      5,
      5,
      '2026-07-20',
    );

    expect(progress.nextAction(path, '2026-07-20')).toEqual({
      kind: 'complete',
      title: 'Bạn đã hoàn thành lộ trình HSK 1–6',
      route: '/learn/notebook',
    });
  });
});
