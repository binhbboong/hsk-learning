import { Component, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { CheckpointQuestion } from '../../core/models/learning-content';
import { AudioService } from '../../core/services/audio.service';
import { LearningPathApiService } from '../../core/services/learning-path-api.service';
import { LearningProfileRepository } from '../../core/services/learning-profile.repository';
import { MistakeService } from '../../core/services/mistake.service';
import { ProgressService } from '../../core/services/progress.service';

@Component({
  selector: 'app-checkpoint',
  imports: [RouterLink],
  templateUrl: './checkpoint.html',
  styleUrl: './checkpoint.scss',
})
export class Checkpoint {
  private readonly api = inject(LearningPathApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly audio = inject(AudioService);
  private readonly mistakes = inject(MistakeService);
  private readonly repository = inject(LearningProfileRepository);
  readonly progress = inject(ProgressService);

  readonly checkpoint = signal<import('../../core/models/learning-content').Checkpoint | null>(null);
  readonly index = signal(0);
  readonly selectedOption = signal<string | null>(null);
  readonly arrangedTokens = signal<string[]>([]);
  readonly score = signal(0);
  readonly finished = signal(false);
  readonly currentQuestion = computed(
    () => this.checkpoint()?.questions[this.index()] ?? null,
  );
  readonly unlocked = computed(() => {
    const checkpoint = this.checkpoint();
    if (!checkpoint) return false;
    const profile = this.repository.profile();
    return (
      checkpoint.lesson_ids.every((id) =>
        profile.completedLessonIds.includes(id),
      ) &&
      !profile.checkpointResults.some(
        (result) => result.checkpointId === checkpoint.id,
      )
    );
  });

  constructor() {
    const start = Number(this.route.snapshot.queryParamMap.get('start') ?? 1);
    this.api
      .getCheckpoint(start)
      .subscribe((checkpoint) => this.checkpoint.set(checkpoint));
  }

  play(): void {
    const text = this.currentQuestion()?.audio_text;
    if (text) this.audio.speak(text, 0.82);
  }

  selectOption(optionId: string): void {
    this.selectedOption.set(optionId);
  }

  chooseToken(token: string): void {
    const question = this.currentQuestion();
    if (!question) return;
    const used = this.arrangedTokens().filter((item) => item === token).length;
    const available = question.tokens.filter((item) => item === token).length;
    if (used < available) this.arrangedTokens.update((items) => [...items, token]);
  }

  undoToken(): void {
    this.arrangedTokens.update((items) => items.slice(0, -1));
  }

  submitAnswer(): void {
    const checkpoint = this.checkpoint();
    const question = this.currentQuestion();
    if (!checkpoint || !question || !this.unlocked()) return;
    const answer = question.kind === 'sentence-order'
      ? this.arrangedTokens().join(' ')
      : this.selectedOption();
    if (!answer) return;
    const correct = answer === question.correct_answer;
    if (correct) {
      this.score.update((value) => value + 1);
      this.mistakes.resolve(`checkpoint-${question.id}`);
    } else {
      this.mistakes.add(this.toMistake(question));
    }
    if (this.index() === checkpoint.questions.length - 1) {
      this.progress.completeCheckpoint(
        checkpoint.id,
        this.score(),
        checkpoint.questions.length,
      );
      this.finished.set(true);
      return;
    }
    this.index.update((value) => value + 1);
    this.selectedOption.set(null);
    this.arrangedTokens.set([]);
  }

  private toMistake(question: CheckpointQuestion) {
    const option = question.options.find(
      (item) => item.id === question.correct_answer,
    );
    return {
      id: `checkpoint-${question.id}`,
      sourceLessonId: 'hsk1-lessons-1-5',
      kind: 'checkpoint' as const,
      prompt: question.prompt_vi,
      correctAnswer: option?.text ?? question.correct_answer,
      explanationVi: question.explanation_vi,
    };
  }
}
