import { Routes } from '@angular/router';
import { Dashboard } from './features/dashboard/dashboard';
import { LessonOverview } from './features/lesson-overview/lesson-overview';
import { Study } from './features/study/study';
import { Results } from './features/results/results';
import { SkillsCatalog } from './features/skills-catalog/skills-catalog';
import { Grammar } from './features/grammar/grammar';
import { Listening } from './features/listening/listening';
import { Pronunciation } from './features/pronunciation/pronunciation';
import { SkillResults } from './features/skill-results/skill-results';
import { LearningHome } from './features/learning-home/learning-home';
import { LessonPlayer } from './features/lesson-player/lesson-player';
import { ReviewCenter } from './features/review-center/review-center';
import { VocabularyNotebook } from './features/vocabulary-notebook/vocabulary-notebook';
import { Checkpoint } from './features/checkpoint/checkpoint';
import { Auth } from './features/auth/auth';
import { authGuard } from './core/auth/auth.guard';
import { adminGuard } from './core/auth/admin.guard';
import { ContentAdmin } from './features/content-admin/content-admin';
import { TopicVocabulary } from './features/topic-vocabulary/topic-vocabulary';
import { PlacementTest } from './features/placement-test/placement-test';
import { LevelExam } from './features/level-exam/level-exam';
import { LearningPreferences } from './features/learning-preferences/learning-preferences';

export const routes: Routes = [
  { path: 'auth', component: Auth, title: 'HSK Learning · Đăng nhập' },
  { path: '', component: Dashboard, title: 'HSK Learning · Bắt đầu học' },
  { path: 'lesson', component: LessonOverview, title: 'HSK Learning · Tổng quan bài học' },
  { path: 'study', component: Study, title: 'HSK Learning · Flip-card' },
  { path: 'results', component: Results, title: 'HSK Learning · Kết quả' },
  { path: 'skills', component: SkillsCatalog, title: 'HSK Learning · Chọn kỹ năng' },
  { path: 'skills/grammar', component: Grammar, title: 'HSK Learning · Ngữ pháp HSK 1' },
  { path: 'skills/listening', component: Listening, title: 'HSK Learning · Nghe hiểu HSK 1' },
  { path: 'skills/pronunciation', component: Pronunciation, title: 'HSK Learning · Phát âm HSK 1' },
  { path: 'skills/result', component: SkillResults, title: 'HSK Learning · Kết quả kỹ năng' },
  { path: 'learn', component: LearningHome, canActivate: [authGuard], title: 'HSK Learning · Tiến độ của bạn' },
  { path: 'learn/lesson/:number', component: LessonPlayer, canActivate: [authGuard], title: 'HSK Learning · Bài học' },
  { path: 'learn/review', component: ReviewCenter, canActivate: [authGuard], title: 'HSK Learning · Trung tâm ôn tập' },
  { path: 'learn/notebook', component: VocabularyNotebook, canActivate: [authGuard], title: 'HSK Learning · Sổ từ cá nhân' },
  { path: 'learn/topics', component: TopicVocabulary, canActivate: [authGuard], title: 'HSK Learning · Từ vựng theo chủ đề' },
  { path: 'learn/placement', component: PlacementTest, canActivate: [authGuard], title: 'HSK Learning · Kiểm tra đầu vào' },
  { path: 'learn/level-exam', component: LevelExam, canActivate: [authGuard], title: 'HSK Learning · Thi tổng kết cấp HSK' },
  { path: 'learn/preferences', component: LearningPreferences, canActivate: [authGuard], title: 'HSK Learning · Mục tiêu học' },
  { path: 'learn/checkpoint', component: Checkpoint, canActivate: [authGuard], title: 'HSK Learning · Kiểm tra Bài 1–5' },
  { path: 'admin/content', component: ContentAdmin, canActivate: [authGuard, adminGuard], title: 'HSK Learning · Quản trị nội dung AI' },
];
