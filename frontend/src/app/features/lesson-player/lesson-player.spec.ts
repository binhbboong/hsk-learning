import { TestBed } from '@angular/core/testing';
import { ActivatedRoute, provideRouter, Router } from '@angular/router';
import { BehaviorSubject, of, throwError } from 'rxjs';

import { MultiActivityLesson } from '../../core/models/learning-content';
import { AudioService } from '../../core/services/audio.service';
import { LearningPathApiService } from '../../core/services/learning-path-api.service';
import { MistakeService } from '../../core/services/mistake.service';
import { NotebookService } from '../../core/services/notebook.service';
import { ProgressService } from '../../core/services/progress.service';
import { PronunciationAnalysisService } from '../../core/services/pronunciation-analysis.service';
import { SampleAudioService } from '../../core/services/sample-audio.service';
import { LessonPlayer } from './lesson-player';


const lesson: MultiActivityLesson = {
  id: 'hsk1-lesson-1',
  number: 1,
  level: 1,
  title: 'Chào hỏi và giới thiệu',
  goal: 'Chào hỏi và nói tên',
  estimated_minutes: 10,
  dialogue: [
    { id: 'line-1', speaker: 'Mai', hanzi: '你好！', audio_text: '你好！', pinyin: 'Nǐ hǎo!', translation_vi: 'Xin chào!' },
    { id: 'line-2', speaker: '王明', hanzi: '我是王明。', audio_text: '我是王明。', pinyin: 'Wǒ shì Wáng Míng.', translation_vi: 'Tôi là Vương Minh.' },
  ],
  listening: {
    id: 'listen-1', audio_text: '我是王明。', prompt_vi: 'Người nói tên gì?',
    options: [{ id: 'a', text: 'Vương Minh' }, { id: 'b', text: 'Lý Hoa' }],
    correct_option_id: 'a', transcript_zh: '我是王明。', pinyin: 'Wǒ shì Wáng Míng.',
    translation_vi: 'Tôi là Vương Minh.', explanation_vi: 'Nghe từ 王明.',
  },
  sentence_order: {
    id: 'order-1', prompt_vi: 'Sắp xếp câu đúng', tokens: ['学生', '是', '我'],
    correct_tokens: ['我', '是', '学生'], pinyin: 'Wǒ shì xuésheng.',
    translation_vi: 'Tôi là học sinh.', explanation_vi: 'Chủ thể đứng trước.',
  },
  vocabulary: [
    { id: 'word-1', hanzi: '你', pinyin: 'nǐ', meaning_vi: 'bạn' },
    { id: 'word-2', hanzi: '好', pinyin: 'hǎo', meaning_vi: 'tốt' },
  ],
  pronunciation_text: '你好！',
};

