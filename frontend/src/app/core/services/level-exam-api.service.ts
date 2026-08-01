import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../environments/environment.generated';
import { LevelExamAttempt, LevelExamResult, LevelExamStatus } from '../models/level-exam';

@Injectable({ providedIn: 'root' })
export class LevelExamApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiBaseUrl}/api/v1/level-exams`;
  status() { return this.http.get<LevelExamStatus>(`${this.baseUrl}/status`); }
  start() { return this.http.post<LevelExamAttempt>(`${this.baseUrl}/attempts`, {}); }
  save(attemptId: string, questionId: string, optionId: string, flagged: boolean, currentIndex: number) {
    return this.http.put<LevelExamAttempt>(`${this.baseUrl}/attempts/${attemptId}`, {
      question_id: questionId, option_id: optionId, flagged, current_index: currentIndex,
    });
  }
  submit(attemptId: string) { return this.http.post<LevelExamResult>(`${this.baseUrl}/attempts/${attemptId}/submit`, {}); }
  audio(attemptId: string, questionId: string) {
    return this.http.post(`${this.baseUrl}/attempts/${attemptId}/questions/${questionId}/audio`, {}, { responseType: 'blob' });
  }
}
