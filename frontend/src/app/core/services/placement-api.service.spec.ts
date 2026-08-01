import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../../../environments/environment.generated';
import { PlacementApiService } from './placement-api.service';


describe('PlacementApiService', () => {
  it('starts, answers and applies a placement attempt through authenticated API routes', () => {
    environment.apiBaseUrl = 'https://hsk-api.example';
    TestBed.configureTestingModule({ providers: [provideHttpClient(), provideHttpClientTesting()] });
    const service = TestBed.inject(PlacementApiService);
    const http = TestBed.inject(HttpTestingController);

    service.start().subscribe();
    expect(http.expectOne('https://hsk-api.example/api/v1/placement/attempts').request.method).toBe('POST');

    service.answer('attempt-1', 'answer-a').subscribe();
    const answer = http.expectOne('https://hsk-api.example/api/v1/placement/attempts/attempt-1/answers');
    expect(answer.request.body).toEqual({ option_id: 'answer-a', skip: false });

    service.selectLevel(3).subscribe();
    expect(http.expectOne('https://hsk-api.example/api/v1/placement/selection').request.body)
      .toEqual({ selected_level: 3 });

    http.verify();
    environment.apiBaseUrl = '';
  });
});
