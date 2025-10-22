# --- Stage 1: Build the Vite app ---
FROM node:18-alpine AS build
WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all source code
COPY . .

# Fix permissions for Vite binary
RUN chmod +x ./node_modules/.bin/vite

# Build production files (output goes to /app/dist)
RUN npx vite build

# --- Stage 2: Serve with NGINX ---
FROM nginx:stable-alpine

# Copy built static files to NGINX's html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Add custom NGINX config (optional for SPA routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
