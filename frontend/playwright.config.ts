import { defineConfig, devices } from '@playwright/test'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const frontendDir = fileURLToPath(new URL('.', import.meta.url))
const backendDir = path.resolve(frontendDir, '../backend')
const databasePath = path.join(backendDir, 'stock_analyze_e2e.db')
const databaseUrl = `sqlite:///${databasePath.replace(/\\/g, '/')}`

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  workers: 1,
  timeout: 30_000,
  expect: {
    timeout: 7_000,
  },
  globalSetup: './e2e/global-setup.ts',
  outputDir: 'test-results',
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
  ],
  use: {
    baseURL: 'http://127.0.0.1:5174',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: [
    {
      command: 'python -m uvicorn app.main:app --host 127.0.0.1 --port 8001',
      cwd: backendDir,
      url: 'http://127.0.0.1:8001/health',
      reuseExistingServer: false,
      timeout: 30_000,
      env: {
        ...process.env,
        APP_ENV: 'test',
        DATABASE_URL: databaseUrl,
        ALLOWED_ORIGIN: 'http://127.0.0.1:5174',
        ALLOWED_ORIGINS: 'http://127.0.0.1:5174',
        GOOGLE_CLIENT_ID: '',
        GOOGLE_CLIENT_SECRET: '',
        GOOGLE_ALLOWED_EMAIL: '',
        OPENAI_API_KEY: '',
      },
    },
    {
      command: 'npm run dev -- --host 127.0.0.1 --port 5174',
      cwd: frontendDir,
      url: 'http://127.0.0.1:5174/login',
      reuseExistingServer: false,
      timeout: 30_000,
      env: {
        ...process.env,
        VITE_API_BASE_URL: 'http://127.0.0.1:8001',
      },
    },
  ],
})
