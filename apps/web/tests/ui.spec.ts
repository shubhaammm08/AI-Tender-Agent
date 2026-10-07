import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await expect(page).toHaveTitle(/AI Tender Agent/);
});

test('tenders view renders correctly', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await expect(page.locator('text=Good morning')).toBeVisible();
  await expect(page.locator('text=4 new tenders match your business today')).toBeVisible();
});

test('navigation works', async ({ page }) => {
  await page.goto('http://localhost:3000/');
  await page.click('text=Document vault');
  await expect(page.locator('text=Upload each document once')).toBeVisible();
  
  await page.click('text=My bids');
  await expect(page.locator('text=Every bid waits for your approval')).toBeVisible();
});
