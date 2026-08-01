import { computed, Injectable, signal } from '@angular/core';

import { TopicVocabularyProgress } from '../models/learning-profile';
import {
  TopicVocabularySession,
  TopicVocabularyWord,
} from '../models/topic-vocabulary';
import { LearningProfileRepository } from './learning-profile.repository';
import { ProgressService } from './progress.service';
import { ReviewQuizService } from './review-quiz.service';
import { SrsService } from './srs.service';


export interface TopicAnswerResult {
  correct: boolean;
  selected: string;
  correctMeaning: string;
}

@Injectable({ providedIn: 'root' })
export class TopicVocabularySessionService {
  readonly session = signal<TopicVocabularySession | null>(null);
  readonly answerResult = signal<TopicAnswerResult | null>(null);
  readonly progress = computed(() => {
    const current = this.session();
    if (!current) return null;
    return this.repository.profile().topicVocabularyProgress.find(
      (item) => item.sessionId === current.id,
    ) ?? null;
  });
  readonly currentWord = computed<TopicVocabularyWord | null>(() => {
    const current = this.session();
    const progress = this.progress();
    if (!current || !progress || progress.phase === 'completed') return null;
    const index = progress.phase === 'cards' ? progress.cardIndex : progress.quizIndex;
    return current.words[index] ?? null;
  });
  readonly options = computed(() => {
    const current = this.session();
    const word = this.currentWord();
    if (!current || !word || this.progress()?.phase !== 'quiz') return [];
    return this.quiz.optionsFor(
      { id: word.id, meaningVi: word.meaning_vi },
      current.words.map((item) => item.meaning_vi),
    );
  });

  constructor(
    private readonly repository: LearningProfileRepository,
    private readonly quiz: ReviewQuizService,
    private readonly srs: SrsService,
    private readonly learningProgress: ProgressService,
  ) {}

  open(session: TopicVocabularySession): void {
    if (session.words.length !== 10) {
      throw new Error('Phiên từ vựng phải có đúng 10 từ.');
    }
    this.session.set(session);
    this.answerResult.set(null);
    if (!this.progress()) {
      this.saveProgress({
        topicId: session.topic_id,
        sessionId: session.id,
        phase: 'cards',
        cardIndex: 0,
        quizIndex: 0,
        learnedWordIds: [],
        correctWordIds: [],
        updatedAt: new Date().toISOString(),
      });
    }
  }

  completeCurrentCard(): void {
    const progress = this.progress();
    const word = this.currentWord();
    if (!progress || !word || progress.phase !== 'cards') return;
    const nextIndex = Math.min(10, progress.cardIndex + 1);
    this.saveProgress({
      ...progress,
      phase: nextIndex === 10 ? 'quiz' : 'cards',
      cardIndex: nextIndex,
      learnedWordIds: this.unique([...progress.learnedWordIds, word.id]),
      updatedAt: new Date().toISOString(),
    });
  }

  answer(selected: string): TopicAnswerResult {
    const existing = this.answerResult();
    if (existing) return existing;
    const progress = this.progress();
    const session = this.session();
    const word = this.currentWord();
    if (!progress || !session || !word || progress.phase !== 'quiz') {
      throw new Error('Chưa có câu hỏi từ vựng để trả lời.');
    }
    const correct = selected === word.meaning_vi;
    const result = { correct, selected, correctMeaning: word.meaning_vi };
    const profile = this.repository.profile();
    const existingIdentity = profile.reviewCards.find(
      (card) => card.hanzi === word.hanzi,
    )?.id ?? profile.notebook.find(
      (item) => item.hanzi === word.hanzi,
    )?.id ?? word.id;
    this.srs.schedule(
      {
        id: existingIdentity,
        hanzi: word.hanzi,
        pinyin: word.pinyin,
        meaningVi: word.meaning_vi,
        sourceLessonId: `topic:${session.topic_id}`,
      },
      correct ? 'remembered' : 'forgot',
    );
    this.saveProgress({
      ...progress,
      correctWordIds: correct
        ? this.unique([...progress.correctWordIds, word.id])
        : progress.correctWordIds,
      updatedAt: new Date().toISOString(),
    });
    this.answerResult.set(result);
    return result;
  }

  continueQuiz(activityDate?: string): void {
    const result = this.answerResult();
    const progress = this.progress();
    if (!result || !progress || progress.phase !== 'quiz') return;
    const nextIndex = progress.quizIndex + 1;
    const completed = nextIndex >= 10;
    this.saveProgress({
      ...progress,
      phase: completed ? 'completed' : 'quiz',
      quizIndex: Math.min(10, nextIndex),
      updatedAt: new Date().toISOString(),
    });
    this.answerResult.set(null);
    if (completed) {
      this.learningProgress.recordActivity(
        activityDate,
        'topic-vocabulary',
        this.progress()?.correctWordIds.length,
      );
    }
  }

  private saveProgress(next: TopicVocabularyProgress): void {
    this.repository.update((profile) => ({
      ...profile,
      topicVocabularyProgress: [
        ...profile.topicVocabularyProgress.filter(
          (item) => item.sessionId !== next.sessionId,
        ),
        next,
      ],
    }));
  }

  private unique(values: string[]): string[] {
    return [...new Set(values)];
  }
}
