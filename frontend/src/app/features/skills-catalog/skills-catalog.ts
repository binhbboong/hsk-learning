import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { SkillCatalog } from '../../core/models/skill-lesson';
import { SkillApiService } from '../../core/services/skill-api.service';


@Component({
  selector: 'app-skills-catalog',
  imports: [RouterLink],
  templateUrl: './skills-catalog.html',
  styleUrl: './skills-catalog.scss',
})
export class SkillsCatalog implements OnInit {
  private readonly skillApi = inject(SkillApiService);

  readonly catalog = signal<SkillCatalog | null>(null);
  readonly loading = signal(true);
  readonly error = signal(false);

  ngOnInit(): void {
    this.load();
  }

  retry(): void {
    this.load();
  }

  private load(): void {
    this.loading.set(true);
    this.error.set(false);
    this.skillApi.getCatalog().subscribe({
      next: (catalog) => {
        this.catalog.set(catalog);
        this.loading.set(false);
      },
      error: () => {
        this.error.set(true);
        this.loading.set(false);
      },
    });
  }
}
