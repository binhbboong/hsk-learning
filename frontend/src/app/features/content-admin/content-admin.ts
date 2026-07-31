import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import {
  ContentAdminService,
  ContentDraft,
  UsageSummary,
} from '../../core/services/content-admin.service';


@Component({
  selector: 'app-content-admin',
  imports: [RouterLink],
  templateUrl: './content-admin.html',
  styleUrl: './content-admin.scss',
})
export class ContentAdmin implements OnInit {
  private readonly api = inject(ContentAdminService);

  readonly drafts = signal<ContentDraft[]>([]);
  readonly selected = signal<ContentDraft | null>(null);
  readonly usage = signal<UsageSummary | null>(null);
  readonly editorValue = signal('');
  readonly loading = signal(true);
  readonly saving = signal(false);
  readonly message = signal<string | null>(null);
  readonly error = signal<string | null>(null);

  ngOnInit(): void {
    this.reload();
  }

  choose(draft: ContentDraft): void {
    this.selected.set(draft);
    this.editorValue.set(JSON.stringify(draft.payload, null, 2));
    this.message.set(null);
    this.error.set(null);
  }

  updateEditor(value: string): void {
    this.editorValue.set(value);
  }

  save(): void {
    const draft = this.selected();
    if (!draft || this.saving()) return;
    let payload: Record<string, unknown>;
    try {
      payload = JSON.parse(this.editorValue()) as Record<string, unknown>;
    } catch {
      this.error.set('JSON chưa hợp lệ. Hãy kiểm tra dấu phẩy và dấu ngoặc.');
      return;
    }
    this.saving.set(true);
    this.api.update(draft.id, payload).subscribe({
      next: (updated) => {
        this.replace(updated);
        this.choose(updated);
        this.saving.set(false);
        this.message.set(
          updated.quality.passed
            ? 'Đã lưu. Nội dung đủ điều kiện để duyệt.'
            : 'Đã lưu. Nội dung vẫn còn lỗi chất lượng.',
        );
      },
      error: (error) => {
        this.saving.set(false);
        this.error.set(error?.error?.detail ?? 'Không thể lưu nội dung.');
      },
    });
  }

  approve(): void {
    this.decide('approve');
  }

  reject(): void {
    this.decide('reject');
  }

  private decide(action: 'approve' | 'reject'): void {
    const draft = this.selected();
    if (!draft || this.saving()) return;
    this.saving.set(true);
    this.api[action](draft.id).subscribe({
      next: () => {
        this.saving.set(false);
        this.message.set(
          action === 'approve' ? 'Đã duyệt và phát hành.' : 'Đã từ chối nội dung.',
        );
        this.reload();
      },
      error: (error) => {
        this.saving.set(false);
        this.error.set(error?.error?.detail ?? 'Không thể cập nhật trạng thái.');
      },
    });
  }

  private reload(): void {
    this.loading.set(true);
    this.api.list().subscribe({
      next: (drafts) => {
        this.drafts.set(drafts);
        this.loading.set(false);
        if (drafts.length) this.choose(drafts[0]);
        else this.selected.set(null);
      },
      error: (error) => {
        this.loading.set(false);
        this.error.set(error?.status === 403
          ? 'Tài khoản không có quyền quản trị.'
          : 'Không thể tải hàng đợi nội dung.');
      },
    });
    this.api.usage().subscribe({
      next: (usage) => this.usage.set(usage),
      error: () => this.error.set('Không thể tải usage AI.'),
    });
  }

  private replace(updated: ContentDraft): void {
    this.drafts.update((items) =>
      items.map((item) => item.id === updated.id ? updated : item),
    );
    this.selected.set(updated);
  }
}

