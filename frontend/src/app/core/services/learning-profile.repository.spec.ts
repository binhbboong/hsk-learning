import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';

import { LearningProfileRepository } from './learning-profile.repository';


describe('LearningProfileRepository', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
  });

  it('creates and persists a versioned anonymous profile', () => {
    const repository = TestBed.inject(LearningProfileRepository);
    repository.update((profile) => ({
      ...profile,
      completedLessonIds: ['hsk1-lesson-1'],
    }));

    const restored = new LearningProfileRepository();

    expect(restored.profile().version).toBe(1);
    expect(restored.profile().completedLessonIds).toEqual(['hsk1-lesson-1']);
  });

  it('recovers safely from corrupted browser data', () => {
    localStorage.setItem('hsk-learning.profile.v1', '{broken');

    const repository = new LearningProfileRepository();

    expect(repository.profile().completedLessonIds).toEqual([]);
    expect(repository.profile().streak.current).toBe(0);
    expect(localStorage.getItem('hsk-learning.profile.v1')).not.toBe('{broken');
  });

  it('imports anonymous progress into an empty account then syncs updates', () => {
    localStorage.setItem('hsk-learning.session.v1', JSON.stringify({
      token: 'profile-token',
      user: { id: 'u1', display_name: 'Mai', email: 'mai@example.com' },
    }));
    const repository = TestBed.inject(LearningProfileRepository);
    repository.update((profile) => ({
      ...profile,
      completedLessonIds: ['hsk1-lesson-1'],
    }));
    const http = TestBed.inject(HttpTestingController);
    let connected = false;

    repository.connectAccount().subscribe(() => connected = true);
    http.expectOne('/api/v1/profile').flush({
      version: 1,
      completedLessonIds: [],
      streak: { current: 0, longest: 0, lastActiveDate: null },
      reviewCards: [],
      mistakes: [],
      notebook: [],
      checkpointResults: [],
    });
    const importRequest = http.expectOne('/api/v1/profile');
    expect(importRequest.request.method).toBe('PUT');
    expect(importRequest.request.body.completedLessonIds).toEqual(['hsk1-lesson-1']);
    importRequest.flush(importRequest.request.body);

    expect(connected).toBe(true);
  });
});
