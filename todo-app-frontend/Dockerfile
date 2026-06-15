# === ЭТАП 1: Разработка (Dev) ===
FROM node:18-alpine AS development
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
# Эта команда по умолчанию, её переопределит docker-compose.override.yml
CMD ["npm", "start"]

# === ЭТАП 2: Сборка (Builder) ===
FROM development AS builder
RUN npm run build

# === ЭТАП 3: Продакшен (Prod) ===
FROM nginx:alpine AS production
COPY --from=builder /app/build /usr/share/nginx/html
RUN echo "server { listen 80; location / { root /usr/share/nginx/html; index index.html index.htm; try_files \$uri \$uri/ /index.html; } }" > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]