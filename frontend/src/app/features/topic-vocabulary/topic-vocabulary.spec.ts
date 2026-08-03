import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of, throwError } from 'rxjs';
import { vi } from 'vitest';

import { TopicRecommendationsResponse, TopicVocabularySession } from '../../core/models/topic-vocabulary';
import { AudioService } from '../../core/services/audio.service';
import { SampleAudioService } from '../../core/services/sample-audio.service';
import { LearningProfileRepository } from '../../core/services/learning-profile.repository';
import { TopicVocabularyApiService } from '../../core/services/topic-vocabulary-api.service';
import { TopicVocabulary } from './topic-vocabulary';


const recommendations: TopicRecommendationsResponse = {
  source: 'curated',
  items: Array.from({ length: 5 }, (_, index) => ({
    id: `topic-${index}`,
    name_vi: `Chủ đề ${index + 1}`,
    description_vi: 'Từ vựng thực tế.',
    reason_vi: 'Phù hợp với HSK hiện tại.',
    word_count: 10 as const,
    level: 1,
    learned_count: 0,
    remembered_count: 0,
  })),
};

const session: TopicVocabularySession = {
  id: 'topic-0-session-1',
  topic_id: 'topic-0',
  topic_name_vi: 'Chủ đề 1',
  level: 1,
  source: 'curated',
  words: Array.from({ length: 10 }, (_, index) => ({
    id: `word:${index}`,
    hanzi: `词${index}`,
    pinyin: `cí ${index}`,
    sino_vietnamese: 'TỪ',
    meaning_vi: `nghĩa ${index}`,
    example_zh: `这是词${index}。`,
    example_vi: `Đây là từ ${index}.`,
    audio_text: `词${index}`,
    example_audio_text: `这是词${index}。`,
    is_extension: false,
  })),
};

