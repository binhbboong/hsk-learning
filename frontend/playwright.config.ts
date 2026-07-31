import { defineConfig, devices } from '@playwright/test';

const python = process.env['PYTHON'] ?? 'python';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  retries: 0,
  reporter: 'list',
  use: {
    baseURL: 'http://127.0.0.1:4200',
    trace: 'retain-on-failure',
  },
  webServer: [
    {
      command: `"${python}" -m uvicorn app:app --host 127.0.0.1 --port 8010`,
      cwd: '../backend',
      url: 'http://127.0.0.1:8010/api/health',
      reuseExistingServer: true,
      timeout: 60_000,
    },
    {
      command: 'ng serve --proxy-config proxy.e2e.conf.json --host 127.0.0.1 --port 4200',
      url: 'http://127.0.0.1:4200',
      reuseExistingServer: true,
      timeout: 120_000,
    },
  ],
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
