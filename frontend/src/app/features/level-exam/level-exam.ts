import { Component, computed, inject, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { LevelExamAttempt, LevelExamResult } from '../../core/models/level-exam';
import { LevelExamApiService } from '../../core/services/level-exam-api.service';
import { LearningPathApiService } from '../../core/services/learning-path-api.service';

@Component({ selector: 'app-level-exam', imports: [RouterLink], templateUrl: './level-exam.html', styleUrl: './level-exam.scss' })
export class LevelExam {
  private readonly api = inject(LevelExamApiService);
  private readonly paths = inject(LearningPathApiService);
  private readonly router = inject(Router);
  readonly attempt = signal<LevelExamAttempt | null>(null);
  readonly result = signal<LevelExamResult | null>(null);
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly currentIndex = signal(0);
  readonly current = computed(() => this.attempt()?.questions[this.currentIndex()] ?? null);
  readonly answeredCount = computed(() => Object.keys(this.attempt()?.selections ?? {}).length);

  constructor() {
    this.api.status().subscribe({ next: status => {
      if (status.latest_result?.passed) this.result.set(status.latest_result);
      if (status.in_progress) { this.attempt.set(status.in_progress); this.currentIndex.set(status.in_progress.current_index); }
      this.loading.set(false);
    }, error: error => this.fail(error) });
  }
  start(): void { this.loading.set(true); this.api.start().subscribe({ next: attempt => {
    this.attempt.set(attempt); this.currentIndex.set(attempt.current_index); this.loading.set(false);
  }, error: error => this.fail(error) }); }
  choose(optionId: string): void {
    const attempt = this.attempt(), question = this.current(); if (!attempt || !question) return;
    this.api.save(attempt.attempt_id, question.id, optionId,
      attempt.flagged_question_ids.includes(question.id), this.currentIndex()).subscribe({
      next: saved => this.attempt.set(saved), error: error => this.fail(error),
    });
  }
  toggleFlag(): void {
    const attempt = this.attempt(), question = this.current();
    const selected = question ? attempt?.selections[question.id] : null;
    if (!attempt || !question || !selected) return;
    this.api.save(attempt.attempt_id, question.id, selected,
      !attempt.flagged_question_ids.includes(question.id), this.currentIndex()).subscribe({
      next: saved => this.attempt.set(saved), error: error => this.fail(error),
    });
  }
  go(index: number): void { this.currentIndex.set(Math.max(0, Math.min(19, index))); }
  playAudio(): void {
    const attempt = this.attempt(), question = this.current(); if (!attempt || !question) return;
    this.api.audio(attempt.attempt_id, question.id).subscribe({ next: blob => {
      const url = URL.createObjectURL(blob), audio = new Audio(url);
      audio.onended = () => URL.revokeObjectURL(url); void audio.play();
    }, error: error => this.fail(error) });
  }
  submit(): void {
    const attempt = this.attempt();
    if (!attempt || this.answeredCount() < 20) { this.error.set('Hãy trả lời đủ 20 câu trước khi nộp bài.'); return; }
    this.api.submit(attempt.attempt_id).subscribe({ next: result => {
      this.result.set(result); this.attempt.set(null); this.error.set(null);
    }, error: error => this.fail(error) });
  }
  continuePath(): void { this.paths.createNextPath().subscribe({
    next: () => void this.router.navigateByUrl('/learn'), error: error => this.fail(error),
  }); }
  private fail(error: any): void { this.error.set(error?.error?.detail ?? 'Đã có lỗi. Vui lòng thử lại.'); this.loading.set(false); }
}
