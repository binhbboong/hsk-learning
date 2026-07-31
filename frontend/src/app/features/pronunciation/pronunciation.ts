import { Component, inject, OnDestroy, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { PronunciationLesson } from '../../core/models/skill-lesson';
import { AudioService } from '../../core/services/audio.service';
import { SkillApiService } from '../../core/services/skill-api.service';
import { SkillResultService } from '../../core/services/skill-result.service';


type SelfRating = 'retry' | 'close' | 'matched';

@Component({
  selector: 'app-pronunciation',
  imports: [RouterLink],
  templateUrl: './pronunciation.html',
  styleUrl: './pronunciation.scss',
})
export class Pronunciation implements OnInit, OnDestroy {
  private readonly api = inject(SkillApiService);
  private readonly audio = inject(AudioService);
  private readonly results = inject(SkillResultService);
  private readonly router = inject(Router);

  readonly lesson = signal<PronunciationLesson | null>(null);
  readonly loading = signal(true);
  readonly error = signal(false);
  readonly recording = signal(false);
  readonly microphoneUnavailable = signal(false);
  readonly recordingUrl = signal<string | null>(null);
  readonly rating = signal<SelfRating | null>(null);

  ngOnInit(): void {
    this.api.getLesson('pronunciation').subscribe({
      next: (lesson) => {
        this.lesson.set(lesson as PronunciationLesson);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      },
    });
  }

  ngOnDestroy(): void {
    const url = this.recordingUrl();
    if (url) this.audio.revokeRecording(url);
  }

  playSample(): void {
    const lesson = this.lesson();
    if (lesson) this.audio.speak(lesson.hanzi, 0.72);
  }

  async startRecording(): Promise<void> {
    const started = await this.audio.startRecording();
    this.recording.set(started);
    this.microphoneUnavailable.set(!started);
  }

  async stopRecording(): Promise<void> {
    const url = await this.audio.stopRecording();
    this.recording.set(false);
    if (url) {
      const previous = this.recordingUrl();
      if (previous) this.audio.revokeRecording(previous);
      this.recordingUrl.set(url);
    }
  }

  rate(rating: SelfRating): void {
    this.rating.set(rating);
  }

  complete(): void {
    const lesson = this.lesson();
    const rating = this.rating();
    if (!lesson || !rating) return;
    const scores: Record<SelfRating, number> = { retry: 1, close: 2, matched: 3 };
    this.results.set({
      kind: 'pronunciation',
      title: lesson.title,
      score: scores[rating],
      total: 3,
      summary:
        rating === 'matched'
          ? 'Bạn cảm nhận âm của mình đã gần với mẫu.'
          : 'Bạn đã nghe lại và xác định được mức độ cần luyện thêm.',
      nextTip: lesson.correction_tip_vi,
      retryRoute: '/skills/pronunciation',
    });
    void this.router.navigate(['/skills/result']);
  }
}
