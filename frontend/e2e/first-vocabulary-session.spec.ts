import { expect, test } from '@playwright/test';

test('learner completes five cards and reviews only missed words', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: /Bắt đầu tiếng Trung/i })).toBeVisible();
  await expect(page.getByText('Chào hỏi đầu tiên')).toBeVisible();
  await page.getByTestId('start-lesson').click();

  await expect(page).toHaveURL(/\/lesson$/);
  await expect(page.getByText('5 thẻ')).toBeVisible();
  await expect(page.getByText('Hán-Việt')).toBeVisible();
  await page.getByTestId('start-study').click();

  await expect(page).toHaveURL(/\/study$/);
  for (let index = 1; index <= 5; index += 1) {
    await expect(page.getByText(`${index} / 5`)).toBeVisible();
    await page.getByTestId('reveal').click();
    await expect(page.getByText('Pinyin')).toBeVisible();
    await page
      .getByTestId(index <= 3 ? 'remembered' : 'review')
      .click();
  }

  await expect(page).toHaveURL(/\/results$/);
  await expect(page.getByText('5 thẻ')).toBeVisible();
  await expect(page.getByText('3 đã nhớ')).toBeVisible();
  await expect(page.getByText('2 cần ôn')).toBeVisible();

  await page.getByTestId('review-cards').click();
  await expect(page).toHaveURL(/\/study$/);
  await expect(page.getByText('1 / 2')).toBeVisible();
});
