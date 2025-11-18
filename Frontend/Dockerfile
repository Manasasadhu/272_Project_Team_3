# Multi-stage build for React frontend
FROM node:20-alpine AS builder

WORKDIR /app

# Clone the latest code from feat/end-to-end-testing branch
RUN apk add --no-cache git && \
    git clone --branch feat/end-to-end-testing --depth 1 https://github.com/Manasasadhu/272_Project_Team_3.git /tmp/repo && \
    cp -r /tmp/repo/Frontend/* /app/ && \
    rm -rf /tmp/repo

# Install dependencies
RUN npm ci

# Build the app
RUN npm run build

# Production stage - serve with nginx
FROM nginx:alpine

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
