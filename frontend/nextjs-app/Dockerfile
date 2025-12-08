FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm install

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app

# Build arguments for service URLs
ARG NEXT_PUBLIC_AUTH_SERVICE_URL=http://auth-service.codeforces.svc.cluster.local:80
ARG NEXT_PUBLIC_CONTEST_SERVICE_URL=http://contest-service.codeforces.svc.cluster.local:80
ARG NEXT_PUBLIC_SUBMISSION_SERVICE_URL=http://submission-service.codeforces.svc.cluster.local:80
ARG NEXT_PUBLIC_LEADERBOARD_SERVICE_URL=http://leaderboard-service.codeforces.svc.cluster.local:80

# Make build args available as env vars during build
ENV NEXT_PUBLIC_AUTH_SERVICE_URL=$NEXT_PUBLIC_AUTH_SERVICE_URL
ENV NEXT_PUBLIC_CONTEST_SERVICE_URL=$NEXT_PUBLIC_CONTEST_SERVICE_URL
ENV NEXT_PUBLIC_SUBMISSION_SERVICE_URL=$NEXT_PUBLIC_SUBMISSION_SERVICE_URL
ENV NEXT_PUBLIC_LEADERBOARD_SERVICE_URL=$NEXT_PUBLIC_LEADERBOARD_SERVICE_URL

COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]

