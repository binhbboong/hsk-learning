import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { LessonApiService } from '../../core/services/lesson-api.service';
import { Dashboard } from './dashboard';

const lesson = {
  id: 'hsk1-chao-hoi',
  level: 1 as const,
  title: 'Chào hỏi đầu tiên',
  goal: 'Nhận biết 5 từ HSK 1.',
  estimated_minutes: 5,
  source: 'fallback' as const,
  cards: Array.from({ length: 5 }, (_, index) => ({
    id: `card-${index}`,
    hanzi: '你',
    pinyin: 'nǐ',
    sino_vietnamese: 'nhĩ',
    meaning_vi: 'bạn',
    example_zh: '你好！',
    example_vi: 'Xin chào!',
  })),
};

describe('Dashboard', () => {
  let fixture: ComponentFixture<Dashboard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Dashboard],
      providers: [
        provideRouter([]),
        {
          provide: LessonApiService,
          useValue: { getRecommendedLesson: () => of(lesson) },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(Dashboard);
  });

  it('shows the recommended HSK 1 lesson and start action', async () => {
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();

    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    const link = (fixture.nativeElement as HTMLElement).querySelector(
      'a[data-testid="start-lesson"]',
    );

    expect(text).toContain('Chào hỏi đầu tiên');
    expect(text).toContain('HSK 1');
    expect(text).toContain('5 từ');
    expect(link?.textContent).toContain('Bắt đầu học');
    expect(link?.getAttribute('href')).toBe('/lesson');
  });
});
