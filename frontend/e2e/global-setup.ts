import { execFileSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const backendDir = fileURLToPath(new URL('../../backend', import.meta.url))
const databasePath = path.resolve(backendDir, 'stock_analyze_e2e.db')

export default function globalSetup() {
  if (path.basename(databasePath) !== 'stock_analyze_e2e.db' || path.dirname(databasePath) !== path.resolve(backendDir)) {
    throw new Error(`Unsafe E2E database path: ${databasePath}`)
  }

  fs.rmSync(databasePath, { force: true })

  const env = {
    ...process.env,
    APP_ENV: 'test',
    DATABASE_URL: `sqlite:///${databasePath.replace(/\\/g, '/')}`,
    GOOGLE_CLIENT_ID: '',
    GOOGLE_CLIENT_SECRET: '',
    GOOGLE_ALLOWED_EMAIL: '',
    OPENAI_API_KEY: '',
  }

  execFileSync('python', ['-m', 'alembic', 'upgrade', 'head'], {
    cwd: backendDir,
    env,
    stdio: 'inherit',
  })
  execFileSync('python', ['seeds/seed_defaults.py'], {
    cwd: backendDir,
    env,
    stdio: 'inherit',
  })
  execFileSync('python', ['tests/e2e/seed_dashboard.py'], {
    cwd: backendDir,
    env,
    stdio: 'inherit',
  })
}
