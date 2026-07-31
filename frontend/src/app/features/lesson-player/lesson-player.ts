import {
  Component,
  computed,
  inject,
  OnDestroy,
  OnInit,
  signal,
} from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import {
  LessonWord,
  MultiActivityLesson,
} from '../../core/models/learning-content';
import { AudioService } from '../../core/services/audio.service';
import { LearningPathApiService } from '../../core/services/learning-path-api.service';
import { MistakeService } from '../../core/services/mistake.service';
import { NotebookService } from '../../core/services/notebook.service';
import { ProgressService } from '../../core/services/progress.service';
import { SrsService } from '../../core/services/srs.service';
import {
  PronunciationAnalysisService,
  PronunciationResult,
} from '../../core/services/pronunciation-analysis.service';
import { SampleAudioService } from '../../core/services/sample-audio.service';


type LessonStep = 'dialogue' | 'listening' | 'sentence-order' | 'pronunciation';

@Component({
  selector: 'app-lesson-player',
  imports: [RouterLink],
  templateUrl: './lesson-player.html',
  styleUrl: './lesson-player.scss',
})
export class LessonPlayer implements OnInit, OnDestroy {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(LearningPathApiService);
  private readonly audio = inject(AudioService);
  private readonly mistakes = inject(MistakeService);
  private readonly srs = inject(SrsService);
  private readonly pronunciationAnalysis = inject(PronunciationAnalysisService);
  private readonly sampleAudio = inject(SampleAudioService);
  readonly notebook = inject(NotebookService);
  readonly progress = inject(ProgressService);

  readonly lesson = signal<MultiActivityLesson | null>(null);
  readonly loading = signal(true);
  readonly error = signal(false);
  readonly step = signal<LessonStep>('dialogue');
  readonly showPinyin = signal(true);
  readonly showTranslation = signal(true);
  readonly selectedListening = signal<string | null>(null);
  readonly listeningChecked = signal(false);
  readonly arrangedTokens = signal<string[]>([]);
  readonly orderChecked = signal(false);
  readonly recording = signal(false);
  readonly microphoneUnavailable = signal(false);
  readonly recordingUrl = signal<string | null>(null);
  readonly recordingReadyForAnalysis = signal(false);
  readonly recordingIssue = signal<string | null>(null);
  readonly recordingSeconds = signal(0);
  readonly analyzingPronunciation = signal(false);
  readonly pronunciationResult = signal<PronunciationResult | null>(null);
  readonly pronunciationError = signal<string | null>(null);
  readonly generatedAudioUrl = signal<string | null>(null);
  readonly sampleAudioLoading = signal(false);
  readonly sampleAudioError = signal<string | null>(null);
  readonly lessonCompleted = signal(false);
  readonly nextLearningRoute = computed(() => {
    const number = this.lesson()?.number ?? 1;
    return number % 5 === 0 ? '/learn/checkpoint' : `/learn/lesson/${number + 1}`;
  });
  readonly nextLearningQueryParams = computed(() => {
    const number = this.lesson()?.number ?? 1;
    return number % 5 === 0 ? { start: number - 4 } : null;
  });
  readonly nextLearningLabel = computed(() => {
    const number = this.lesson()?.number ?? 1;
    return number % 5 === 0 ? 'Làm checkpoint' : `Học tiếp Bài ${number + 1}`;
  });
  private recordingTimer: ReturnType<typeof setInterval> | null = null;

