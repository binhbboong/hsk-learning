import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { Lesson } from '../models/lesson';
import { environment } from '../../../environments/environment.generated';

@Injectable({ providedIn: 'root' })
export class LessonApiService {
  private readonly http = inject(HttpClient);

  getRecommendedLesson(): Observable<Lesson> {
    const baseUrl = environment.apiBaseUrl.replace(/\/$/, '');
    return this.http.get<Lesson>(`${baseUrl}/api/v1/lessons/recommended`, {
      params: { level: 1, size: 5 },
    });
  }
}
