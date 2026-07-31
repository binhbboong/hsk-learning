import { expect, test } from '@playwright/test';


test('learner completes the two-question grammar lesson', async ({ page }) => {
  await page.goto('/skills');
  await expect(page.getByRole('heading', { name: 'Hôm nay bạn muốn luyện gì?' })).toBeVisible();
  await expect(page.locator('[data-testid^="skill-"]')).toHaveCount(4);
  await page.getByTestId('skill-grammar').click();

  await expect(page.getByText('A + 是 + B')).toBeVisible();
  await page.getByTestId('option-a').click();
  await page.getByTestId('check-answer').click();
  await expect(page.getByText('Chính xác')).toBeVisible();
  await page.getByTestId('next-question').click();
  await page.getByTestId('option-b').click();
  await page.getByTestId('check-answer').click();
  await page.getByTestId('next-question').click();

  await expect(page).toHaveURL(/\/skills\/result$/);
  await expect(page.getByText('Hoàn thành bài ngữ pháp')).toBeVisible();
  await expect(page.getByText('2 / 2')).toBeVisible();
});

test('learner reveals transcript and completes listening', async ({ page }) => {
  await page.goto('/skills/listening');
  await expect(page.getByRole('heading', { name: 'Nghe lời chào đầu tiên' })).toBeVisible();
  await expect(page.getByText('Nǐ hǎo, wǒ shì Wáng Míng.')).toBeHidden();
  await page.getByTestId('play-slow').click();
  await page.getByTestId('show-transcript').click();
  await expect(page.getByText('Nǐ hǎo, wǒ shì Wáng Míng.')).toBeVisible();
  await page.getByRole('button', { name: 'Vương Minh' }).click();
  await page.getByTestId('submit-listening').click();

  await expect(page).toHaveURL(/\/skills\/result$/);
  await expect(page.getByText('Hoàn thành bài nghe hiểu')).toBeVisible();
  await expect(page.getByText('1 / 1')).toBeVisible();
});

test('pronunciation remains completable without microphone', async ({ page }) => {
  await page.goto('/skills/pronunciation');
  await expect(page.getByText('nǐ hǎo')).toBeVisible();
  await expect(page.getByText(/Người Việt thường đọc/)).toBeVisible();
  await page.getByTestId('start-recording').click();
  await expect(page.getByText('Microphone không khả dụng.')).toBeVisible();
  await page.getByRole('button', { name: 'Gần đúng' }).click();
  await page.getByTestId('complete-pronunciation').click();

  await expect(page).toHaveURL(/\/skills\/result$/);
  await expect(page.getByText('Hoàn thành bài phát âm')).toBeVisible();
  await expect(page.getByText('2 / 3')).toBeVisible();
});
