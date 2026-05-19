import { test, expect } from '@playwright/test';

test.describe('Candidate submission flow', () => {
  test('handles success path', async ({ page }) => {
    test.skip(!process.env.PLAYWRIGHT_BASE_URL, 'Set PLAYWRIGHT_BASE_URL for e2e execution.');

    await page.goto('/candidates/new');
    await page.getByLabel('Email').fill('alex@example.com');
    await page.getByLabel('Name').fill('Alex Applicant');
    await page.getByRole('button', { name: 'Submit' }).click();

    await expect(page.getByText('Saved')).toBeVisible();
  });

  test('shows error for invalid form', async ({ page }) => {
    test.skip(!process.env.PLAYWRIGHT_BASE_URL, 'Set PLAYWRIGHT_BASE_URL for e2e execution.');

    await page.goto('/candidates/new');
    await page.getByRole('button', { name: 'Submit' }).click();
    await expect(page.getByRole('alert')).toContainText('valid input');
  });
});
