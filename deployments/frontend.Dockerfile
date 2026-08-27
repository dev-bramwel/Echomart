FROM node:22-alpine AS build

WORKDIR /app
COPY vite-frontend/package*.json ./
RUN npm ci

COPY vite-frontend/ ./
ARG VITE_API_URL=http://localhost:8000/
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:1.27-alpine
COPY deployments/nginx.conf /etc/nginx/nginx.conf
COPY deployments/frontend.nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

USER nginx

EXPOSE 8080
