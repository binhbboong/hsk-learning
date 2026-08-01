import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment.generated';
import { PlacementAttempt, PlacementStatus } from '../models/placement';


@Injectable({ providedIn: 'root' })
export class PlacementApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiBaseUrl}/api/v1/placement`;

  status(): Observable<PlacementStatus> {
    return this.http.get<PlacementStatus>(`${this.baseUrl}/status`);
  }

  start(): Observable<PlacementAttempt> {
    return this.http.post<PlacementAttempt>(`${this.baseUrl}/attempts`, null);
  }

  answer(attemptId: string, optionId: string | null, skip = false): Observable<PlacementAttempt> {
    return this.http.post<PlacementAttempt>(`${this.baseUrl}/attempts/${attemptId}/answers`, {
      option_id: optionId,
      skip,
    });
  }

  submitPronunciation(attemptId: string, recording: Blob): Observable<PlacementAttempt> {
    const form = new FormData();
    form.append('audio', recording, `placement.${recording.type.includes('wav') ? 'wav' : 'webm'}`);
    return this.http.post<PlacementAttempt>(
      `${this.baseUrl}/attempts/${attemptId}/pronunciation`, form,
    );
  }

  listeningAudio(attemptId: string): Observable<Blob> {
    return this.http.post(`${this.baseUrl}/attempts/${attemptId}/audio`, null, {
      responseType: 'blob',
    });
  }

  skip(): Observable<{ selected_level: number; applied: boolean }> {
    return this.http.post<{ selected_level: number; applied: boolean }>(`${this.baseUrl}/skip`, null);
  }

  selectLevel(level: number): Observable<{ selected_level: number; applied: boolean }> {
    return this.http.post<{ selected_level: number; applied: boolean }>(`${this.baseUrl}/selection`, {
      selected_level: level,
    });
  }
}
