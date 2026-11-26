FROM node:24-alpine@sha256:116b800c3754b440ee0aa3ed2f20f5bf3d99a554bfd9adeea09ea8017f6e85f5 AS build
WORKDIR /app
COPY package.json package-lock.json ./
COPY apps ./apps
COPY packages/ui-components ./packages/ui-components
RUN npm ci
ARG APP_NAME
RUN npm run build --workspace=@epi/$APP_NAME && cp -r apps/$APP_NAME/frontend/dist /frontend
FROM nginxinc/nginx-unprivileged:1.27-alpine@sha256:65e3e85dbaed8ba248841d9d58a899b6197106c23cb0ff1a132b7bfe0547e4c0
COPY infrastructure/docker/frontend.conf.template /etc/nginx/templates/default.conf.template
COPY --from=build /frontend /usr/share/nginx/html
