import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment.generated';


export interface ContentDraft {
  id: string;
  account_id: string;
  path_index: number;
  status: 'pending' | 'approved' | 'rejected';
  payload: Record<string, unknown>;
  quality: { passed: boolean; codes: string[]; issues: string[] };
  created_at: string;
  updated_at: string;
  reviewed_by: string | null;
}

export interface UsageSummary {
  date: string;
  today_requests: number;
  successful_requests: number;
  failed_requests: number;
  input_tokens: number;
  output_tokens: number;
  account_daily_limit: number;
  system_daily_limit: number;
}

@Injectable({ providedIn: 'root' })
export class ContentAdminService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${environment.apiBaseUrl}/api/v1/admin`;

  list(status = 'pending'): Observable<ContentDraft[]> {
    return this.http.get<ContentDraft[]>(
      `${this.baseUrl}/content`,
      { params: { status } },
    );
  }

  usage(): Observable<UsageSummary> {
    return this.http.get<UsageSummary>(`${this.baseUrl}/usage`);
  }

  update(id: string, payload: Record<string, unknown>): Observable<ContentDraft> {
    return this.http.put<ContentDraft>(
      `${this.baseUrl}/content/${id}`,
      { payload },
    );
  }

  approve(id: string): Observable<ContentDraft> {
    return this.http.post<ContentDraft>(
      `${this.baseUrl}/content/${id}/approve`,
      null,
    );
  }

  reject(id: string): Observable<ContentDraft> {
    return this.http.post<ContentDraft>(
      `${this.baseUrl}/content/${id}/reject`,
      null,
    );
  }
}

