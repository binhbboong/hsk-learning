import { TestBed } from '@angular/core/testing';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

import { LessonApiService } from './lesson-api.service';
import { environment } from '../../../environments/environment.generated';

describe('LessonApiService', () => {
  it('requests the fixed MVP lesson contract', () => {
    environment.apiBaseUrl = 'https://hsk-api.example';
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    const service = TestBed.inject(LessonApiService);
    const http = TestBed.inject(HttpTestingController);

    service.getRecommendedLesson().subscribe();

    const request = http.expectOne(
      (candidate) =>
        candidate.url === 'https://hsk-api.example/api/v1/lessons/recommended' &&
        candidate.params.get('level') === '1' &&
        candidate.params.get('size') === '5',
    );
    expect(request.request.method).toBe('GET');
    request.flush({
      id: 'lesson',
      level: 1,
      title: 'Bài học',
      goal: 'Mục tiêu',
      estimated_minutes: 5,
      source: 'fallback',
      cards: [],
    });
    http.verify();
    environment.apiBaseUrl = '';
  });
});
