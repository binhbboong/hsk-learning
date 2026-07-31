import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { Lesson } from '../../core/models/lesson';
import { LessonApiService } from '../../core/services/lesson-api.service';

@Component({
  selector: 'app-lesson-overview',
  imports: [RouterLink],
  templateUrl: './lesson-overview.html',
  styleUrl: './lesson-overview.scss',
})
export class LessonOverview implements OnInit {
  private readonly lessonApi = inject(LessonApiService);

  readonly lesson = signal<Lesson | null>(null);
  readonly loading = signal(true);
  readonly error = signal(false);

  ngOnInit(): void {
    this.lessonApi.getRecommendedLesson().subscribe({
      next: (lesson) => {
        this.lesson.set(lesson);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      },
    });
  }

  retry(): void {
    this.loading.set(true);
    this.error.set(false);
    this.ngOnInit();
  }
}
