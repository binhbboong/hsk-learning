import { Component, computed, inject, OnDestroy, OnInit, signal } from '@angular/core';
import { Router, RouterLink } from '@angular/router';

import { PlacementAttempt, PlacementSkill } from '../../core/models/placement';
import { AudioService } from '../../core/services/audio.service';
import { PlacementApiService } from '../../core/services/placement-api.service';
import { LearningProfileRepository } from '../../core/services/learning-profile.repository';


@Component({
  selector: 'app-placement-test',
  imports: [RouterLink],
  templateUrl: './placement-test.html',
  styleUrl: './placement-test.scss',
})
export class PlacementTest implements OnInit, OnDestroy {
  private readonly api = inject(PlacementApiService);
  private readonly audio = inject(AudioService);
  private readonly router = inject(Router);
  private readonly profile = inject(LearningProfileRepository);

  readonly loading = signal(true);
  readonly phase = signal<'intro' | 'test' | 'result'>('intro');
  readonly attempt = signal<PlacementAttempt | null>(null);
  readonly selectedOption = signal<string | null>(null);
  readonly selectedLevel = signal(1);
  readonly busy = signal(false);
  readonly error = signal<string | null>(null);
  readonly recording = signal(false);
  readonly recordingUrl = signal<string | null>(null);
  readonly recordingReady = signal(false);
  readonly audioUrl = signal<string | null>(null);
  readonly canApplyLevel = signal(true);
  readonly retakeDate = signal<string | null>(null);

  readonly question = computed(() => this.attempt()?.question ?? null);
  readonly result = computed(() => this.attempt()?.result ?? null);
  readonly progress = computed(() => ((this.question()?.number ?? 0) / 20) * 100);
  readonly skillLabel = computed(() => this.labelFor(this.question()?.skill));

  ngOnInit(): void {
    this.api.status().subscribe({
      next: (status) => {
        this.canApplyLevel.set(status.can_apply_level);
        this.retakeDate.set(status.retake_available_at);
        if (status.in_progress) {
          this.setAttempt(status.in_progress);
        } else if (status.latest_result && !status.can_take) {
          this.attempt.set({ attempt_id: '', status: 'completed', question: null, result: status.latest_result });
          this.selectedLevel.set(status.latest_result.recommended_level);
          this.phase.set('result');
        }
        this.loading.set(false);
      },
      error: () => {
        this.loading.set(false);
        this.error.set('Chưa thể tải bài kiểm tra đầu vào. Vui lòng thử lại.');
      },
    });
  }

  ngOnDestroy(): void {
    this.releaseUrls();
  }

  start(): void {
    if (this.busy()) return;
    this.busy.set(true);
    this.error.set(null);
    this.api.start().subscribe({
      next: (attempt) => { this.busy.set(false); this.setAttempt(attempt); },
      error: (error) => { this.busy.set(false); this.error.set(this.errorText(error)); },
    });
  }

  selectOption(id: string): void {
    if (!this.busy()) this.selectedOption.set(id);
  }

  submitAnswer(): void {
    const attempt = this.attempt();
    const option = this.selectedOption();
    if (!attempt || !option || this.busy()) return;
    this.busy.set(true);
    this.api.answer(attempt.attempt_id, option).subscribe({
      next: (next) => { this.busy.set(false); this.setAttempt(next); },
      error: (error) => { this.busy.set(false); this.error.set(this.errorText(error)); },
    });
  }

  skipQuestion(): void {
    const attempt = this.attempt();
    if (!attempt || this.busy()) return;
    this.busy.set(true);
    this.api.answer(attempt.attempt_id, null, true).subscribe({
      next: (next) => { this.busy.set(false); this.setAttempt(next); },
      error: (error) => { this.busy.set(false); this.error.set(this.errorText(error)); },
    });
  }

