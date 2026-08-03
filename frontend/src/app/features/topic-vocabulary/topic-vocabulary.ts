import { Component, inject, OnDestroy, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { TopicRecommendation } from '../../core/models/topic-vocabulary';
import { AudioService } from '../../core/services/audio.service';
import { SampleAudioService } from '../../core/services/sample-audio.service';
import { TopicVocabularyApiService } from '../../core/services/topic-vocabulary-api.service';
import { TopicVocabularySessionService } from '../../core/services/topic-vocabulary-session.service';
import { LearningProfileRepository } from '../../core/services/learning-profile.repository';


@Component({
  selector: 'app-topic-vocabulary',
  imports: [RouterLink],
  templateUrl: './topic-vocabulary.html',
  styleUrl: './topic-vocabulary.scss',
})
export class TopicVocabulary implements OnInit, OnDestroy {
  private readonly api = inject(TopicVocabularyApiService);
  private readonly audio = inject(AudioService);
  private readonly sampleAudio = inject(SampleAudioService);
  readonly session = inject(TopicVocabularySessionService);
  private readonly repository = inject(LearningProfileRepository);

  readonly topics = signal<TopicRecommendation[]>([]);
  readonly source = signal<'ai' | 'curated'>('ai');
  readonly loading = signal(true);
  readonly error = signal<string | null>(null);
  readonly cardRevealed = signal(false);
  readonly audioLoading = signal(false);
  readonly audioError = signal<string | null>(null);
  readonly generatedAudioUrl = signal<string | null>(null);
  private autoAdvanceTimer: ReturnType<typeof setTimeout> | null = null;

  ngOnInit(): void {
    this.loadRecommendations();
  }

  ngOnDestroy(): void {
    if (this.autoAdvanceTimer) clearTimeout(this.autoAdvanceTimer);
    const url = this.generatedAudioUrl();
    if (url) URL.revokeObjectURL(url);
  }

  refresh(): void {
    this.loadRecommendations(true);
  }

  start(topic: TopicRecommendation): void {
    this.loading.set(true);
    this.error.set(null);
    this.api.startSession(topic.id).subscribe({
      next: (session) => {
        this.session.open(session);
        this.cardRevealed.set(false);
        this.loading.set(false);
      },
      error: (error) => {
        this.error.set(error?.error?.detail ?? 'Chưa thể chuẩn bị phiên 10 từ. Vui lòng thử lại.');
        this.loading.set(false);
      },
    });
  }

  backToTopics(): void {
    this.session.session.set(null);
    this.session.answerResult.set(null);
    this.cardRevealed.set(false);
  }

  reveal(): void {
    this.cardRevealed.set(true);
  }

  nextCard(): void {
    if (!this.cardRevealed()) return;
    this.session.completeCurrentCard();
    this.cardRevealed.set(false);
  }

  chooseAnswer(answer: string): void {
    const result = this.session.answer(answer);
    if (result.correct && !this.autoAdvanceTimer) {
      this.autoAdvanceTimer = setTimeout(() => {
        this.autoAdvanceTimer = null;
        this.continueQuiz();
      }, 700);
    }
  }

  continueQuiz(): void {
    if (this.autoAdvanceTimer) {
      clearTimeout(this.autoAdvanceTimer);
      this.autoAdvanceTimer = null;
    }
    this.session.continueQuiz();
  }

  playAudio(text: string): void {
    this.audioError.set(null);
    this.audioLoading.set(true);
    this.sampleAudio.synthesize(text, 0.85).subscribe({
      next: (blob) => {
        const previous = this.generatedAudioUrl();
        if (previous) URL.revokeObjectURL(previous);
        this.generatedAudioUrl.set(URL.createObjectURL(blob));
        this.audioLoading.set(false);
      },
      error: (error) => {
        if (this.audio.speak(text, 0.85)) {
          this.audioLoading.set(false);
          return;
        }
        this.audioError.set(error?.error?.detail ?? 'Chưa thể phát giọng mẫu.');
        this.audioLoading.set(false);
      },
    });
  }

  progressPercent(): number {
    const progress = this.session.progress();
    if (!progress) return 0;
    if (progress.phase === 'cards') return progress.cardIndex * 5;
    if (progress.phase === 'quiz') return 50 + progress.quizIndex * 5;
    return 100;
  }

  learnedCount(topic: TopicRecommendation): number {
    const local = this.repository.profile().topicVocabularyProgress.find(
      (item) => item.topicId === topic.id,
    );
    return Math.max(topic.learned_count, local?.learnedWordIds.length ?? 0);
  }

  actionLabel(topic: TopicRecommendation): string {
    const local = this.repository.profile().topicVocabularyProgress.find(
      (item) => item.topicId === topic.id,
    );
    if (local?.phase === 'completed') return 'Xem kết quả';
    return this.learnedCount(topic) > 0 ? 'Tiếp tục' : 'Bắt đầu';
  }

  private loadRecommendations(refresh = false): void {
    this.loading.set(true);
    this.error.set(null);
    this.api.recommendations(refresh).subscribe({
      next: (response) => {
        this.topics.set(response.items);
        this.source.set(response.source);
        this.loading.set(false);
      },
      error: (error) => {
        this.error.set(error?.error?.detail ?? 'Chưa thể tải chủ đề. Vui lòng thử lại.');
        this.loading.set(false);
      },
    });
  }
}
