import { provideHttpClient } from '@angular/common/http';
import {
  HttpTestingController,
  provideHttpClientTesting,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../../../environments/environment.generated';
import { SkillApiService } from './skill-api.service';


describe('SkillApiService', () => {
  it('loads the HSK 1 catalog and a selected skill lesson', () => {
    environment.apiBaseUrl = 'https://hsk-api.example';
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    const service = TestBed.inject(SkillApiService);
    const http = TestBed.inject(HttpTestingController);

    service.getCatalog().subscribe();
    const catalog = http.expectOne('https://hsk-api.example/api/v1/skills?level=1');
    expect(catalog.request.method).toBe('GET');
    catalog.flush({ level: 1, items: [] });

    service.getLesson('grammar').subscribe();
    const lesson = http.expectOne(
      'https://hsk-api.example/api/v1/skills/grammar?level=1',
    );
    expect(lesson.request.method).toBe('GET');
    lesson.flush({ kind: 'grammar' });

    http.verify();
    environment.apiBaseUrl = '';
  });
});
