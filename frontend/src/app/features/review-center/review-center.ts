import { Component, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { NotebookService } from '../../core/services/notebook.service';
import { MistakeService } from '../../core/services/mistake.service';
import { SrsRating, SrsService } from '../../core/services/srs.service';
import { ReviewQuizService } from '../../core/services/review-quiz.service';


type ReviewMode = 'srs' | 'mistakes' | 'notebook';

@Component({
  selector: 'app-review-center',
  imports: [RouterLink],
  templateUrl: './review-center.html',
  styleUrl: './review-center.scss',
})
export class ReviewCenter {
  private readonly route = inject(ActivatedRoute);
  readonly srs = inject(SrsService);
  readonly mistakes = inject(MistakeService);
  readonly notebook = inject(NotebookService);
  private readonly quiz = inject(ReviewQuizService);

  readonly mode = signal<ReviewMode>(this.initialMode());
  readonly revealed = signal(false);
  readonly selectedAnswer = signal<string | null>(null);
  readonly mistakeAnswer = signal('');
  readonly arrangedMistakeTokens = signal<string[]>([]);
  readonly mistakeFeedback = signal<string | null>(null);
  readonly reviewedCount = signal(0);
  readonly hasScheduledCards = computed(() => this.srs.cardCount() > 0);

  readonly reviewCards = computed(() => {
    if (this.mode() === 'notebook') {
      return this.notebook.words().map((word) => ({
        ...word,
        repetitions: 0,
        intervalDays: 0,
        dueDate: new Date().toISOString().slice(0, 10),
      }));
    }
    return this.srs.dueCards();
  });
  readonly currentCard = computed(() => this.reviewCards()[0] ?? null);
  readonly answerOptions = computed(() => {
    const card = this.currentCard();
    return card ? this.quiz.optionsFor(card, this.reviewCards().map((item) => item.meaningVi)) : [];
  });
  readonly answerCorrect = computed(() => this.selectedAnswer() === this.currentCard()?.meaningVi);
  readonly currentMistake = computed(() => this.mistakes.items()[0] ?? null);
  readonly isSentenceOrderMistake = computed(() => {
    const mistake = this.currentMistake();
    return (
      mistake?.kind === 'sentence-order' ||
      mistake?.prompt.toLocaleLowerCase().includes('sắp xếp') === true
    );
  });
  readonly mistakeTokens = computed(() => {
    const mistake = this.currentMistake();
    if (!mistake || !this.isSentenceOrderMistake()) return [];
    return this.tokenize(mistake.correctAnswer).reverse();
  });
  readonly availableMistakeTokens = computed(() => {
    const selected = [...this.arrangedMistakeTokens()];
    return this.mistakeTokens().filter((token) => {
      const selectedIndex = selected.indexOf(token);
      if (selectedIndex === -1) return true;
      selected.splice(selectedIndex, 1);
      return false;
    });
  });

  setMode(mode: ReviewMode): void {
    this.mode.set(mode);
    this.revealed.set(false);
    this.selectedAnswer.set(null);
    this.mistakeFeedback.set(null);
    this.mistakeAnswer.set('');
    this.arrangedMistakeTokens.set([]);
  }

  reveal(): void {
    this.revealed.set(true);
  }

  chooseAnswer(answer: string): void {
    if (this.revealed()) return;
    this.selectedAnswer.set(answer);
    this.revealed.set(true);
  }

  continueReview(): void {
    this.rate(this.answerCorrect() ? 'remembered' : 'forgot');
    this.selectedAnswer.set(null);
  }

  rate(rating: SrsRating): void {
    const card = this.currentCard();
    if (!card || !this.revealed()) return;
    if (this.mode() === 'notebook') {
      this.srs.schedule(card, rating);
    } else {
      this.srs.rate(card.id, rating);
      this.reviewedCount.update((count) => count + 1);
    }
    this.revealed.set(false);
  }

  updateMistakeAnswer(value: string): void {
    this.mistakeAnswer.set(value);
  }

  chooseMistakeToken(token: string): void {
    if (!this.availableMistakeTokens().includes(token)) return;
    this.arrangedMistakeTokens.update((tokens) => [...tokens, token]);
    this.mistakeFeedback.set(null);
  }

  undoMistakeToken(): void {
    this.arrangedMistakeTokens.update((tokens) => tokens.slice(0, -1));
    this.mistakeFeedback.set(null);
  }

  answerArrangedMistake(): void {
    this.answerMistake(this.arrangedMistakeTokens().join(' '));
  }

  answerMistake(answer = this.mistakeAnswer()): void {
    const mistake = this.currentMistake();
    if (!mistake) return;
    if (
      this.normalizeAnswer(answer) ===
      this.normalizeAnswer(mistake.correctAnswer)
    ) {
      this.mistakes.resolve(mistake.id);
      this.mistakeFeedback.set('Chính xác. Câu này đã được xóa khỏi danh sách sai.');
      this.mistakeAnswer.set('');
      this.arrangedMistakeTokens.set([]);
    } else {
      this.mistakeFeedback.set(
        `Chưa đúng. Đáp án: ${mistake.correctAnswer}. ${mistake.explanationVi}`,
      );
    }
  }

  private tokenize(answer: string): string[] {
    return answer.split(/[|\s]+/u).filter(Boolean);
  }

  private normalizeAnswer(answer: string): string {
    return this.tokenize(answer).join('|').toLocaleLowerCase();
  }

  private initialMode(): ReviewMode {
    const source = this.route.snapshot.queryParamMap.get('source');
    return source === 'notebook' || source === 'mistakes' ? source : 'srs';
  }
}