  playListening(): void {
    const attempt = this.attempt();
    if (!attempt || this.busy()) return;
    this.busy.set(true);
    this.api.listeningAudio(attempt.attempt_id).subscribe({
      next: (blob) => {
        const previous = this.audioUrl();
        if (previous) URL.revokeObjectURL(previous);
        const url = URL.createObjectURL(blob);
        this.audioUrl.set(url);
        this.busy.set(false);
        void new Audio(url).play();
      },
      error: (error) => { this.busy.set(false); this.error.set(this.errorText(error)); },
    });
  }

  playPronunciationSample(): void {
    const text = this.question()?.target_text;
    if (text) this.audio.speak(text, 0.82);
  }

  async startRecording(): Promise<void> {
    this.error.set(null);
    this.recordingReady.set(false);
    this.recording.set(await this.audio.startRecording());
    if (!this.recording()) this.error.set('Không thể mở microphone. Bạn có thể bỏ qua câu này.');
  }

  async stopRecording(): Promise<void> {
    const url = await this.audio.stopRecording();
    this.recording.set(false);
    if (!url) return;
    const previous = this.recordingUrl();
    if (previous) this.audio.revokeRecording(previous);
    this.recordingUrl.set(url);
    const quality = this.audio.recordingQuality();
    this.recordingReady.set(quality.durationMs >= 800 && quality.size >= 512 && quality.hasSpeech !== false);
    if (!this.recordingReady()) this.error.set('Bản thu quá ngắn hoặc chưa có giọng nói. Hãy thu lại.');
  }

  submitPronunciation(): void {
    const attempt = this.attempt();
    const blob = this.audio.recordingBlob();
    if (!attempt || !blob || !this.recordingReady() || this.busy()) return;
    this.busy.set(true);
    this.api.submitPronunciation(attempt.attempt_id, blob).subscribe({
      next: (next) => { this.busy.set(false); this.setAttempt(next); },
      error: (error) => { this.busy.set(false); this.error.set(this.errorText(error)); },
    });
  }

  skipPlacement(): void {
    if (this.busy()) return;
    this.busy.set(true);
    this.api.skip().subscribe({
      next: () => {
        this.setLocalStartingLevel(1, 'skipped');
        void this.router.navigateByUrl('/learn');
      },
      error: (error) => { this.busy.set(false); this.error.set(this.errorText(error)); },
    });
  }

  chooseLevel(level: number): void { this.selectedLevel.set(level); }

  applyLevel(): void {
    if (this.busy() || !this.canApplyLevel()) return;
    this.busy.set(true);
    this.error.set(null);
    this.api.selectLevel(this.selectedLevel()).subscribe({
      next: () => {
        this.setLocalStartingLevel(this.selectedLevel(), 'applied');
        void this.router.navigateByUrl('/learn');
      },
      error: (error) => { this.busy.set(false); this.error.set(this.errorText(error)); },
    });
  }

  labelFor(skill?: PlacementSkill): string {
    return ({ vocabulary: 'Từ vựng', grammar: 'Ngữ pháp', listening: 'Nghe', pronunciation: 'Phát âm' } as const)[skill ?? 'vocabulary'];
  }

  private setAttempt(attempt: PlacementAttempt): void {
    this.releaseUrls();
    this.attempt.set(attempt);
    this.selectedOption.set(null);
    this.recordingReady.set(false);
    this.error.set(null);
    if (attempt.status === 'completed' && attempt.result) {
      this.selectedLevel.set(attempt.result.recommended_level);
      this.phase.set('result');
    } else {
      this.phase.set('test');
    }
  }

  private releaseUrls(): void {
    const recording = this.recordingUrl();
    if (recording) this.audio.revokeRecording(recording);
    const generated = this.audioUrl();
    if (generated) URL.revokeObjectURL(generated);
    this.recordingUrl.set(null);
    this.audioUrl.set(null);
  }

  private errorText(error: any): string {
    return error?.error?.detail ?? 'Đã có lỗi kết nối. Vui lòng thử lại.';
  }

  private setLocalStartingLevel(level: number, status: string): void {
    this.profile.update((profile) => ({
      ...profile,
      startingLevel: level,
      placementTest: { status, selectedLevel: level },
    }));
  }
}
