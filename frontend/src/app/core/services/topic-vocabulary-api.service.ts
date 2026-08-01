import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import {
  TopicRecommendationsResponse,
  TopicVocabularySession,
} from '../models/topic-vocabulary';
import { environment } from '../../../environments/environment.generated';


@Injectable({ providedIn: 'root' })
export class TopicVocabularyApiService {
  private readonly http = inject(HttpClient);

  recommendations(refresh = false): Observable<TopicRecommendationsResponse> {
    return this.http.get<TopicRecommendationsResponse>(
      `${environment.apiBaseUrl}/api/v1/topic-vocabulary/recommendations`,
      { params: refresh ? { refresh: true } : {} },
    );
  }

  startSession(topicId: string): Observable<TopicVocabularySession> {
    return this.http.post<TopicVocabularySession>(
      `${environment.apiBaseUrl}/api/v1/topic-vocabulary/sessions`,
      { topic_id: topicId },
    );
  }
}
