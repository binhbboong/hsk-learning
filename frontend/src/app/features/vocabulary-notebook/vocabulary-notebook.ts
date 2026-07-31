import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { NotebookService } from '../../core/services/notebook.service';


@Component({
  selector: 'app-vocabulary-notebook',
  imports: [RouterLink],
  templateUrl: './vocabulary-notebook.html',
  styleUrl: './vocabulary-notebook.scss',
})
export class VocabularyNotebook {
  readonly notebook = inject(NotebookService);

  remove(wordId: string): void {
    this.notebook.remove(wordId);
  }
}
