FROM nginx:1.23.3-alpine-slim as prod

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

FROM prod as dev

COPY nginx.conf.dev /etc/nginx/conf.d/nginx.conf