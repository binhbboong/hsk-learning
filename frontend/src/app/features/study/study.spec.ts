import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { Lesson } from '../../core/models/lesson';
import { LessonApiService } from '../../core/services/lesson-api.service';
import { StudySessionService } from '../../core/services/study-session.service';
import { Study } from './study';

const lesson: Lesson = {
  id: 'lesson',
  level: 1,
  title: 'Chào hỏi đầu tiên',
  goal: 'Mục tiêu',
  estimated_minutes: 5,
  source: 'fallback',
  cards: Array.from({ length: 5 }, (_, index) => ({
    id: `card-${index + 1}`,
    hanzi: index === 0 ? '你' : `字${index + 1}`,
    pinyin: index === 0 ? 'nǐ' : 'zì',
    sino_vietnamese: index === 0 ? 'nhĩ' : 'tự',
    meaning_vi: index === 0 ? 'bạn' : `từ ${index + 1}`,
    example_zh: '你好！',
    example_vi: 'Xin chào!',
  })),
};

describe('Study', () => {
  let fixture: ComponentFixture<Study>;
  let session: StudySessionService;

  beforeEach(async () => {
    sessionStorage.clear();
    await TestBed.configureTestingModule({
      imports: [Study],
      providers: [
        provideRouter([]),
        {
          provide: LessonApiService,
          useValue: { getRecommendedLesson: () => of(lesson) },
        },
      ],
    }).compileComponents();
    session = TestBed.inject(StudySessionService);
    session.start(lesson);
    fixture = TestBed.createComponent(Study);
    fixture.detectChanges();
  });

  it('hides the answer and rating controls before reveal', () => {
    const element = fixture.nativeElement as HTMLElement;

    expect(element.textContent).toContain('你');
    expect(element.textContent).toContain('1 / 5');
    expect(element.textContent).not.toContain('nhĩ');
    expect(element.querySelector('[data-testid="remembered"]')).toBeNull();
  });

  it('reveals Vietnamese learning details before accepting a rating', () => {
    const element = fixture.nativeElement as HTMLElement;

    (element.querySelector('[data-testid="reveal"]') as HTMLButtonElement).click();
    fixture.detectChanges();

    expect(element.textContent).toContain('nǐ');
    expect(element.textContent).toContain('nhĩ');
    expect(element.textContent).toContain('bạn');
    expect(element.textContent).toContain('Xin chào!');
    expect(element.querySelector('[data-testid="remembered"]')).not.toBeNull();
    expect(element.querySelector('[data-testid="review"]')).not.toBeNull();
  });

  it('advances to the next hidden card after rating', () => {
    const element = fixture.nativeElement as HTMLElement;
    (element.querySelector('[data-testid="reveal"]') as HTMLButtonElement).click();
    fixture.detectChanges();

    (element.querySelector('[data-testid="remembered"]') as HTMLButtonElement).click();
    fixture.detectChanges();

    expect(element.textContent).toContain('2 / 5');
    expect(element.textContent).toContain('字2');
    expect(session.revealed()).toBe(false);
  });
});
