import { computed, inject, Injectable } from '@angular/core';

import { MistakeRecord } from '../models/learning-profile';
import { LearningProfileRepository } from './learning-profile.repository';


@Injectable({ providedIn: 'root' })
export class MistakeService {
  private readonly repository = inject(LearningProfileRepository);
  readonly items = computed(() => this.repository.profile().mistakes);

  add(mistake: MistakeRecord): void {
    this.repository.update((profile) => ({
      ...profile,
      mistakes: profile.mistakes.some((item) => item.id === mistake.id)
        ? profile.mistakes
        : [...profile.mistakes, mistake],
    }));
  }

  resolve(mistakeId: string): void {
    this.repository.update((profile) => ({
      ...profile,
      mistakes: profile.mistakes.filter((item) => item.id !== mistakeId),
    }));
  }
}