describe('LessonPlayer', () => {
  let audio: {
    speak: ReturnType<typeof vi.fn>;
    startRecording: ReturnType<typeof vi.fn>;
    stopRecording: ReturnType<typeof vi.fn>;
    revokeRecording: ReturnType<typeof vi.fn>;
    recordingBlob: ReturnType<typeof vi.fn>;
    recordingQuality: ReturnType<typeof vi.fn>;
  };
  let sampleAudio: { synthesize: ReturnType<typeof vi.fn> };
  let pronunciationAnalysis: { analyze: ReturnType<typeof vi.fn> };
  let routeParams: BehaviorSubject<{ get: (name: string) => string | null }>;

  beforeEach(async () => {
    localStorage.clear();
    audio = {
      speak: vi.fn().mockReturnValue(true),
      startRecording: vi.fn().mockResolvedValue(true),
      stopRecording: vi.fn().mockResolvedValue('blob:lesson-recording'),
      revokeRecording: vi.fn(),
      recordingBlob: vi.fn().mockReturnValue(new Blob(['audio'], { type: 'audio/webm' })),
      recordingQuality: vi.fn().mockReturnValue({
        durationMs: 2000,
        hasSpeech: true,
        size: 5000,
      }),
    };
    sampleAudio = {
      synthesize: vi.fn().mockReturnValue(of(new Blob(['mp3'], { type: 'audio/mpeg' }))),
    };
    pronunciationAnalysis = {
      analyze: vi.fn().mockReturnValue(of({
        verdict: 'correct', score: 95, content_score: 100, transcript: '你好！',
        feedback_vi: 'AI đã nhận diện đúng câu mẫu.', focus_vi: [],
        syllables: [
          { target: 'nǐ', tone: 3, status: 'good', heard: 'nǐ', tip_vi: 'Hạ thấp rồi nhấc nhẹ.' },
          { target: 'hǎo', tone: 3, status: 'review', heard: 'hao', tip_vi: 'Giữ thanh 3 rõ hơn.' },
        ],
        disclaimer_vi: 'Phản hồi AI chỉ hỗ trợ luyện tập, không phải điểm thi hay đánh giá của giáo viên.',
      })),
    };
    routeParams = new BehaviorSubject<{
      get: (name: string) => string | null;
    }>({
      get: (name: string) => (name === 'number' ? '1' : null),
    });
    await TestBed.configureTestingModule({
      imports: [LessonPlayer],
      providers: [
        provideRouter([]),
        {
          provide: ActivatedRoute,
          useValue: {
            snapshot: { paramMap: { get: () => '1' } },
            paramMap: routeParams,
          },
        },
        {
          provide: LearningPathApiService,
          useValue: {
            getLesson: (number: number) =>
              of({ ...lesson, id: `hsk1-lesson-${number}`, number }),
          },
        },
        { provide: AudioService, useValue: audio },
        { provide: SampleAudioService, useValue: sampleAudio },
        {
          provide: PronunciationAnalysisService,
          useValue: pronunciationAnalysis,
        },
      ],
    }).compileComponents();
  });

  it('plays each dialogue line and toggles pinyin and translation independently', async () => {
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    expect(element.textContent).toContain('Nǐ hǎo!');
    expect(element.textContent).toContain('Xin chào!');
    fixture.componentInstance.togglePinyin();
    fixture.detectChanges();
    expect(element.textContent).not.toContain('Nǐ hǎo!');
    expect(element.textContent).toContain('Xin chào!');
    fixture.componentInstance.toggleTranslation();
    fixture.detectChanges();
    expect(element.textContent).not.toContain('Xin chào!');

    (element.querySelector('[data-testid="play-line-line-1"]') as HTMLButtonElement).click();
    expect(sampleAudio.synthesize).toHaveBeenCalledWith('你好！', 0.82);
    expect(audio.speak).not.toHaveBeenCalled();
  });

  it('loads generated sample audio before using the browser speech engine', async () => {
    vi.spyOn(URL, 'createObjectURL').mockReturnValue('blob:generated-sample');
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();

    fixture.componentInstance.playLine('你好！');
    fixture.detectChanges();

    expect(sampleAudio.synthesize).toHaveBeenCalledWith('你好！', 0.82);
    expect(fixture.componentInstance.generatedAudioUrl()).toBe('blob:generated-sample');
  });

  it('falls back to the browser speech engine when AI audio fails', async () => {
    sampleAudio.synthesize.mockReturnValue(throwError(() => new Error('TTS unavailable')));
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();

    fixture.componentInstance.playLine('你好！');

    expect(sampleAudio.synthesize).toHaveBeenCalledWith('你好！', 0.82);
    expect(audio.speak).toHaveBeenCalledWith('你好！', 0.82);
    expect(fixture.componentInstance.sampleAudioError()).toBeNull();
  });

  it('does not send a silent recording for AI analysis', async () => {
    audio.recordingQuality.mockReturnValue({
      durationMs: 1800,
      hasSpeech: false,
      size: 4000,
    });
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.componentInstance.goToStep('pronunciation');
    await fixture.componentInstance.startRecording();
    await fixture.componentInstance.stopRecording();
    fixture.detectChanges();

    fixture.componentInstance.analyzePronunciation();

    expect(pronunciationAnalysis.analyze).not.toHaveBeenCalled();
    expect(fixture.componentInstance.recordingReadyForAnalysis()).toBe(false);
    expect(fixture.nativeElement.textContent).toContain('Không phát hiện giọng nói');
  });

  it('shows syllable and tone feedback with the assistive disclaimer', async () => {
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.componentInstance.goToStep('pronunciation');
    fixture.componentInstance.recordingReadyForAnalysis.set(true);
    fixture.componentInstance.analyzePronunciation();
    fixture.detectChanges();

    const element = fixture.nativeElement as HTMLElement;
    expect(element.querySelectorAll('[data-testid="syllable-feedback"]')).toHaveLength(2);
    expect(element.textContent).toContain('nǐ · thanh 3');
    expect(element.textContent).toContain('Giữ thanh 3 rõ hơn.');
    expect(element.textContent).toContain('không phải điểm thi');
  });

  it('saves a word, records a wrong listening answer and supports sentence undo', async () => {
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.componentInstance.toggleWord(lesson.vocabulary[0]);
    expect(TestBed.inject(NotebookService).words()).toHaveLength(1);

    fixture.componentInstance.goToStep('listening');
    fixture.componentInstance.selectListening('b');
    fixture.componentInstance.submitListening();
    expect(TestBed.inject(MistakeService).items()).toHaveLength(1);

    fixture.componentInstance.goToStep('sentence-order');
    fixture.componentInstance.chooseToken('我');
    fixture.componentInstance.chooseToken('是');
    fixture.componentInstance.undoToken();
    expect(fixture.componentInstance.arrangedTokens()).toEqual(['我']);
  });

  it('shows the sentence pinyin only after a correct order is confirmed', async () => {
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.componentInstance.goToStep('sentence-order');
    fixture.detectChanges();

    expect(
      fixture.nativeElement.querySelector('[data-testid="order-pinyin"]'),
    ).toBeNull();

    for (const token of lesson.sentence_order.correct_tokens) {
      fixture.componentInstance.chooseToken(token);
    }
    fixture.componentInstance.submitOrder();
    fixture.detectChanges();

    expect(
      fixture.nativeElement.querySelector('[data-testid="order-pinyin"]')
        ?.textContent,
    ).toContain(lesson.sentence_order.pinyin);
  });

  it('does not reveal sentence pinyin after an incorrect order', async () => {
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.componentInstance.goToStep('sentence-order');
    for (const token of lesson.sentence_order.tokens) {
      fixture.componentInstance.chooseToken(token);
    }
    fixture.componentInstance.submitOrder();
    fixture.detectChanges();

    expect(
      fixture.nativeElement.querySelector('[data-testid="order-pinyin"]'),
    ).toBeNull();
  });

  it('completes after recording fallback and updates lesson progress', async () => {
    const router = TestBed.inject(Router);
    vi.spyOn(router, 'navigate').mockResolvedValue(true);
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();

    fixture.componentInstance.completeLesson();
    fixture.detectChanges();

    expect(TestBed.inject(ProgressService).completedCount()).toBe(1);
    expect(TestBed.inject(ProgressService).streak()).toBe(1);
    expect(router.navigate).not.toHaveBeenCalled();
    expect(fixture.nativeElement.textContent).toContain('Hoàn thành Bài 1');
    expect(fixture.nativeElement.textContent).toContain('Học tiếp Bài 2');
    expect(fixture.nativeElement.textContent).toContain('học tiếp bài kế tiếp ngay');
    expect(
      fixture.nativeElement.querySelector('[data-testid="continue-next-lesson"]')
        ?.getAttribute('href'),
    ).toBe('/learn/lesson/2');
  });

  it('starts the next lesson from the first activity with a clean state', async () => {
    const fixture = TestBed.createComponent(LessonPlayer);
    fixture.detectChanges();
    await fixture.whenStable();

    fixture.componentInstance.goToStep('pronunciation');
    fixture.componentInstance.selectedListening.set('b');
    fixture.componentInstance.listeningChecked.set(true);
    fixture.componentInstance.arrangedTokens.set(['我']);
    fixture.componentInstance.orderChecked.set(true);
    fixture.componentInstance.completeLesson();

    routeParams.next({
      get: (name: string) => (name === 'number' ? '2' : null),
    });
    fixture.detectChanges();

    expect(fixture.componentInstance.lesson()?.number).toBe(2);
    expect(fixture.componentInstance.step()).toBe('dialogue');
    expect(fixture.componentInstance.selectedListening()).toBeNull();
    expect(fixture.componentInstance.listeningChecked()).toBe(false);
    expect(fixture.componentInstance.arrangedTokens()).toEqual([]);
    expect(fixture.componentInstance.orderChecked()).toBe(false);
    expect(fixture.componentInstance.lessonCompleted()).toBe(false);
    expect(fixture.nativeElement.textContent).toContain('Hoạt động 1');
  });
});
