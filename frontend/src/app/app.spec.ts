import { TestBed } from '@angular/core/testing';
import { App } from './app';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting } from '@angular/common/http/testing';
import { provideRouter } from '@angular/router';

describe('App', () => {
  beforeEach(async () => {
    localStorage.clear();
    document.documentElement.removeAttribute('data-theme');
    await TestBed.configureTestingModule({
      imports: [App],
      providers: [provideRouter([]), provideHttpClient(), provideHttpClientTesting()],
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(App);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it('should render the product brand', async () => {
    const fixture = TestBed.createComponent(App);
    await fixture.whenStable();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.textContent).toContain('HSK Learning');
  });

  it('lets the learner choose a persisted theme from the account menu', () => {
    localStorage.setItem(
      'hsk-learning.session.v1',
      JSON.stringify({
        token: 'token',
        user: {
          id: 'user-1',
          display_name: 'Bình',
          email: 'binh@example.com',
        },
      }),
    );
    const fixture = TestBed.createComponent(App);
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    (element.querySelector('[data-testid="account-menu"]') as HTMLButtonElement).click();
    fixture.detectChanges();
    const darkButton = element.querySelector('[data-testid="theme-dark"]') as HTMLButtonElement;

    expect(darkButton).not.toBeNull();
    darkButton.click();
    fixture.detectChanges();

    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    expect(darkButton.getAttribute('aria-pressed')).toBe('true');
  });
});
