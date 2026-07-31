import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';

import { SkillApiService } from '../../core/services/skill-api.service';
import { SkillsCatalog } from './skills-catalog';


const catalog = {
  level: 1 as const,
  items: [
    { kind: 'vocabulary' as const, title: 'Từ vựng', goal: 'Nhớ từ', estimated_minutes: 5, route: '/lesson' },
    { kind: 'grammar' as const, title: 'Ngữ pháp', goal: 'Dùng câu', estimated_minutes: 7, route: '/skills/grammar' },
    { kind: 'listening' as const, title: 'Nghe hiểu', goal: 'Nghe câu', estimated_minutes: 5, route: '/skills/listening' },
    { kind: 'pronunciation' as const, title: 'Phát âm', goal: 'Sửa thanh điệu', estimated_minutes: 6, route: '/skills/pronunciation' },
  ],
};

describe('SkillsCatalog', () => {
  async function create(api: object): Promise<ComponentFixture<SkillsCatalog>> {
    await TestBed.configureTestingModule({
      imports: [SkillsCatalog],
      providers: [
        provideRouter([]),
        { provide: SkillApiService, useValue: api },
      ],
    }).compileComponents();
    const fixture = TestBed.createComponent(SkillsCatalog);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
    return fixture;
  }

  it('shows four skill choices with goals, durations and routes', async () => {
    const fixture = await create({ getCatalog: () => of(catalog) });
    const element = fixture.nativeElement as HTMLElement;
    const links = [...element.querySelectorAll<HTMLAnchorElement>('[data-testid^="skill-"]')];

    expect(links).toHaveLength(4);
    expect(element.textContent).toContain('Hôm nay bạn muốn luyện gì?');
    expect(element.textContent).toContain('Ngữ pháp');
    expect(element.textContent).toContain('Nghe hiểu');
    expect(element.textContent).toContain('Phát âm');
    expect(links.map((link) => link.getAttribute('href'))).toContain('/skills/grammar');
  });

  it('shows a retry action when the catalog fails', async () => {
    const fixture = await create({
      getCatalog: () => throwError(() => new Error('offline')),
    });

    expect(fixture.nativeElement.textContent).toContain('Không thể tải danh mục');
    expect(fixture.nativeElement.querySelector('[data-testid="retry-catalog"]')).not.toBeNull();
  });
});