  readonly availableTokens = computed(() => {
    const source = this.lesson()?.sentence_order.tokens ?? [];
    const selected = [...this.arrangedTokens()];
    return source.filter((token) => {
      const index = selected.indexOf(token);
      if (index === -1) return true;
      selected.splice(index, 1);
      return false;
    });
  });
  readonly stepNumber = computed(
    () =>
      ({
        dialogue: 1,
        listening: 2,
        'sentence-order': 3,
        pronunciation: 4,
      })[this.step()],
  );

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      const number = Number(params.get('number') ?? 1);
      this.loadLesson(number);
    });
  }

  private loadLesson(number: number): void {
    this.resetLessonState();
    this.loading.set(true);
    this.error.set(false);
    this.lesson.set(null);
    this.api.getLesson(number).subscribe({
      next: (lesson) => {
        this.lesson.set(lesson);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      },
    });
  }

  private resetLessonState(): void {
    this.step.set('dialogue');
    this.selectedListening.set(null);
    this.listeningChecked.set(false);
    this.arrangedTokens.set([]);
    this.orderChecked.set(false);
    this.lessonCompleted.set(false);
    this.recording.set(false);
    this.recordingReadyForAnalysis.set(false);
    this.recordingIssue.set(null);
    this.recordingSeconds.set(0);
    this.microphoneUnavailable.set(false);
    this.analyzingPronunciation.set(false);
    this.pronunciationResult.set(null);
    this.pronunciationError.set(null);
    this.sampleAudioLoading.set(false);
    this.sampleAudioError.set(null);
    this.stopRecordingTimer();

    const recordingUrl = this.recordingUrl();
    if (recordingUrl) this.audio.revokeRecording(recordingUrl);
    this.recordingUrl.set(null);

    const generatedUrl = this.generatedAudioUrl();
    if (generatedUrl) URL.revokeObjectURL(generatedUrl);
    this.generatedAudioUrl.set(null);
  }

  ngOnDestroy(): void {
    const url = this.recordingUrl();
    if (url) this.audio.revokeRecording(url);
    const generatedUrl = this.generatedAudioUrl();
    if (generatedUrl) URL.revokeObjectURL(generatedUrl);
    this.stopRecordingTimer();
  }

  goToStep(step: LessonStep): void {
    this.step.set(step);
  }

  togglePinyin(): void {
    this.showPinyin.update((visible) => !visible);
  }

  toggleTranslation(): void {
    this.showTranslation.update((visible) => !visible);
  }

  playLine(text: string): void {
    const speed = 0.82;
    this.sampleAudioError.set(null);
    if (this.audio.speak(text, speed)) return;
    this.sampleAudioLoading.set(true);
    this.sampleAudio.synthesize(text, speed).subscribe({
      next: (blob) => {
        const previous = this.generatedAudioUrl();
        if (previous) URL.revokeObjectURL(previous);
        this.generatedAudioUrl.set(URL.createObjectURL(blob));
        this.sampleAudioLoading.set(false);
      },
      error: (error) => {
        this.sampleAudioError.set(
          error?.error?.detail ?? 'Chưa thể phát giọng mẫu. Vui lòng thử lại.',
        );
        this.sampleAudioLoading.set(false);
      },
    });
  }

  toggleWord(word: LessonWord): void {
    if (this.notebook.has(word.id)) {
      this.notebook.remove(word.id);
      return;
    }
    const lesson = this.lesson();
    if (!lesson) return;
    this.notebook.add({
      id: word.id,
      hanzi: word.hanzi,
      pinyin: word.pinyin,
      meaningVi: word.meaning_vi,
      sourceLessonId: lesson.id,
    });
  }

  selectListening(optionId: string): void {
    if (!this.listeningChecked()) this.selectedListening.set(optionId);
  }

  submitListening(): void {
    const lesson = this.lesson();
    const selected = this.selectedListening();
    if (!lesson || !selected) return;
    if (selected !== lesson.listening.correct_option_id) {
      this.mistakes.add({
        id: lesson.listening.id,
        sourceLessonId: lesson.id,
        kind: 'listening',
        prompt: lesson.listening.prompt_vi,
        correctAnswer:
          lesson.listening.options.find(
            (option) => option.id === lesson.listening.correct_option_id,
          )?.text ?? '',
        explanationVi: lesson.listening.explanation_vi,
      });
    } else {
      this.mistakes.resolve(lesson.listening.id);
    }
    this.listeningChecked.set(true);
  }

  chooseToken(token: string): void {
    if (!this.orderChecked()) {
      this.arrangedTokens.update((tokens) => [...tokens, token]);
    }
  }

  undoToken(): void {
    if (!this.orderChecked()) {
      this.arrangedTokens.update((tokens) => tokens.slice(0, -1));
    }
  }

  submitOrder(): void {
    const lesson = this.lesson();
    if (!lesson || this.arrangedTokens().length !== lesson.sentence_order.tokens.length) {
      return;
    }
    const correct =
      this.arrangedTokens().join('|') ===
      lesson.sentence_order.correct_tokens.join('|');
    if (!correct) {
      this.mistakes.add({
        id: lesson.sentence_order.id,
        sourceLessonId: lesson.id,
        kind: 'sentence-order',
        prompt: lesson.sentence_order.prompt_vi,
        correctAnswer: lesson.sentence_order.correct_tokens.join(' '),
        explanationVi: lesson.sentence_order.explanation_vi,
      });
    } else {
      this.mistakes.resolve(lesson.sentence_order.id);
    }
    this.orderChecked.set(true);
  }

  async startRecording(): Promise<void> {
    this.pronunciationResult.set(null);
    this.pronunciationError.set(null);
    this.recordingIssue.set(null);
    this.recordingReadyForAnalysis.set(false);
    const started = await this.audio.startRecording();
    this.recording.set(started);
    this.microphoneUnavailable.set(!started);
    if (started) {
      this.recordingSeconds.set(0);
      this.recordingTimer = setInterval(
        () => this.recordingSeconds.update((seconds) => seconds + 1),
        1000,
      );
    }
  }

  analyzePronunciation(): void {
    const lesson = this.lesson();
    const blob = this.audio.recordingBlob();
    if (!lesson || !blob || !this.recordingReadyForAnalysis()) return;
    const pinyin = lesson.dialogue.find(
      (line) => line.audio_text === lesson.pronunciation_text,
    )?.pinyin ?? '';
    this.analyzingPronunciation.set(true);
    this.pronunciationError.set(null);
    this.pronunciationAnalysis.analyze(blob, lesson.pronunciation_text, pinyin).subscribe({
      next: (result) => {
        this.pronunciationResult.set(result);
        this.progress.recordActivity(undefined, 'pronunciation', result.score);
        this.analyzingPronunciation.set(false);
      },
      error: (error) => {
        this.pronunciationError.set(
          error?.error?.detail ?? 'AI chưa thể phân tích bản thu này. Bạn vẫn có thể nghe lại và thử lại.',
        );
        this.analyzingPronunciation.set(false);
      },
    });
  }

  async stopRecording(): Promise<void> {
    const url = await this.audio.stopRecording();
    this.stopRecordingTimer();
    this.recording.set(false);
    if (url) {
      const previous = this.recordingUrl();
      if (previous) this.audio.revokeRecording(previous);
      this.recordingUrl.set(url);
      const quality = this.audio.recordingQuality();
      if (quality.durationMs < 800) {
        this.recordingIssue.set('Bản thu quá ngắn. Hãy nói ít nhất 1 giây rồi dừng thu.');
      } else if (quality.size < 512) {
        this.recordingIssue.set('Bản thu không có dữ liệu âm thanh. Hãy kiểm tra microphone.');
      } else if (quality.hasSpeech === false) {
        this.recordingIssue.set('Không phát hiện giọng nói. Hãy nói gần microphone và thử lại.');
      } else {
        this.recordingReadyForAnalysis.set(true);
      }
    }
  }

  private stopRecordingTimer(): void {
    if (this.recordingTimer) clearInterval(this.recordingTimer);
    this.recordingTimer = null;
  }

  completeLesson(): void {
    const lesson = this.lesson();
    if (!lesson) return;
    for (const word of lesson.vocabulary) {
      this.srs.schedule(
        {
          id: word.id,
          hanzi: word.hanzi,
          pinyin: word.pinyin,
          meaningVi: word.meaning_vi,
          sourceLessonId: lesson.id,
        },
        'remembered',
      );
    }
    this.progress.completeLesson(lesson.id);
    this.lessonCompleted.set(true);
  }
}
