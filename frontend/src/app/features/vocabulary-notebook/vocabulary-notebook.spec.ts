import { TestBed } from '@angular/core/testing';
import { provideRouter } from '@angular/router';

import { NotebookService } from '../../core/services/notebook.service';
import { VocabularyNotebook } from './vocabulary-notebook';


describe('VocabularyNotebook', () => {
  it('lists saved words with source and supports removal', async () => {
    localStorage.clear();
    await TestBed.configureTestingModule({
      imports: [VocabularyNotebook],
      providers: [provideRouter([])],
    }).compileComponents();
    const notebook = TestBed.inject(NotebookService);
    notebook.add({
      id: 'word-1',
      hanzi: '你',
      pinyin: 'nǐ',
      meaningVi: 'bạn',
      sourceLessonId: 'hsk1-lesson-1',
    });
    const fixture = TestBed.createComponent(VocabularyNotebook);
    fixture.detectChanges();
    const element = fixture.nativeElement as HTMLElement;

    expect(element.textContent).toContain('你');
    expect(element.textContent).toContain('nǐ');
    expect(element.textContent).toContain('hsk1-lesson-1');
    expect(element.querySelector('[data-testid="review-notebook"]')?.getAttribute('href')).toContain('/learn/review');

    fixture.componentInstance.remove('word-1');
    fixture.detectChanges();
    expect(element.textContent).toContain('Sổ từ đang trống');
  });
});
