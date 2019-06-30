FROM nginx:alpine

RUN apk add curl

HEALTHCHECK --interval=10s --timeout=3s \
    CMD curl -f http://localhost || exit 1
