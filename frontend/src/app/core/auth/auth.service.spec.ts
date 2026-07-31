import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { AuthService } from './auth.service';

describe('AuthService', () => {
  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
  });

  it('registers and persists the active user session', () => {
    const service = TestBed.inject(AuthService);
    const http = TestBed.inject(HttpTestingController);
    let completed = false;

    service.register('Mai Anh', 'mai@example.com', 'matkhau123').subscribe(() => completed = true);
    const request = http.expectOne('/api/v1/auth/register');
    expect(request.request.method).toBe('POST');
    request.flush({
      token: 'session-token',
      user: { id: 'user-1', display_name: 'Mai Anh', email: 'mai@example.com' },
    });

    expect(completed).toBe(true);
    expect(service.user()?.display_name).toBe('Mai Anh');
    expect(service.token()).toBe('session-token');
    expect(JSON.parse(localStorage.getItem('hsk-learning.session.v1')!)).toMatchObject({
      token: 'session-token',
    });
  });

  it('restores a saved session and clears it on logout', () => {
    localStorage.setItem('hsk-learning.session.v1', JSON.stringify({
      token: 'saved-token',
      user: { id: 'user-2', display_name: 'Bình', email: 'binh@example.com' },
    }));
    const service = TestBed.inject(AuthService);
    const http = TestBed.inject(HttpTestingController);

    expect(service.isAuthenticated()).toBe(true);
    service.logout().subscribe();
    const request = http.expectOne('/api/v1/auth/logout');
    expect(request.request.headers.get('Authorization')).toBe('Bearer saved-token');
    request.flush(null, { status: 204, statusText: 'No Content' });

    expect(service.isAuthenticated()).toBe(false);
    expect(localStorage.getItem('hsk-learning.session.v1')).toBeNull();
  });
});
