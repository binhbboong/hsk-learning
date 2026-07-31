import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { of } from 'rxjs';

import { PronunciationLesson } from '../../core/models/skill-lesson';
import { AudioService } from '../../core/services/audio.service';
import { SkillApiService } from '../../core/services/skill-api.service';
import { SkillResultService } from '../../core/services/skill-result.service';
import { Pronunciation } from './pronunciation';


const lesson: PronunciationLesson = {
  id: 'pronunciation',
  level: 1,
  kind: 'pronunciation',
  title: 'Thanh điệu trong 你好',
  goal: 'Luyện hai thanh 3',
  estimated_minutes: 6,
  hanzi: '你好',
  pinyin: 'nǐ hǎo',
  meaning_vi: 'xin chào',
  tone_path: ['nǐ: đọc gần thanh 2', 'hǎo: hạ rồi nâng'],
  common_mistake_vi: 'Người Việt thường đọc hai âm trũng như nhau.',
  correction_tip_vi: 'Đọc nǐ ngắn và đi lên, sau đó hạ rồi nâng ở hǎo.',
};

describe('Pronunciation', () => {
  let fixture: ComponentFixture<Pronunciation>;
  let audio: {
    speak: ReturnType<typeof vi.fn>;
    startRecording: ReturnType<typeof vi.fn>;
    stopRecording: ReturnType<typeof vi.fn>;
    revokeRecording: ReturnType<typeof vi.fn>;
  };

  beforeEach(async () => {
    audio = {
      speak: vi.fn().mockReturnValue(true),
      startRecording: vi.fn().mockResolvedValue(true),
      stopRecording: vi.fn().mockResolvedValue('blob:recording'),
      revokeRecording: vi.fn(),
    };
    await TestBed.configureTestingModule({
      imports: [Pronunciation],
      providers: [
        provideRouter([]),
        { provide: SkillApiService, useValue: { getLesson: () => of(lesson) } },
        { provide: AudioService, useValue: audio },
      ],
    }).compileComponents();
    fixture = TestBed.createComponent(Pronunciation);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
  });

  it('shows the tone path and Vietnamese-specific correction', () => {
    const text = fixture.nativeElement.textContent as string;
    expect(text).toContain('nǐ hǎo');
    expect(text).toContain('nǐ: đọc gần thanh 2');
    expect(text).toContain('Người Việt thường');
    expect(text).toContain('Đọc nǐ ngắn');
  });

  it('records locally and exposes playback', async () => {
    await fixture.componentInstance.startRecording();
    expect(fixture.componentInstance.recording()).toBe(true);

    await fixture.componentInstance.stopRecording();
    fixture.detectChanges();

    expect(audio.stopRecording).toHaveBeenCalled();
    expect(
      fixture.nativeElement.querySelector('audio[data-testid="recording-playback"]')
        ?.getAttribute('src'),
    ).toBe('blob:recording');
  });

  it('falls back to listening and self-practice when microphone is unavailable', async () => {
    audio.startRecording.mockResolvedValue(false);
    await fixture.componentInstance.startRecording();
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Microphone không khả dụng');
    expect(fixture.nativeElement.textContent).toContain('Bạn vẫn có thể nghe mẫu');
  });

  it('requires a self-rating and then stores the result', () => {
    const router = TestBed.inject(Router);
    const navigate = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    fixture.componentInstance.rate('close');
    fixture.componentInstance.complete();

    const result = TestBed.inject(SkillResultService).result();
    expect(result?.kind).toBe('pronunciation');
    expect(result?.score).toBe(2);
    expect(navigate).toHaveBeenCalledWith(['/skills/result']);
  });
});
