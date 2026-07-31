import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { of } from 'rxjs';

import { ListeningLesson } from '../../core/models/skill-lesson';
import { AudioService } from '../../core/services/audio.service';
import { SkillApiService } from '../../core/services/skill-api.service';
import { SkillResultService } from '../../core/services/skill-result.service';
import { Listening } from './listening';


const lesson: ListeningLesson = {
  id: 'listening',
  level: 1,
  kind: 'listening',
  title: 'Nghe lời chào',
  goal: 'Nhận ra tên',
  estimated_minutes: 5,
  utterance_zh: '你好，我是王明。',
  pinyin: 'Nǐ hǎo, wǒ shì Wáng Míng.',
  meaning_vi: 'Xin chào, tôi là Vương Minh.',
  question_vi: 'Người nói tên gì?',
  options: [{ id: 'a', text: 'Vương Minh' }, { id: 'b', text: 'Lý Hoa' }],
  correct_option_id: 'a',
  explanation_vi: '我是王明 nghĩa là tôi là Vương Minh.',
};

describe('Listening', () => {
  let fixture: ComponentFixture<Listening>;
  let audio: { speak: ReturnType<typeof vi.fn> };

  beforeEach(async () => {
    audio = { speak: vi.fn().mockReturnValue(true) };
    await TestBed.configureTestingModule({
      imports: [Listening],
      providers: [
        provideRouter([]),
        { provide: SkillApiService, useValue: { getLesson: () => of(lesson) } },
        { provide: AudioService, useValue: audio },
      ],
    }).compileComponents();
    fixture = TestBed.createComponent(Listening);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
  });

  it('plays normal and slow speech while keeping transcript hidden', () => {
    const element = fixture.nativeElement as HTMLElement;
    expect(element.textContent).not.toContain(lesson.pinyin);

    (element.querySelector('[data-testid="play-normal"]') as HTMLButtonElement).click();
    (element.querySelector('[data-testid="play-slow"]') as HTMLButtonElement).click();

    expect(audio.speak).toHaveBeenNthCalledWith(1, lesson.utterance_zh, 0.86);
    expect(audio.speak).toHaveBeenNthCalledWith(2, lesson.utterance_zh, 0.62);
  });

  it('reveals transcript on request and completes the answer', () => {
    const router = TestBed.inject(Router);
    const navigate = vi.spyOn(router, 'navigate').mockResolvedValue(true);
    const element = fixture.nativeElement as HTMLElement;

    (element.querySelector('[data-testid="show-transcript"]') as HTMLButtonElement).click();
    fixture.detectChanges();
    expect(element.textContent).toContain(lesson.pinyin);

    fixture.componentInstance.select('a');
    fixture.componentInstance.submit();

    expect(TestBed.inject(SkillResultService).result()?.score).toBe(1);
    expect(navigate).toHaveBeenCalledWith(['/skills/result']);
  });

  it('offers transcript fallback when speech is unavailable', () => {
    audio.speak.mockReturnValue(false);
    fixture.componentInstance.play(0.86);
    fixture.detectChanges();

    expect(fixture.nativeElement.textContent).toContain('Thiết bị không phát được audio');
    expect(fixture.nativeElement.textContent).toContain(lesson.pinyin);
  });
});
