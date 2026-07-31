import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';

import { Auth } from './auth';

describe('Auth', () => {
  beforeEach(async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [Auth],
      providers: [
        provideRouter([]),
        provideHttpClient(),
        provideHttpClientTesting(),
      ],
    }).compileComponents();
  });

  it('switches between login and registration with friendly validation', () => {
    const fixture = TestBed.createComponent(Auth);
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    expect(element.textContent).toContain('Chào mừng bạn quay lại');
    fixture.componentInstance.setMode('register');
    fixture.detectChanges();
    expect(element.textContent).toContain('Tạo không gian học của bạn');
    fixture.componentInstance.submit();
    fixture.detectChanges();
    expect(element.textContent).toContain('Vui lòng nhập tên');
    expect(element.textContent).toContain('Email chưa đúng định dạng');
    expect(element.textContent).toContain('Mật khẩu cần ít nhất 8 ký tự');
  });

  it('registers and navigates to the requested learning page', () => {
    const router = TestBed.inject(Router);
    vi.spyOn(router, 'navigateByUrl').mockResolvedValue(true);
    const fixture = TestBed.createComponent(Auth);
    fixture.componentInstance.setMode('register');
    fixture.componentInstance.displayName.set('Mai Anh');
    fixture.componentInstance.email.set('mai@example.com');
    fixture.componentInstance.password.set('matkhau123');
    fixture.componentInstance.submit();

    const http = TestBed.inject(HttpTestingController);
    http.expectOne('/api/v1/auth/register').flush({
      token: 'token',
      user: { id: 'u1', display_name: 'Mai Anh', email: 'mai@example.com' },
    });
    http.expectOne('/api/v1/profile').flush({
      version: 1,
      completedLessonIds: [],
      streak: { current: 0, longest: 0, lastActiveDate: null },
      reviewCards: [],
      mistakes: [],
      notebook: [],
      checkpointResults: [],
    });

    expect(router.navigateByUrl).toHaveBeenCalledWith('/learn');
  });
});
