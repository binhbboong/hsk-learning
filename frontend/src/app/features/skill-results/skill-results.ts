import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';

import { SkillResultService } from '../../core/services/skill-result.service';


@Component({
  selector: 'app-skill-results',
  imports: [RouterLink],
  templateUrl: './skill-results.html',
  styleUrl: './skill-results.scss',
})
export class SkillResults {
  readonly results = inject(SkillResultService);

  label(kind: string): string {
    return {
      grammar: 'ngữ pháp',
      listening: 'nghe hiểu',
      pronunciation: 'phát âm',
    }[kind] ?? 'kỹ năng';
  }
}
