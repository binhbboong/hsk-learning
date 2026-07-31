import { computed, Injectable, signal } from '@angular/core';

import { Lesson, VocabularyCard } from '../models/lesson';

export type CardRating = 'remembered' | 'review';

interface StoredSession {
  lesson: Lesson;
  cards: VocabularyCard[];
  currentIndex: number;
  revealed: boolean;
  ratings: Record<string, CardRating>;
}

const STORAGE_KEY = 'hsk-learning.study-session.v1';

@Injectable({ providedIn: 'root' })
export class StudySessionService {
  private readonly lessonState = signal<Lesson | null>(null);
  private readonly cardsState = signal<VocabularyCard[]>([]);
  private readonly currentIndexState = signal(0);
  private readonly revealedState = signal(false);
  private readonly ratingsState = signal<Record<string, CardRating>>({});

  readonly currentCard = computed(
    () => this.cardsState()[this.currentIndexState()] ?? null,
  );
  readonly currentPosition = computed(() =>
    this.cardsState().length === 0
      ? 0
      : Math.min(this.currentIndexState() + 1, this.cardsState().length),
  );
  readonly totalCards = computed(() => this.cardsState().length);
  readonly revealed = this.revealedState.asReadonly();
  readonly active = computed(() => this.lessonState() !== null);
  readonly complete = computed(
    () =>
      this.cardsState().length > 0 &&
      this.currentIndexState() >= this.cardsState().length,
  );
  readonly results = computed(() => {
    const cards = this.cardsState();
    const ratings = this.ratingsState();
    const reviewCards = cards.filter((card) => ratings[card.id] === 'review');
    const remembered = cards.filter(
      (card) => ratings[card.id] === 'remembered',
    ).length;

    return {
      total: cards.length,
      remembered,
      review: reviewCards.length,
      reviewCards,
    };
  });

  constructor() {
    this.restore();
  }

  start(lesson: Lesson, cards: VocabularyCard[] = lesson.cards): void {
    this.lessonState.set(lesson);
    this.cardsState.set(cards);
    this.currentIndexState.set(0);
    this.revealedState.set(false);
    this.ratingsState.set({});
    this.persist();
  }

  reveal(): void {
    if (this.currentCard() === null) {
      throw new Error('Không có thẻ đang học.');
    }
    this.revealedState.set(true);
    this.persist();
  }

  rate(rating: CardRating): boolean {
    const card = this.currentCard();
    if (card === null) {
      throw new Error('Không có thẻ đang học.');
    }
    if (!this.revealedState()) {
      throw new Error('Hãy lật thẻ trước khi đánh giá.');
    }

    this.ratingsState.update((ratings) => ({ ...ratings, [card.id]: rating }));
    this.currentIndexState.update((index) => index + 1);
    this.revealedState.set(false);
    this.persist();
    return this.complete();
  }

  startReview(): void {
    const lesson = this.lessonState();
    const reviewCards = this.results().reviewCards;
    if (lesson === null || reviewCards.length === 0) {
      throw new Error('Không có từ nào cần ôn lại.');
    }
    this.start(lesson, reviewCards);
  }

  clear(): void {
    this.lessonState.set(null);
    this.cardsState.set([]);
    this.currentIndexState.set(0);
    this.revealedState.set(false);
    this.ratingsState.set({});
    sessionStorage.removeItem(STORAGE_KEY);
  }

  private persist(): void {
    const lesson = this.lessonState();
    if (lesson === null) {
      return;
    }
    const payload: StoredSession = {
      lesson,
      cards: this.cardsState(),
      currentIndex: this.currentIndexState(),
      revealed: this.revealedState(),
      ratings: this.ratingsState(),
    };
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  }

  private restore(): void {
    const value = sessionStorage.getItem(STORAGE_KEY);
    if (value === null) {
      return;
    }
    try {
      const stored = JSON.parse(value) as StoredSession;
      this.lessonState.set(stored.lesson);
      this.cardsState.set(stored.cards);
      this.currentIndexState.set(stored.currentIndex);
      this.revealedState.set(stored.revealed);
      this.ratingsState.set(stored.ratings);
    } catch {
      sessionStorage.removeItem(STORAGE_KEY);
    }
  }
}
