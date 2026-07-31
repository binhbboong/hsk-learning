import { inject, Injectable } from '@angular/core';

import { ReviewCard } from '../models/learning-profile';
import { LearningProfileRepository } from './learning-profile.repository';


export type SrsRating = 'forgot' | 'hard' | 'remembered';
export type ReviewWord = Pick<
  ReviewCard,
  'id' | 'hanzi' | 'pinyin' | 'meaningVi' | 'sourceLessonId'
>;

@Injectable({ providedIn: 'root' })
export class SrsService {
  private readonly repository = inject(LearningProfileRepository);

  dueCards(today = this.today()): ReviewCard[] {
    return this.repository
      .profile()
      .reviewCards.filter((card) => card.dueDate <= today);
  }

  cardCount(): number {
    return this.repository.profile().reviewCards.length;
  }

  schedule(
    word: ReviewWord,
    rating: SrsRating,
    today = this.today(),
  ): ReviewCard {
    const current = this.repository
      .profile()
      .reviewCards.find((card) => card.id === word.id);
    const next = this.calculate(word, current, rating, today);
    this.save(next);
    return next;
  }

  rate(cardId: string, rating: SrsRating, today = this.today()): ReviewCard {
    const current = this.repository
      .profile()
      .reviewCards.find((card) => card.id === cardId);
    if (!current) throw new Error('Không tìm thấy thẻ ôn tập.');
    const next = this.calculate(current, current, rating, today);
    this.save(next);
    this.repository.update((profile) => ({
      ...profile,
      activityEvents: [
        ...profile.activityEvents,
        { kind: 'review', occurredAt: `${today}T12:00:00Z` },
      ],
    }));
    return next;
  }

  private calculate(
    word: ReviewWord,
    current: ReviewCard | undefined,
    rating: SrsRating,
    today: string,
  ): ReviewCard {
    const baseIntervals: Record<SrsRating, number> = {
      forgot: 1,
      hard: 3,
      remembered: 7,
    };
    const repetitions =
      rating === 'forgot' ? 0 : (current?.repetitions ?? 0) + 1;
    const intervalDays =
      rating === 'remembered' && current
        ? Math.max(7, current.intervalDays * 2)
        : baseIntervals[rating];
    return {
      ...word,
      repetitions,
      intervalDays,
      dueDate: this.addDays(today, intervalDays),
      lastReviewedAt: current ? `${today}T12:00:00Z` : undefined,
    };
  }

  private save(card: ReviewCard): void {
    this.repository.update((profile) => ({
      ...profile,
      reviewCards: [
        ...profile.reviewCards.filter((candidate) => candidate.id !== card.id),
        card,
      ],
    }));
  }

  private addDays(date: string, days: number): string {
    const [year, month, day] = date.split('-').map(Number);
    const next = new Date(Date.UTC(year, month - 1, day + days));
    return next.toISOString().slice(0, 10);
  }

  private today(): string {
    return new Date().toISOString().slice(0, 10);
  }
}
