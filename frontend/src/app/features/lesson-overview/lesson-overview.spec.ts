import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { LessonApiService } from '../../core/services/lesson-api.service';
import { LessonOverview } from './lesson-overview';

const lesson = {
  id: 'hsk1-chao-hoi',
  level: 1 as const,
  title: 'Chào hỏi đầu tiên',
  goal: 'Nhận biết và sử dụng 5 từ HSK 1.',
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

describe('LessonOverview', () => {
  let fixture: ComponentFixture<LessonOverview>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LessonOverview],
      providers: [
        provideRouter([]),
        {
          provide: LessonApiService,
          useValue: { getRecommendedLesson: () => of(lesson) },
        },
      ],
    }).compileComponents();
    fixture = TestBed.createComponent(LessonOverview);
  });

  it('explains the session before the learner starts', async () => {
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();

    const element = fixture.nativeElement as HTMLElement;
    const text = element.textContent ?? '';
    const start = element.querySelector('a[data-testid="start-study"]');

    expect(text).toContain('Chào hỏi đầu tiên');
    expect(text).toContain('5 thẻ');
    expect(text).toContain('5 phút');
    expect(text).toContain('Pinyin');
    expect(text).toContain('Hán-Việt');
    expect(text).toContain('Nghĩa tiếng Việt');
    expect(text).toContain('Ví dụ');
    expect(start?.textContent).toContain('Bắt đầu flip-card');
    expect(start?.getAttribute('href')).toBe('/study');
  });
});
