import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable, signal } from '@angular/core';
import { Observable, of, switchMap, tap } from 'rxjs';

import {
  createEmptyLearningProfile,
  LearningProfile,
} from '../models/learning-profile';
import { environment } from '../../../environments/environment.generated';


const STORAGE_KEY = 'hsk-learning.profile.v1';

@Injectable({ providedIn: 'root' })
export class LearningProfileRepository {
  readonly profile = signal<LearningProfile>(this.restore());
  private connected = false;

  constructor(private readonly http?: HttpClient) {}

  update(transform: (profile: LearningProfile) => LearningProfile): void {
    const next = transform(this.profile());
    this.profile.set(next);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    if (this.connected) this.saveRemote(next).subscribe();
  }

  reset(): void {
    const empty = createEmptyLearningProfile();
    this.profile.set(empty);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(empty));
  }

  connectAccount(): Observable<LearningProfile> {
    if (!this.http) return of(this.profile());
    const headers = this.authHeaders();
    return this.http.get<LearningProfile>(
      `${environment.apiBaseUrl}/api/v1/profile`,
      { headers },
    ).pipe(
      switchMap((remote) => {
        remote.activityEvents = Array.isArray(remote.activityEvents)
          ? remote.activityEvents
          : [];
        remote.topicVocabularyProgress = Array.isArray(remote.topicVocabularyProgress)
          ? remote.topicVocabularyProgress
          : [];
        remote.startingLevel = remote.startingLevel ?? null;
        remote.placementTest = remote.placementTest ?? null;
        remote.learningPreferences = remote.learningPreferences ?? null;
        const local = this.profile();
        if (this.isEmpty(remote) && !this.isEmpty(local)) {
          return this.saveRemote(local, headers);
        }
        this.profile.set(remote);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(remote));
        return of(remote);
      }),
      tap(() => this.connected = true),
    );
  }

  disconnectAccount(): void {
    this.connected = false;
    this.profile.set(createEmptyLearningProfile());
    localStorage.removeItem(STORAGE_KEY);
  }

  private saveRemote(
    profile: LearningProfile,
    headers = this.authHeaders(),
  ): Observable<LearningProfile> {
    if (!this.http) return of(profile);
    return this.http.put<LearningProfile>(
      `${environment.apiBaseUrl}/api/v1/profile`,
      profile,
      { headers },
    );
  }

  private authHeaders(): HttpHeaders {
    try {
      const session = JSON.parse(
        localStorage.getItem('hsk-learning.session.v1') || '{}',
      ) as { token?: string };
      return session.token
        ? new HttpHeaders({ Authorization: `Bearer ${session.token}` })
        : new HttpHeaders();
    } catch {
      return new HttpHeaders();
    }
  }

  private isEmpty(profile: LearningProfile): boolean {
    return profile.completedLessonIds.length === 0
      && profile.reviewCards.length === 0
      && profile.mistakes.length === 0
      && profile.notebook.length === 0
      && profile.checkpointResults.length === 0
      && (profile.activityEvents?.length ?? 0) === 0
      && (profile.topicVocabularyProgress?.length ?? 0) === 0
      && profile.streak.current === 0;
  }

  private restore(): LearningProfile {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) {
      const empty = createEmptyLearningProfile();
      localStorage.setItem(STORAGE_KEY, JSON.stringify(empty));
      return empty;
    }
    try {
      const parsed = JSON.parse(stored) as LearningProfile;
      if (
        parsed.version !== 1 ||
        !Array.isArray(parsed.completedLessonIds) ||
        !Array.isArray(parsed.reviewCards) ||
        !Array.isArray(parsed.mistakes) ||
        !Array.isArray(parsed.notebook) ||
        !Array.isArray(parsed.checkpointResults)
      ) {
        throw new Error('Unsupported learning profile');
      }
      parsed.activityEvents = Array.isArray(parsed.activityEvents)
        ? parsed.activityEvents
        : [];
      parsed.topicVocabularyProgress = Array.isArray(parsed.topicVocabularyProgress)
        ? parsed.topicVocabularyProgress
        : [];
      parsed.startingLevel = parsed.startingLevel ?? null;
      parsed.placementTest = parsed.placementTest ?? null;
      parsed.learningPreferences = parsed.learningPreferences ?? null;
      return parsed;
    } catch {
      const empty = createEmptyLearningProfile();
      localStorage.setItem(STORAGE_KEY, JSON.stringify(empty));
      return empty;
    }
  }
}
