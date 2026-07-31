import { Injectable, signal } from '@angular/core';

import { SkillKind } from '../models/skill-lesson';


export interface SkillResult {
  kind: Exclude<SkillKind, 'vocabulary'>;
  title: string;
  score: number;
  total: number;
  summary: string;
  nextTip: string;
  retryRoute: string;
}

@Injectable({ providedIn: 'root' })
export class SkillResultService {
  readonly result = signal<SkillResult | null>(null);

  set(result: SkillResult): void {
    this.result.set(result);
    sessionStorage.setItem('hsk-learning.skill-result.v1', JSON.stringify(result));
  }

  constructor() {
    const stored = sessionStorage.getItem('hsk-learning.skill-result.v1');
    if (stored) {
      try {
        this.result.set(JSON.parse(stored) as SkillResult);
      } catch {
        sessionStorage.removeItem('hsk-learning.skill-result.v1');
      }
    }
  }
}
