import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { SkillResultService } from '../../core/services/skill-result.service';
import { SkillResults } from './skill-results';


describe('SkillResults', () => {
  it('summarizes the skill and offers retry and catalog routes', async () => {
    await TestBed.configureTestingModule({
      imports: [SkillResults],
      providers: [provideRouter([])],
    }).compileComponents();
    const results = TestBed.inject(SkillResultService);
    results.set({
      kind: 'grammar',
      title: 'Giới thiệu với 是',
      score: 2,
      total: 2,
      summary: 'Bạn đã dùng đúng mẫu câu.',
      nextTip: 'Đọc lại hai ví dụ.',
      retryRoute: '/skills/grammar',
    });
    const fixture = TestBed.createComponent(SkillResults);
    fixture.detectChanges();

    const element = fixture.nativeElement as HTMLElement;
    expect(element.textContent).toContain('Hoàn thành bài ngữ pháp');
    expect(element.textContent).toContain('2 / 2');
    expect(element.textContent).toContain('Bạn đã dùng đúng mẫu câu.');
    expect(element.querySelector('[data-testid="retry-skill"]')?.getAttribute('href')).toBe('/skills/grammar');
    expect(element.querySelector('[data-testid="back-skills"]')?.getAttribute('href')).toBe('/skills');
  });
});
