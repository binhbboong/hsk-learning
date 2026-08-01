import { TestBed } from '@angular/core/testing';

import { ThemeService } from './theme.service';

describe('ThemeService', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.removeAttribute('data-theme');
    TestBed.configureTestingModule({});
  });

  afterEach(() => {
    document.documentElement.removeAttribute('data-theme');
  });

  it('follows the device theme by default', () => {
    const service = TestBed.inject(ThemeService);

    expect(service.preference()).toBe('system');
    expect(document.documentElement.getAttribute('data-theme')).toBeNull();
  });

  it('applies and persists an explicit dark theme', () => {
    const service = TestBed.inject(ThemeService);

    service.setPreference('dark');

    expect(service.preference()).toBe('dark');
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    expect(localStorage.getItem('hsk-learning.theme.v1')).toBe('dark');
  });

  it('returns to the device theme when system is selected', () => {
    const service = TestBed.inject(ThemeService);
    service.setPreference('light');

    service.setPreference('system');

    expect(document.documentElement.getAttribute('data-theme')).toBeNull();
    expect(localStorage.getItem('hsk-learning.theme.v1')).toBe('system');
  });
});
