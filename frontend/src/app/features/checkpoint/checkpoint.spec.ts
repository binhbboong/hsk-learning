import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';
import { of } from 'rxjs';

import { Checkpoint as CheckpointModel } from '../../core/models/learning-content';
import { LearningPathApiService } from '../../core/services/learning-path-api.service';
import { LearningProfileRepository } from '../../core/services/learning-profile.repository';
import { MistakeService } from '../../core/services/mistake.service';
import { Checkpoint } from './checkpoint';

const checkpoint: CheckpointModel = {
  id: 'hsk1-checkpoint-1-5',
  title: 'Kiểm tra Bài 1–5',
  lesson_ids: Array.from({ length: 5 }, (_, index) => `hsk1-lesson-${index + 1}`),
  questions: [
    {
      id: 'cp-1', kind: 'listening', prompt_vi: 'Bạn nghe thấy lời chào nào?',
      audio_text: '你好', options: [{ id: 'a', text: '你好' }, { id: 'b', text: '谢谢' }],
      tokens: [], correct_answer: 'a', explanation_vi: '你好 nghĩa là xin chào.',
    },
    {
      id: 'cp-2', kind: 'sentence-order', prompt_vi: 'Sắp xếp thành câu',
      audio_text: null, options: [], tokens: ['学生', '是', '我'],
      correct_answer: '我 是 学生', explanation_vi: 'Trật tự: chủ ngữ + 是 + danh từ.',
    },
  ],
};

describe('Checkpoint', () => {
  beforeEach(async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [Checkpoint],
      providers: [
        provideRouter([]),
        { provide: LearningPathApiService, useValue: { getCheckpoint: () => of(checkpoint) } },
      ],
    }).compileComponents();
  });

  it('remains locked before five lessons are complete', async () => {
    const fixture = TestBed.createComponent(Checkpoint);
    fixture.detectChanges();
    await fixture.whenStable();
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('Chưa mở khóa');
  });

  it('saves the result and sends wrong answers to mistake review', async () => {
    const repository = TestBed.inject(LearningProfileRepository);
    repository.update((profile) => ({ ...profile, completedLessonIds: checkpoint.lesson_ids }));
    const fixture = TestBed.createComponent(Checkpoint);
    fixture.detectChanges();
    await fixture.whenStable();

    fixture.componentInstance.selectOption('b');
    fixture.componentInstance.submitAnswer();
    fixture.componentInstance.chooseToken('我');
    fixture.componentInstance.chooseToken('是');
    fixture.componentInstance.chooseToken('学生');
    fixture.componentInstance.submitAnswer();

    expect(repository.profile().checkpointResults).toHaveLength(1);
    expect(repository.profile().checkpointResults[0].score).toBe(1);
    expect(TestBed.inject(MistakeService).items()).toHaveLength(1);
    fixture.detectChanges();
    expect(fixture.nativeElement.textContent).toContain('1 / 2');
  });
});
