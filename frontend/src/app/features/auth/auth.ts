import { HttpErrorResponse } from '@angular/common/http';
import { Component, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { AuthService } from '../../core/auth/auth.service';
import { LearningProfileRepository } from '../../core/services/learning-profile.repository';

type AuthMode = 'login' | 'register';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.html',
  styleUrl: './auth.scss',
})
export class Auth {
  private readonly auth = inject(AuthService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);
  private readonly profile = inject(LearningProfileRepository);

  readonly mode = signal<AuthMode>('login');
  readonly displayName = signal('');
  readonly email = signal('');
  readonly password = signal('');
  readonly passwordVisible = signal(false);
  readonly submitting = signal(false);
  readonly submitted = signal(false);
  readonly apiError = signal<string | null>(null);
  readonly isRegister = computed(() => this.mode() === 'register');

  setMode(mode: AuthMode): void {
    this.mode.set(mode);
    this.submitted.set(false);
    this.apiError.set(null);
  }

  submit(): void {
    this.submitted.set(true);
    this.apiError.set(null);
    if (!this.valid()) return;
    this.submitting.set(true);
    const request = this.isRegister()
      ? this.auth.register(this.displayName().trim(), this.email().trim(), this.password())
      : this.auth.login(this.email().trim(), this.password());
    request.subscribe({
      next: () => {
        this.profile.connectAccount().subscribe({
          next: () => this.router.navigateByUrl(
            this.route.snapshot.queryParamMap.get('returnUrl') || '/learn',
          ),
          error: () => this.router.navigateByUrl('/learn'),
        });
      },
      error: (error: HttpErrorResponse) => {
        this.apiError.set(
          error.error?.detail || 'Chưa thể kết nối. Vui lòng thử lại.',
        );
        this.submitting.set(false);
      },
    });
  }

  updateEmail(value: string): void { this.email.set(value); }
  updatePassword(value: string): void { this.password.set(value); }
  updateDisplayName(value: string): void { this.displayName.set(value); }

  emailInvalid(): boolean {
    return !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(this.email().trim());
  }

  private valid(): boolean {
    return (!this.isRegister() || this.displayName().trim().length >= 2)
      && !this.emailInvalid()
      && this.password().length >= 8;
  }
}
