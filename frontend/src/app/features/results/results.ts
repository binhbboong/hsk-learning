import { Component, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { StudySessionService } from '../../core/services/study-session.service';

@Component({
  selector: 'app-results',
  imports: [RouterLink],
  templateUrl: './results.html',
  styleUrl: './results.scss',
})
export class Results {
  readonly session = inject(StudySessionService);
  private readonly router = inject(Router);

  startReview(): void {
    this.session.startReview();
    void this.router.navigate(['/study']);
  }
}
