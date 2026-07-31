import { HttpClient, HttpHeaders } from '@angular/common/http';
import { computed, inject, Injectable, signal } from '@angular/core';
import { catchError, finalize, Observable, tap, throwError } from 'rxjs';

import { environment } from '../../../environments/environment.generated';
import { AuthSession, AuthUser } from './auth.models';

const SESSION_KEY = 'hsk-learning.session.v1';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiBaseUrl}/api/v1/auth`;
  private readonly session = signal<AuthSession | null>(this.restore());

  readonly user = computed(() => this.session()?.user ?? null);
  readonly token = computed(() => this.session()?.token ?? null);
  readonly isAuthenticated = computed(() => Boolean(this.session()));

  register(displayName: string, email: string, password: string): Observable<AuthSession> {
    return this.http.post<AuthSession>(`${this.baseUrl}/register`, {
      display_name: displayName,
      email,
      password,
    }).pipe(tap((session) => this.save(session)));
  }

  login(email: string, password: string): Observable<AuthSession> {
    return this.http.post<AuthSession>(`${this.baseUrl}/login`, { email, password })
      .pipe(tap((session) => this.save(session)));
  }

  validateSession(): Observable<AuthUser> {
    return this.http.get<AuthUser>(`${this.baseUrl}/me`, {
      headers: this.authHeaders(),
    }).pipe(
      tap((user) => {
        const current = this.session();
        if (current) this.save({ ...current, user });
      }),
      catchError((error) => {
        this.clear();
        return throwError(() => error);
      }),
    );
  }

  logout(): Observable<void> {
    const request = this.http.post<void>(`${this.baseUrl}/logout`, null, {
      headers: this.authHeaders(),
    });
    return request.pipe(finalize(() => this.clear()));
  }

  clear(): void {
    this.session.set(null);
    localStorage.removeItem(SESSION_KEY);
  }

  private authHeaders(): HttpHeaders {
    const token = this.token();
    return token
      ? new HttpHeaders({ Authorization: `Bearer ${token}` })
      : new HttpHeaders();
  }

  private save(session: AuthSession): void {
    this.session.set(session);
    localStorage.setItem(SESSION_KEY, JSON.stringify(session));
  }

  private restore(): AuthSession | null {
    try {
      const stored = localStorage.getItem(SESSION_KEY);
      if (!stored) return null;
      const parsed = JSON.parse(stored) as AuthSession;
      return parsed.token && parsed.user?.id ? parsed : null;
    } catch {
      localStorage.removeItem(SESSION_KEY);
      return null;
    }
  }
}
