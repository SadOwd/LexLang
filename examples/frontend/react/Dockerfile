# syntax=docker/dockerfile:1
ARG NODE_VERSION=22.13.1

# Build stage
FROM node:${NODE_VERSION}-slim AS builder
WORKDIR /app

# Install dependencies (npm ci expects package-lock.json, but it's not present, so fallback to npm install)
COPY --link package.json ./
# If you have a package-lock.json, uncomment the next line:
# COPY --link package-lock.json ./

RUN --mount=type=cache,target=/root/.npm \
    npm install

# Copy the rest of the application source
COPY --link . .

# Build the app (if you have a build step, e.g., for React)
RUN --mount=type=cache,target=/root/.npm \
    npm run build || echo "No build script, skipping."

# Production stage
FROM node:${NODE_VERSION}-slim AS final
WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy built app and dependencies from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
# If you have a package-lock.json, uncomment the next line:
# COPY --from=builder /app/package-lock.json ./
COPY --from=builder /app/build ./build
COPY --from=builder /app/public ./public

ENV NODE_ENV=production
ENV NODE_OPTIONS="--max-old-space-size=4096"
USER appuser

# If you use serve or similar to serve the build, adjust the CMD accordingly
CMD ["npx", "serve", "-s", "build"]
