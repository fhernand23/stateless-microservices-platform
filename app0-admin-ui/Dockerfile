FROM node:16 as build-stage
# RUN apk --no-cache add --virtual native-deps \
#     g++ gcc libgcc libstdc++ linux-headers make python autoconf automake

ADD package.json /tmp/package.json
ADD package-lock.json /tmp/package-lock.json

# ADD yarn.lock /tmp/yarm.lock
# RUN CYPRESS_INSTALL_BINARY=0 cd /tmp && yarn --frozen-lockfile --network-timeout 100000
RUN npm install -g npm@latest
RUN CYPRESS_INSTALL_BINARY=0 cd /tmp && npm install --legacy-peer-deps
RUN mkdir -p /app && cp -a /tmp/node_modules /app/

WORKDIR /app
COPY . .
RUN SILENT=0 npm run build


# production stage
FROM nginx:mainline-alpine as production-stage
# Copy the respective nginx configuration files
COPY --from=build-stage /app/dist /app
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


# FROM bitnami/nginx:1.19 AS prod
# WORKDIR /app

# COPY --from=build /app/dist .
# COPY ./nginx/vuejs.conf /opt/bitnami/nginx/conf/server_blocks/nginx.conf
