import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { NEVER, of } from 'rxjs';
import { vi } from 'vitest';

import { AudioService } from '../../core/services/audio.service';
import { PlacementApiService } from '../../core/services/placement-api.service';
import { PlacementTest } from './placement-test';


const attempt = {
  attempt_id: 'attempt-1',
  status: 'in_progress' as const,
  question: {
    id: 'vocabulary-hsk3', skill: 'vocabulary' as const, level: 3,
    prompt_vi: 'Chọn nghĩa đúng của “已经”.',
    options: ['đã', 'đang', 'sẽ', 'thường'].map((text, index) => ({ id: `o${index}`, text })),
    target_text: null, target_pinyin: null, number: 1, total: 20 as const,
  },
  result: null,
};

describe('PlacementTest', () => {
  const api = {
    status: vi.fn(() => of({ can_take: true, in_progress: null, latest_result: null,
      retake_available_at: null, selected_level: null, can_apply_level: true })),
    start: vi.fn(() => of(attempt)),
    answer: vi.fn(() => of({ ...attempt, question: { ...attempt.question, number: 2 } })),
    skip: vi.fn(() => of({ selected_level: 1, applied: true })),
    selectLevel: vi.fn(() => of({ selected_level: 3, applied: true })),
  };

  beforeEach(async () => {
    Object.values(api).forEach((mock) => mock.mockClear());
    await TestBed.configureTestingModule({
      imports: [PlacementTest],
      providers: [
        provideRouter([]),
        { provide: PlacementApiService, useValue: api },
        { provide: AudioService, useValue: { speak: () => true } },
      ],
    }).compileComponents();
  });

  it('introduces all four skills and keeps HSK 1 as a one-click option', () => {
    const fixture = TestBed.createComponent(PlacementTest);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('20 câu');
    expect(fixture.nativeElement.textContent).toContain('Từ vựng');
    expect(fixture.nativeElement.textContent).toContain('Phát âm');
    expect(fixture.nativeElement.textContent).toContain('Bỏ qua, học HSK 1');
  });

  it('starts the adaptive attempt and renders four answer buttons', () => {
    const fixture = TestBed.createComponent(PlacementTest);
    fixture.detectChanges();
    fixture.componentInstance.start();
    fixture.detectChanges();

    expect(api.start).toHaveBeenCalledOnce();
    expect(fixture.nativeElement.textContent).toContain('Câu 1 / 20');
    expect(fixture.nativeElement.querySelectorAll('[data-testid="placement-option"]')).toHaveLength(4);
  });

  it('submits the selected option and advances to the server-owned next question', () => {
    const fixture = TestBed.createComponent(PlacementTest);
    fixture.detectChanges();
    fixture.componentInstance.start();
    fixture.componentInstance.selectOption('o0');
    fixture.componentInstance.submitAnswer();
    fixture.detectChanges();

    expect(api.answer).toHaveBeenCalledWith('attempt-1', 'o0');
    expect(fixture.nativeElement.textContent).toContain('Câu 2 / 20');
  });

  it('shows the four-skill result and lets an unstarted learner apply another HSK level', () => {
    const result = {
      recommended_level: 3, confidence: 'medium' as const, confidence_vi: 'Khá',
      summary_vi: 'Nên bắt đầu HSK 3.', completed_at: '2026-08-01T00:00:00Z',
      advisory_only: false,
      disclaimer_vi: 'Kết quả chỉ là gợi ý học tập, không phải điểm thi HSK chính thức.',
      skills: (['vocabulary', 'grammar', 'listening', 'pronunciation'] as const).map((skill) => ({
        skill, estimated_level: 3, correct: 3, assessed: 5,
      })),
    };
    api.status.mockReturnValueOnce(of({
      can_take: false, in_progress: null, latest_result: result,
      retake_available_at: '2026-08-31T00:00:00Z', selected_level: null,
      can_apply_level: true,
    }) as any);
    const fixture = TestBed.createComponent(PlacementTest);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Đề xuất');
    expect(fixture.nativeElement.textContent).toContain('HSK 3');
    expect(fixture.nativeElement.textContent).toContain('không phải điểm thi HSK chính thức');
    expect(fixture.nativeElement.querySelectorAll('.levels button')).toHaveLength(6);

    api.selectLevel.mockReturnValueOnce(NEVER);
    fixture.componentInstance.chooseLevel(2);
    fixture.componentInstance.applyLevel();
    expect(api.selectLevel).toHaveBeenCalledWith(2);
  });
});
