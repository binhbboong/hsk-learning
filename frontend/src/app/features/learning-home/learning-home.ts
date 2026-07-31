import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import {
  LearningDaySummary,
  LearningPath,
  PathLessonSummary,
} from '../../core/models/learning-content';
import { LearningPathApiService } from '../../core/services/learning-path-api.service';
import { LearningProfileRepository } from '../../core/services/learning-profile.repository';
import { ProgressService } from '../../core/services/progress.service';
import { MistakeService } from '../../core/services/mistake.service';
import { NotebookService } from '../../core/services/notebook.service';
import { SrsService } from '../../core/services/srs.service';
import {
  LearningAnalyticsService,
  LearningInsights,
} from '../../core/services/learning-analytics.service';


@Component({
  selector: 'app-learning-home',
  imports: [RouterLink],
  templateUrl: './learning-home.html',
  styleUrl: './learning-home.scss',
})
export class LearningHome implements OnInit {
  private readonly api = inject(LearningPathApiService);
  readonly repository = inject(LearningProfileRepository);
  readonly progress = inject(ProgressService);
  readonly mistakes = inject(MistakeService);
  readonly notebook = inject(NotebookService);
  readonly srs = inject(SrsService);
  private readonly analytics = inject(LearningAnalyticsService);

  readonly path = signal<LearningPath | null>(null);
  readonly loading = signal(true);
  readonly error = signal(false);
  readonly generatingPath = signal(false);
  readonly generationError = signal<string | null>(null);
  readonly insights = signal<LearningInsights | null>(null);
  readonly insightsLoading = signal(true);
  readonly insightsError = signal(false);
  readonly nextAction = computed(() => {
    const path = this.path();
    return path
      ? this.progress.nextAction(path)
      : { kind: 'complete' as const, title: '', route: '/learn' };
  });
  readonly dueCount = computed(() => this.srs.dueCards().length);
  readonly displayedDays = computed(() =>
    [...(this.path()?.days ?? [])].reverse(),
  );

  ngOnInit(): void {
    this.loadPath();
    this.loadInsights();
  }

  private loadInsights(): void {
    this.analytics.getInsights().subscribe({
      next: (insights) => {
        this.insights.set(insights);
        this.insightsLoading.set(false);
      },
      error: () => {
        this.insightsError.set(true);
        this.insightsLoading.set(false);
      },
    });
  }

  generateNextPath(): void {
    if (this.generatingPath()) return;
    this.generatingPath.set(true);
    this.generationError.set(null);
    this.api.createNextPath().subscribe({
      next: () => {
        this.generatingPath.set(false);
        this.loadPath(false);
      },
      error: (error) => {
        this.generatingPath.set(false);
        this.generationError.set(
          error?.error?.detail ??
            `AI chưa thể tạo Ngày ${(this.path()?.current_day_number ?? 1) + 1}. Vui lòng thử lại.`,
        );
      },
    });
  }

  lessonsForDay(
    day: LearningDaySummary,
    path: LearningPath,
  ): PathLessonSummary[] {
    const lessonIds = new Set(day.lesson_ids);
    return path.lessons.filter((lesson) => lessonIds.has(lesson.id));
  }

  dayStatus(day: LearningDaySummary): string {
    return this.progress.isDayCompleted(day) ? 'Hoàn thành' : 'Đang học';
  }

  private loadPath(showLoading = true): void {
    if (showLoading) this.loading.set(true);
    this.api.getPath().subscribe({
      next: (path) => {
        this.path.set(path);
        this.loading.set(false);
        if (this.progress.nextAction(path).kind === 'generate') {
          this.generateNextPath();
        }
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      },
    });
  }
}
