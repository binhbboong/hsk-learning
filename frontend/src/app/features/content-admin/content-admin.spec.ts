import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';
import { vi } from 'vitest';

import { ContentAdminService } from '../../core/services/content-admin.service';
import { ContentAdmin } from './content-admin';


describe('ContentAdmin', () => {
  it('shows usage and lets an administrator edit and approve a pending draft', async () => {
    const draft = {
      id: 'draft-1',
      account_id: 'account-1',
      path_index: 2,
      status: 'pending' as const,
      payload: { path_index: 2, level: 1, difficulty: 2, lessons: [], checkpoint: {} },
      quality: { passed: false, codes: ['duplicate'], issues: ['Trùng từ vựng'] },
      created_at: '2026-07-31T08:00:00Z',
      updated_at: '2026-07-31T08:00:00Z',
      reviewed_by: null,
    };
    const approve = vi.fn().mockReturnValue(of({ ...draft, status: 'approved' }));
    const update = vi.fn().mockReturnValue(of({
      ...draft,
      quality: { passed: true, codes: [], issues: [] },
    }));
    await TestBed.configureTestingModule({
      imports: [ContentAdmin],
      providers: [provideRouter([]), {
        provide: ContentAdminService,
        useValue: {
          list: () => of([draft]),
          usage: () => of({
            date: '2026-07-31', today_requests: 2, successful_requests: 1,
            failed_requests: 1, input_tokens: 1200, output_tokens: 800,
            account_daily_limit: 10, system_daily_limit: 50,
          }),
          update,
          approve,
          reject: vi.fn(),
        },
      }],
    }).compileComponents();

    const fixture = TestBed.createComponent(ContentAdmin);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    expect(element.textContent).toContain('2 / 50 lượt hôm nay');
    expect(element.textContent).toContain('Trùng từ vựng');
    fixture.componentInstance.editorValue.set(JSON.stringify(draft.payload));
    fixture.componentInstance.save();
    expect(update).toHaveBeenCalled();
    fixture.componentInstance.approve();
    expect(approve).toHaveBeenCalledWith('draft-1');
  });
});
