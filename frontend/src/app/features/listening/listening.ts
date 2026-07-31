import { Component, inject, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { ListeningLesson } from '../../core/models/skill-lesson';
import { AudioService } from '../../core/services/audio.service';
import { SkillApiService } from '../../core/services/skill-api.service';
import { SkillResultService } from '../../core/services/skill-result.service';


@Component({
  selector: 'app-listening',
  imports: [RouterLink],
  templateUrl: './listening.html',
  styleUrl: './listening.scss',
})
export class Listening implements OnInit {
  private readonly api = inject(SkillApiService);
  private readonly audio = inject(AudioService);
  private readonly results = inject(SkillResultService);
  private readonly router = inject(Router);

  readonly lesson = signal<ListeningLesson | null>(null);
  readonly loading = signal(true);
  readonly error = signal(false);
  readonly transcriptVisible = signal(false);
  readonly audioUnavailable = signal(false);
  readonly selected = signal<string | null>(null);

  ngOnInit(): void {
    this.api.getLesson('listening').subscribe({
      next: (lesson) => {
        this.lesson.set(lesson as ListeningLesson);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      },
    });
  }

  play(rate: number): void {
    const lesson = this.lesson();
    if (!lesson) return;
    if (!this.audio.speak(lesson.utterance_zh, rate)) {
      this.audioUnavailable.set(true);
      this.transcriptVisible.set(true);
    }
  }

  showTranscript(): void {
    this.transcriptVisible.set(true);
  }

  select(optionId: string): void {
    this.selected.set(optionId);
  }

  submit(): void {
    const lesson = this.lesson();
    const selected = this.selected();
    if (!lesson || !selected) return;
    const correct = selected === lesson.correct_option_id;
    this.transcriptVisible.set(true);
    this.results.set({
      kind: 'listening',
      title: lesson.title,
      score: correct ? 1 : 0,
      total: 1,
      summary: correct
        ? 'Bạn đã nhận ra đúng tên người nói trong câu giới thiệu.'
        : `Đáp án đúng là ${lesson.options.find((option) => option.id === lesson.correct_option_id)?.text}.`,
      nextTip: lesson.explanation_vi,
      retryRoute: '/skills/listening',
    });
    void this.router.navigate(['/skills/result']);
  }
}
