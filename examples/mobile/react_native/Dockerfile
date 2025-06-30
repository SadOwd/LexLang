# syntax=docker/dockerfile:1
ARG NODE_VERSION=22.13.1

# Build stage
FROM node:${NODE_VERSION}-slim AS builder
WORKDIR /app

# Copy only package.json for dependency install
COPY --link package.json ./
# If you have a package-lock.json, uncomment the next line
# COPY --link package-lock.json ./

# Install dependencies with cache and bind mounts for deterministic builds
RUN --mount=type=cache,target=/root/.npm \
    npm ci

# Copy the rest of the application source
COPY --link . .

# If you have a build step (e.g., for TypeScript or React Native bundling), uncomment:
# RUN npm run build

# Remove dev dependencies for production
RUN --mount=type=cache,target=/root/.npm \
    npm prune --production

# Production stage
FROM node:${NODE_VERSION}-slim AS final
WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy only necessary files from builder
COPY --from=builder /app /app

ENV NODE_ENV=production
ENV NODE_OPTIONS="--max-old-space-size=4096"
USER appuser

# Expose port if your app listens on one (e.g., 8081 for Metro bundler)
# EXPOSE 8081

CMD ["npm", "start"]
