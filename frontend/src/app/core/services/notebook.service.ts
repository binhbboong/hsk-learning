import { computed, inject, Injectable } from '@angular/core';

import { NotebookWord } from '../models/learning-profile';
import { LearningProfileRepository } from './learning-profile.repository';


export type SaveableWord = Omit<NotebookWord, 'savedAt'>;

@Injectable({ providedIn: 'root' })
export class NotebookService {
  private readonly repository = inject(LearningProfileRepository);
  readonly words = computed(() => this.repository.profile().notebook);

  add(word: SaveableWord, savedAt = new Date().toISOString()): void {
    this.repository.update((profile) => ({
      ...profile,
      notebook: profile.notebook.some((item) => item.id === word.id)
        ? profile.notebook
        : [...profile.notebook, { ...word, savedAt }],
    }));
  }

  remove(wordId: string): void {
    this.repository.update((profile) => ({
      ...profile,
      notebook: profile.notebook.filter((item) => item.id !== wordId),
    }));
  }

  has(wordId: string): boolean {
    return this.words().some((word) => word.id === wordId);
  }
}
