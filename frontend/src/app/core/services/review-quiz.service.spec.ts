import { TestBed } from '@angular/core/testing';
import { ReviewQuizService } from './review-quiz.service';

describe('ReviewQuizService', () => {
  it('creates four unique choices with exactly one correct answer', () => {
    const service = TestBed.inject(ReviewQuizService);
    const options = service.optionsFor(
      { id: 'hello', meaningVi: 'xin chào' },
      ['cảm ơn', 'tạm biệt', 'học sinh', 'giáo viên'],
    );

    expect(options).toHaveLength(4);
    expect(new Set(options).size).toBe(4);
    expect(options.filter((value) => value === 'xin chào')).toHaveLength(1);
  });
});

