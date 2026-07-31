import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment.generated';


export interface ActivityDay {
  date: string;
  active: boolean;
  count: number;
}

export interface RetentionWindow {
  rate: number | null;
  sample_size: number;
  remembered: number;
  label_vi: string;
}

export interface SkillWeakness {
  skill: 'listening' | 'sentence-order' | 'vocabulary' | 'pronunciation';
  label_vi: string;
  evidence_count: number;
  severity: number;
  reason_vi: string;
}

export interface LearningInsights {
  activity_days: ActivityDay[];
  retention_30d: RetentionWindow;
  weaknesses: SkillWeakness[];
  recommendation: {
    title: string;
    reason_vi: string;
    route: string;
    query_params: Record<string, string>;
  };
}

@Injectable({ providedIn: 'root' })
export class LearningAnalyticsService {
  private readonly http = inject(HttpClient);

  getInsights(): Observable<LearningInsights> {
    return this.http.get<LearningInsights>(
      `${environment.apiBaseUrl}/api/v1/analytics/learning`,
    );
  }
}

