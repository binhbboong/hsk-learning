import { Component, computed, inject, signal } from '@angular/core';
import { NavigationEnd, Router, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';

import { AuthService } from './core/auth/auth.service';
import { LearningProfileRepository } from './core/services/learning-profile.repository';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  readonly auth = inject(AuthService);
  private readonly profile = inject(LearningProfileRepository);
  private readonly router = inject(Router);
  private readonly currentUrl = signal(this.router.url);
  readonly showHeader = computed(() => !this.currentUrl().startsWith('/auth'));
  readonly accountOpen = signal(false);

  constructor() {
    this.router.events.pipe(
      filter((event): event is NavigationEnd => event instanceof NavigationEnd),
    ).subscribe((event) => {
      this.currentUrl.set(event.urlAfterRedirects);
      this.accountOpen.set(false);
    });
    if (this.auth.isAuthenticated()) {
      this.profile.connectAccount().subscribe({
        error: () => {
          this.auth.clear();
          this.profile.disconnectAccount();
          this.router.navigate(['/auth'], { queryParams: { reason: 'expired' } });
        },
      });
    }
  }

  logout(): void {
    this.auth.logout().subscribe({
      complete: () => {
        this.profile.disconnectAccount();
        this.router.navigate(['/auth']);
      },
      error: () => {
        this.profile.disconnectAccount();
        this.router.navigate(['/auth']);
      },
    });
  }
}
