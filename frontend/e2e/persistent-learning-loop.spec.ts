import { expect, test } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  const email = `learner-${Date.now()}-${Math.random()}@example.com`;
  await page.goto('/auth');
  await page.getByRole('button', { name: 'Đăng ký', exact: true }).click();
  await page.getByLabel('Tên của bạn').fill('Người học thử');
  await page.getByLabel('Email').fill(email);
  await page.getByLabel('Mật khẩu').fill('matkhau123');
  await page.getByTestId('submit-auth').click();
  await page.waitForURL(/\/learn$/);
  await page.goto('/learn');
});

test('lesson controls, notebook and progress persist after reload', async ({ page }) => {
  await expect(page.getByText('0 / 5 bài')).toBeVisible();
  await page.getByTestId('next-action').click();

  await expect(page).toHaveURL(/\/learn\/lesson\/1$/);
  await expect(page.getByRole('button', { name: /Pinyin Bật/ })).toBeVisible();
  await page.getByTestId('toggle-pinyin').click();
  await expect(page.getByRole('button', { name: /Pinyin Tắt/ })).toBeVisible();
  await page.locator('.lesson-words button').first().click();
  await page.getByRole('button', { name: /Phát âm/ }).click();
  await page.getByTestId('complete-multi-lesson').click();

  await expect(page).toHaveURL(/\/learn$/);
  await expect(page.getByText('1 / 5 bài')).toBeVisible();
  await expect(page.getByText('1 từ đã lưu')).toBeVisible();
  await page.reload();
  await expect(page.getByText('1 / 5 bài')).toBeVisible();
  await page.getByTestId('open-notebook').click();
  await expect(page.locator('.word-list article')).toHaveCount(1);
});

test('two accounts keep separate learning progress', async ({ page }) => {
  await page.getByTestId('next-action').click();
  await page.getByRole('button', { name: /Phát âm/ }).click();
  await page.getByTestId('complete-multi-lesson').click();
  await expect(page.getByText('1 / 5 bài')).toBeVisible();

  await page.getByTestId('account-menu').click();
  await page.getByTestId('logout').click();
  await page.waitForURL(/\/auth$/);
  await page.getByRole('button', { name: 'Đăng ký', exact: true }).click();
  await page.getByLabel('Tên của bạn').fill('Người học thứ hai');
  await page.getByLabel('Email').fill(`second-${Date.now()}@example.com`);
  await page.getByLabel('Mật khẩu').fill('matkhau123');
  await page.getByTestId('submit-auth').click();

  await page.waitForURL(/\/learn$/);
  await expect(page.getByText('0 / 5 bài')).toBeVisible();
  await expect(page.getByText('Người học thứ hai')).toBeVisible();
});

test('checkpoint unlocks after five lessons and stores wrong answers', async ({ page }) => {
  await page.evaluate(() => {
    localStorage.setItem('hsk-learning.profile.v1', JSON.stringify({
      version: 1,
      completedLessonIds: [1, 2, 3, 4, 5].map((number) => `hsk1-lesson-${number}`),
      streak: { current: 5, longest: 5, lastActiveDate: '2026-07-30' },
      reviewCards: [],
      mistakes: [],
      notebook: [],
      checkpointResults: [],
    }));
  });
  await page.reload();
  await expect(page.getByTestId('next-action')).toHaveAttribute('href', '/learn/checkpoint');
  await page.getByTestId('next-action').click();
  await expect(page.getByText('Câu 1 / 3')).toBeVisible();

  await page.locator('.option-list button').last().click();
  await page.getByRole('button', { name: 'Xác nhận đáp án' }).click();
  await expect(page.getByText('Câu 2 / 3')).toBeVisible();
  await page.goto('/learn/review?source=mistakes');
  await page.getByRole('button', { name: /Câu làm sai/ }).click();
  await expect(page.locator('.review-card')).toBeVisible();
});
