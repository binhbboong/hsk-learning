import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../../../environments/environment.generated';
import { LearningPathApiService } from './learning-path-api.service';


describe('LearningPathApiService', () => {
  it('loads path, lesson and checkpoint contracts', () => {
    environment.apiBaseUrl = 'https://api.example';
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    const service = TestBed.inject(LearningPathApiService);
    const http = TestBed.inject(HttpTestingController);

    service.getPath().subscribe();
    http.expectOne('https://api.example/api/v1/path?level=1').flush({ level: 1, lessons: [] });

    service.getLesson(3).subscribe();
    http.expectOne('https://api.example/api/v1/path/lessons/3').flush({ id: 'lesson-3' });

    service.getCheckpoint(6).subscribe();
    http.expectOne('https://api.example/api/v1/path/checkpoint?start=6').flush({ id: 'checkpoint' });

    service.createNextPath().subscribe();
    const createRequest = http.expectOne('https://api.example/api/v1/path/next');
    expect(createRequest.request.method).toBe('POST');
    createRequest.flush({});

    http.verify();
    environment.apiBaseUrl = '';
  });
});
