import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { of } from 'rxjs';

import { GrammarLesson } from '../../core/models/skill-lesson';
import { SkillApiService } from '../../core/services/skill-api.service';
import { SkillResultService } from '../../core/services/skill-result.service';
import { Grammar } from './grammar';


const lesson: GrammarLesson = {
  id: 'grammar',
  level: 1,
  kind: 'grammar',
  title: 'Giới thiệu với 是',
  goal: 'Dùng câu đúng',
  estimated_minutes: 7,
  pattern: 'A + 是 + B',
  explanation_vi: '是 gần nghĩa “là”.',
  examples: [
    { hanzi: '我是学生。', pinyin: 'Wǒ shì xuésheng.', meaning_vi: 'Tôi là học sinh.' },
    { hanzi: '她是老师。', pinyin: 'Tā shì lǎoshī.', meaning_vi: 'Cô ấy là giáo viên.' },
  ],
  questions: [
    {
      id: 'q1',
      prompt_vi: 'Chọn câu đúng',
      options: [{ id: 'a', text: '我是越南人。' }, { id: 'b', text: '我越南人是。' }],
      correct_option_id: 'a',
      explanation_vi: 'A đứng trước 是.',
    },
    {
      id: 'q2',
      prompt_vi: 'Chọn từ còn thiếu',
      options: [{ id: 'a', text: '你' }, { id: 'b', text: '是' }],
      correct_option_id: 'b',
      explanation_vi: 'Cần dùng 是.',
    },
  ],
};

describe('Grammar', () => {
  let fixture: ComponentFixture<Grammar>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Grammar],
      providers: [
        provideRouter([]),
        { provide: SkillApiService, useValue: { getLesson: () => of(lesson) } },
      ],
    }).compileComponents();
    fixture = TestBed.createComponent(Grammar);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
  });

  it('teaches the pattern and gates progress until an answer is checked', () => {
    const element = fixture.nativeElement as HTMLElement;
    expect(element.textContent).toContain('A + 是 + B');
    expect(element.textContent).toContain('Wǒ shì xuésheng.');
    expect(element.textContent).toContain('1 / 2');
    expect(element.querySelector('[data-testid="next-question"]')).toBeNull();

    (element.querySelector('[data-testid="option-a"]') as HTMLButtonElement).click();
    fixture.detectChanges();
    (element.querySelector('[data-testid="check-answer"]') as HTMLButtonElement).click();
    fixture.detectChanges();

    expect(element.textContent).toContain('Chính xác');
    expect(element.textContent).toContain('A đứng trước 是.');
    expect(element.querySelector('[data-testid="next-question"]')).not.toBeNull();
  });

  it('finishes after two checked answers and stores a result', () => {
    const router = TestBed.inject(Router);
    const navigate = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    const results = TestBed.inject(SkillResultService);

    fixture.componentInstance.select('a');
    fixture.componentInstance.check();
    fixture.componentInstance.next();
    fixture.componentInstance.select('b');
    fixture.componentInstance.check();
    fixture.componentInstance.next();

    expect(results.result()?.kind).toBe('grammar');
    expect(results.result()?.score).toBe(2);
    expect(navigate).toHaveBeenCalledWith(['/skills/result']);
  });
});
