import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment.generated';
import {
  Checkpoint,
  DailyPathBundle,
  LearningPath,
  MultiActivityLesson,
} from '../models/learning-content';


@Injectable({ providedIn: 'root' })
export class LearningPathApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiBaseUrl}/api/v1/path`;

  getPath(): Observable<LearningPath> {
    return this.http.get<LearningPath>(this.baseUrl, {
      params: new HttpParams().set('level', 1),
    });
  }

  getLesson(number: number): Observable<MultiActivityLesson> {
    return this.http.get<MultiActivityLesson>(
      `${this.baseUrl}/lessons/${number}`,
    );
  }

  getCheckpoint(start = 1): Observable<Checkpoint> {
    return this.http.get<Checkpoint>(`${this.baseUrl}/checkpoint`, {
      params: new HttpParams().set('start', start),
    });
  }

  createNextPath(): Observable<DailyPathBundle> {
    return this.http.post<DailyPathBundle>(`${this.baseUrl}/next`, {});
  }
}
