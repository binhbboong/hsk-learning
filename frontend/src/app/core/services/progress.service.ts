import { computed, inject, Injectable } from '@angular/core';

import { LearningDaySummary, LearningPath } from '../models/learning-content';
import { LearningProfileRepository } from './learning-profile.repository';


export type NextActionKind =
  | 'checkpoint'
  | 'review'
  | 'lesson'
  | 'generate'
  | 'level-exam'
  | 'complete';

export interface NextLearningAction {
  kind: NextActionKind;
  title: string;
  route: string;
  count?: number;
  queryParams?: Record<string, number>;
}

@Injectable({ providedIn: 'root' })
export class ProgressService {
  private readonly repository = inject(LearningProfileRepository);

  readonly completedCount = computed(
    () => this.repository.profile().completedLessonIds.length,
  );
  readonly streak = computed(() => this.repository.profile().streak.current);

  completedCountFor(path: LearningPath): number {
    const completed = new Set(this.repository.profile().completedLessonIds);
    return path.lessons.filter((lesson) => completed.has(lesson.id)).length;
  }

  completionRateFor(path: LearningPath): number {
    if (!path.lessons.length) return 0;
    return Math.round((this.completedCountFor(path) / path.lessons.length) * 100);
  }

  completedCountForDay(day: LearningDaySummary): number {
    const completed = new Set(this.repository.profile().completedLessonIds);
    return day.lesson_ids.filter((id) => completed.has(id)).length;
  }

  isDayCompleted(day: LearningDaySummary): boolean {
    const profile = this.repository.profile();
    return (
      this.completedCountForDay(day) === 5 &&
      profile.checkpointResults.some(
        (result) => result.checkpointId === day.checkpoint_id,
      )
    );
  }

  pendingCheckpointIdFor(path: LearningPath): string | null {
    const currentDay = path.days.find(
      (day) => day.day_number === path.current_day_number,
    );
    if (!currentDay) return null;
    const profile = this.repository.profile();
    if (
      !currentDay.lesson_ids.every((id) =>
        profile.completedLessonIds.includes(id),
      )
    ) {
      return null;
    }
    return profile.checkpointResults.some(
      (result) => result.checkpointId === currentDay.checkpoint_id,
    )
      ? null
      : currentDay.checkpoint_id;
  }

  completeLesson(lessonId: string, activityDate = this.today()): void {
    this.repository.update((profile) => ({
      ...profile,
      completedLessonIds: profile.completedLessonIds.includes(lessonId)
        ? profile.completedLessonIds
        : [...profile.completedLessonIds, lessonId],
    }));
    this.recordActivity(activityDate, 'lesson');
  }

  completeCheckpoint(
    checkpointId: string,
    score: number,
    total: number,
    completedAt = this.today(),
  ): void {
    this.repository.update((profile) => ({
      ...profile,
      checkpointResults: [
        ...profile.checkpointResults.filter(
          (result) => result.checkpointId !== checkpointId,
        ),
        { checkpointId, score, total, completedAt },
      ],
    }));
    this.recordActivity(completedAt, 'checkpoint');
  }

  recordActivity(
    activityDate = this.today(),
    kind: 'lesson' | 'checkpoint' | 'review' | 'pronunciation' | 'topic-vocabulary' = 'lesson',
    score?: number,
  ): void {
    this.repository.update((profile) => {
      const previous = profile.streak.lastActiveDate;
      const difference = previous
        ? this.calendarDayDifference(previous, activityDate)
        : null;
      const current = previous === activityDate
        ? profile.streak.current
        : difference === 1 ? profile.streak.current + 1 : 1;
      return {
        ...profile,
        activityEvents: [
          ...profile.activityEvents,
          {
            kind,
            occurredAt: activityDate.includes('T')
              ? activityDate
              : `${activityDate}T12:00:00Z`,
            ...(score === undefined ? {} : { score }),
          },
        ],
        streak: {
          current,
          longest: Math.max(profile.streak.longest, current),
          lastActiveDate: activityDate,
        },
      };
    });
  }

  nextAction(
    path: LearningPath,
    today = this.today(),
  ): NextLearningAction {
    const checkpoint = this.pendingCheckpointIdFor(path);
    if (checkpoint) {
      const start = path.checkpoint_start;
      return {
        kind: 'checkpoint',
        title: `Làm checkpoint Bài ${start}–${start + 4}`,
        route: '/learn/checkpoint',
        queryParams: { start },
      };
    }
    if (path.level_exam_required) {
      return {
        kind: 'level-exam',
        title: `Làm bài thi tổng kết HSK ${path.level_exam_level ?? path.current_level}`,
        route: '/learn/level-exam',
      };
    }
    const due = this.repository
      .profile()
      .reviewCards.filter((card) => card.dueDate <= today).length;
    if (due > 0) {
      return {
        kind: 'review',
        title: `Ôn ${due} mục đến hạn`,
        route: '/learn/review',
        count: due,
      };
    }
    const completed = new Set(this.repository.profile().completedLessonIds);
    const nextLesson = path.lessons.find((lesson) => !completed.has(lesson.id));
    if (nextLesson) {
      return {
        kind: 'lesson',
        title: `Tiếp tục Bài ${nextLesson.number}`,
        route: `/learn/lesson/${nextLesson.number}`,
      };
    }
    if (path.completed_all_levels) {
      return {
        kind: 'complete',
        title: 'Bạn đã hoàn thành lộ trình HSK 1–6',
        route: '/learn/notebook',
      };
    }
    return {
      kind: 'generate',
      title: `Đang chuẩn bị Ngày ${path.current_day_number + 1}`,
      route: '/learn',
    };
  }

  private today(): string {
    return new Date().toISOString().slice(0, 10);
  }

  private calendarDayDifference(from: string, to: string): number {
    const [fromYear, fromMonth, fromDay] = from.split('-').map(Number);
    const [toYear, toMonth, toDay] = to.split('-').map(Number);
    return Math.round(
      (Date.UTC(toYear, toMonth - 1, toDay) -
        Date.UTC(fromYear, fromMonth - 1, fromDay)) /
        86_400_000,
    );
  }
}