describe('TopicVocabulary', () => {
  const api = {
    recommendations: vi.fn(() => of(recommendations)),
    startSession: vi.fn(() => of(session)),
  };
  const deviceAudio = { speak: vi.fn(() => true) };
  const sampleAudio = { synthesize: vi.fn(() => of(new Blob())) };

  beforeEach(async () => {
    localStorage.clear();
    api.recommendations.mockClear();
    api.startSession.mockClear();
    deviceAudio.speak.mockClear();
    sampleAudio.synthesize.mockReset();
    sampleAudio.synthesize.mockReturnValue(of(new Blob()));
    await TestBed.configureTestingModule({
      imports: [TopicVocabulary],
      providers: [
        provideRouter([]),
        { provide: TopicVocabularyApiService, useValue: api },
        { provide: AudioService, useValue: deviceAudio },
        { provide: SampleAudioService, useValue: sampleAudio },
      ],
    }).compileComponents();
  });

  it('shows at least five recommended topics and identifies curated fallback', () => {
    const fixture = TestBed.createComponent(TopicVocabulary);
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelectorAll('[data-testid="topic-card"]')).toHaveLength(5);
    expect(fixture.nativeElement.textContent).toContain('chủ đề đã kiểm duyệt');
    expect(fixture.nativeElement.textContent).toContain('10 từ');
  });

  it('starts with a concealed flipcard and reveals all learning details', () => {
    const fixture = TestBed.createComponent(TopicVocabulary);
    fixture.detectChanges();
    fixture.componentInstance.start(recommendations.items[0]);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('词0');
    expect(fixture.nativeElement.textContent).not.toContain('nghĩa 0');

    fixture.componentInstance.reveal();
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('cí 0');
    expect(fixture.nativeElement.textContent).toContain('TỪ');
    expect(fixture.nativeElement.textContent).toContain('nghĩa 0');
    expect(fixture.nativeElement.textContent).toContain('Đây là từ 0.');
  });

  it('uses AI audio for the Hanzi before the device speech engine', () => {
    vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:topic-audio');
    const fixture = TestBed.createComponent(TopicVocabulary);
    fixture.detectChanges();
    fixture.componentInstance.start(recommendations.items[0]);

    fixture.componentInstance.playAudio(session.words[0].audio_text);

    expect(sampleAudio.synthesize).toHaveBeenCalledWith('词0', 0.85);
    expect(deviceAudio.speak).not.toHaveBeenCalled();
  });

  it('falls back to device speech when AI audio is unavailable', () => {
    sampleAudio.synthesize.mockReturnValue(throwError(() => new Error('TTS unavailable')));
    const fixture = TestBed.createComponent(TopicVocabulary);
    fixture.detectChanges();

    fixture.componentInstance.playAudio('你好');

    expect(sampleAudio.synthesize).toHaveBeenCalledWith('你好', 0.85);
    expect(deviceAudio.speak).toHaveBeenCalledWith('你好', 0.85);
    expect(fixture.componentInstance.audioError()).toBeNull();
  });

  it('opens four-answer recall after all ten flipcards', () => {
    const fixture = TestBed.createComponent(TopicVocabulary);
    fixture.detectChanges();
    fixture.componentInstance.start(recommendations.items[0]);
    for (let index = 0; index < 10; index += 1) {
      fixture.componentInstance.reveal();
      fixture.componentInstance.nextCard();
    }
    fixture.detectChanges();

    expect(fixture.nativeElement.querySelectorAll('[data-testid="quiz-option"]')).toHaveLength(4);
    expect(fixture.nativeElement.textContent).toContain('Câu 1 / 10');
  });

  it('keeps a wrong answer until continue and auto-advances a correct answer', () => {
    vi.useFakeTimers();
    try {
      const fixture = TestBed.createComponent(TopicVocabulary);
      fixture.detectChanges();
      fixture.componentInstance.start(recommendations.items[0]);
      for (let index = 0; index < 10; index += 1) {
        fixture.componentInstance.reveal();
        fixture.componentInstance.nextCard();
      }

      fixture.componentInstance.chooseAnswer('đáp án sai');
      vi.advanceTimersByTime(1000);
      expect(fixture.componentInstance.session.progress()?.quizIndex).toBe(0);

      fixture.componentInstance.continueQuiz();
      fixture.componentInstance.chooseAnswer(session.words[1].meaning_vi);
      vi.advanceTimersByTime(800);

      expect(fixture.componentInstance.session.progress()?.quizIndex).toBe(2);
    } finally {
      vi.useRealTimers();
    }
  });

  it('shows local in-progress state and resumes the saved quiz position', () => {
    TestBed.inject(LearningProfileRepository).update((profile) => ({
      ...profile,
      topicVocabularyProgress: [{
        topicId: 'topic-0',
        sessionId: 'topic-0-session-1',
        phase: 'quiz',
        cardIndex: 10,
        quizIndex: 2,
        learnedWordIds: session.words.map((word) => word.id),
        correctWordIds: [session.words[1].id],
        updatedAt: '2026-08-01T00:00:00Z',
      }],
    }));
    const fixture = TestBed.createComponent(TopicVocabulary);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('10 / 10 từ đã học');
    expect(fixture.nativeElement.textContent).toContain('Tiếp tục');

    fixture.componentInstance.start(recommendations.items[0]);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Câu 3 / 10');
  });

  it('offers a clear return to the daily learning path after completion', () => {
    TestBed.inject(LearningProfileRepository).update((profile) => ({
      ...profile,
      topicVocabularyProgress: [{
        topicId: 'topic-0',
        sessionId: 'topic-0-session-1',
        phase: 'completed',
        cardIndex: 10,
        quizIndex: 10,
        learnedWordIds: session.words.map((word) => word.id),
        correctWordIds: session.words.map((word) => word.id),
        updatedAt: '2026-08-03T00:00:00Z',
      }],
    }));
    const fixture = TestBed.createComponent(TopicVocabulary);
    fixture.detectChanges();
    fixture.componentInstance.start(recommendations.items[0]);
    fixture.detectChanges();

    const returnLink = fixture.nativeElement.querySelector('[data-testid="return-to-learning-path"]');
    expect(returnLink).not.toBeNull();
    expect(returnLink.getAttribute('href')).toBe('/learn');
  });
});
