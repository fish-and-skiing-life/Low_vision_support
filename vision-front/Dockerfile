FROM node:12.4.0-alpine

WORKDIR /app


RUN apk update && \
    npm install && \
    npm install -g npm && \
    npm install -g @vue/cli

CMD ["/bin/ash"]
