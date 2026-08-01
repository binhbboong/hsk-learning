import { Component, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { LearningPreferences as Preferences } from '../../core/models/learning-profile';
import { LearningProfileRepository } from '../../core/services/learning-profile.repository';

@Component({ selector: 'app-learning-preferences', imports: [RouterLink], templateUrl: './learning-preferences.html', styleUrl: './learning-preferences.scss' })
export class LearningPreferences {
  private readonly repository = inject(LearningProfileRepository);
  readonly saved = signal(false); readonly error = signal<string | null>(null);
  readonly value = signal<Preferences>(this.repository.profile().learningPreferences ?? { goal: 'communication', dailyMinutes: 20, preferredTopics: [] });
  readonly goals = [['communication', 'Giao tiếp'], ['travel', 'Du lịch'], ['work', 'Công việc'], ['exam', 'Thi HSK'], ['culture', 'Văn hóa']] as const;
  readonly topics = [['food', 'Ăn uống'], ['transport', 'Đi lại'], ['shopping', 'Mua sắm'], ['family', 'Gia đình'], ['workplace', 'Công sở'], ['hobbies', 'Sở thích']] as const;
  setGoal(goal: Preferences['goal']): void { this.value.update(value => ({ ...value, goal })); }
  setMinutes(dailyMinutes: Preferences['dailyMinutes']): void { this.value.update(value => ({ ...value, dailyMinutes })); }
  toggleTopic(topic: Preferences['preferredTopics'][number]): void {
    this.error.set(null); this.value.update(value => {
      if (value.preferredTopics.includes(topic)) return { ...value, preferredTopics: value.preferredTopics.filter(item => item !== topic) };
      if (value.preferredTopics.length === 3) { this.error.set('Bạn có thể chọn tối đa 3 chủ đề.'); return value; }
      return { ...value, preferredTopics: [...value.preferredTopics, topic] };
    });
  }
  save(): void { this.repository.update(profile => ({ ...profile, learningPreferences: this.value() })); this.saved.set(true); }
}
