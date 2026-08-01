import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { environment } from '../../../environments/environment.generated';
import { LevelExamApiService } from './level-exam-api.service';

describe('LevelExamApiService', () => {
  it('starts, saves and submits an exam through authenticated routes', () => {
    environment.apiBaseUrl = 'https://hsk-api.example';
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    const service = TestBed.inject(LevelExamApiService), http = TestBed.inject(HttpTestingController);
    service.start().subscribe();
    expect(http.expectOne('https://hsk-api.example/api/v1/level-exams/attempts').request.method).toBe('POST');
    service.save('a1', 'q1', 'o1', true, 2).subscribe();
    const save = http.expectOne('https://hsk-api.example/api/v1/level-exams/attempts/a1');
    expect(save.request.body).toEqual({ question_id: 'q1', option_id: 'o1', flagged: true, current_index: 2 });
    service.submit('a1').subscribe();
    expect(http.expectOne('https://hsk-api.example/api/v1/level-exams/attempts/a1/submit').request.method).toBe('POST');
    http.verify(); environment.apiBaseUrl = '';
  });
});
