FROM node:24-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
COPY apps ./apps
COPY packages/ui-components ./packages/ui-components
RUN npm ci
ARG APP_NAME
RUN npm run build --workspace=@epi/$APP_NAME && cp -r apps/$APP_NAME/frontend/dist /frontend
FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY infrastructure/docker/frontend.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /frontend /usr/share/nginx/html
