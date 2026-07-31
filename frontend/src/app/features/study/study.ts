import { Component, inject, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { LessonApiService } from '../../core/services/lesson-api.service';
import {
  CardRating,
  StudySessionService,
} from '../../core/services/study-session.service';

@Component({
  selector: 'app-study',
  imports: [RouterLink],
  templateUrl: './study.html',
  styleUrl: './study.scss',
})
export class Study implements OnInit {
  readonly session = inject(StudySessionService);
  private readonly lessonApi = inject(LessonApiService);
  private readonly router = inject(Router);

  readonly loading = signal(false);
  readonly error = signal(false);

  ngOnInit(): void {
    if (this.session.active()) {
      return;
    }

    this.loading.set(true);
    this.lessonApi.getRecommendedLesson().subscribe({
      next: (lesson) => {
        this.session.start(lesson);
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.error.set(true);
      },
    });
  }

  reveal(): void {
    this.session.reveal();
  }

  rate(rating: CardRating): void {
    if (this.session.rate(rating)) {
      void this.router.navigate(['/results']);
    }
  }
}
