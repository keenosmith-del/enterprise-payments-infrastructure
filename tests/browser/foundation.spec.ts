import { test, expect } from '@playwright/test';

for (const port of [5173, 5174, 5175, 5176]) {
  test(`application on ${port} authenticates and reads tenant data`, async ({ page }) => {
    await page.goto(`http://127.0.0.1:${port}/`);
    await expect(page.getByText('Backend readiness: Ready')).toBeVisible();
    await page.getByRole('button', { name: 'Sign in' }).click();
    await page.locator('#username').fill('synthetic-user');
    await page.locator('#password').fill(process.env.EPI_KEYCLOAK_USER_PASSWORD || '');
    await page.locator('#kc-login').click();
    await expect(page.getByText('Signed in')).toBeVisible();
    await expect(page.getByText('Synthetic Entity A')).toBeVisible();
    await expect(page.getByText('Synthetic Entity B')).toHaveCount(0);
    await page.getByRole('button', { name: 'Sign out' }).click();
    await expect(page.getByRole('button', { name: 'Sign in' })).toBeVisible();
  });
}
