import { Component, inject, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { GrammarLesson } from '../../core/models/skill-lesson';
import { SkillApiService } from '../../core/services/skill-api.service';
import { SkillResultService } from '../../core/services/skill-result.service';


@Component({
  selector: 'app-grammar',
  imports: [RouterLink],
  templateUrl: './grammar.html',
  styleUrl: './grammar.scss',
})
export class Grammar implements OnInit {
  private readonly api = inject(SkillApiService);
  private readonly results = inject(SkillResultService);
  private readonly router = inject(Router);

  readonly lesson = signal<GrammarLesson | null>(null);
  readonly index = signal(0);
  readonly selected = signal<string | null>(null);
  readonly checked = signal(false);
  readonly score = signal(0);
  readonly loading = signal(true);
  readonly error = signal(false);

  ngOnInit(): void {
    this.api.getLesson('grammar').subscribe({
      next: (lesson) => {
        this.lesson.set(lesson as GrammarLesson);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      },
    });
  }

  select(optionId: string): void {
    if (!this.checked()) this.selected.set(optionId);
  }

  check(): void {
    const question = this.lesson()?.questions[this.index()];
    if (!question || !this.selected() || this.checked()) return;
    if (this.selected() === question.correct_option_id) {
      this.score.update((score) => score + 1);
    }
    this.checked.set(true);
  }

  next(): void {
    const lesson = this.lesson();
    if (!lesson || !this.checked()) return;
    if (this.index() < lesson.questions.length - 1) {
      this.index.update((index) => index + 1);
      this.selected.set(null);
      this.checked.set(false);
      return;
    }
    this.results.set({
      kind: 'grammar',
      title: lesson.title,
      score: this.score(),
      total: lesson.questions.length,
      summary: 'Bạn đã luyện cách dùng 是 để giới thiệu người và vai trò.',
      nextTip: 'Hãy đọc lại hai câu ví dụ thành tiếng để kết nối ngữ pháp với phát âm.',
      retryRoute: '/skills/grammar',
    });
    void this.router.navigate(['/skills/result']);
  }
}
