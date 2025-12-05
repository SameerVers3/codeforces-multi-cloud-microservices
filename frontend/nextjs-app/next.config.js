/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001',
    NEXT_PUBLIC_AUTH_SERVICE_URL: process.env.NEXT_PUBLIC_AUTH_SERVICE_URL || 'http://localhost:8001',
    NEXT_PUBLIC_CONTEST_SERVICE_URL: process.env.NEXT_PUBLIC_CONTEST_SERVICE_URL || 'http://localhost:8002',
    NEXT_PUBLIC_SUBMISSION_SERVICE_URL: process.env.NEXT_PUBLIC_SUBMISSION_SERVICE_URL || 'http://localhost:8003',
    NEXT_PUBLIC_LEADERBOARD_SERVICE_URL: process.env.NEXT_PUBLIC_LEADERBOARD_SERVICE_URL || 'http://localhost:8006',
  },
}

module.exports = nextConfig

