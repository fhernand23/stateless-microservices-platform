# syntax=docker/dockerfile:1
#hopeit source:
FROM python:3.9-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ARG ENGINE_VERSION

RUN pip install wheel
RUN pip install hopeit.engine[web,cli,fs-storage,redis-streams,apps-visualizer,config-manager,log-streamer]==$ENGINE_VERSION

#prepare dependencies
FROM python:3.9-slim
COPY --from=0 /opt/venv /opt/venv

RUN apt-get update \
    && apt-get install -y --no-install-recommends make git \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app
ENV PATH=/app:$PATH

COPY Makefile .
COPY requirements.txt requirements.txt
COPY requirements.lock requirements.lock
RUN pip install --upgrade pip
#RUN make hopeit-deps

RUN pip install -r requirements.lock
#prepare app files
COPY app0-admin
COPY plugins plugins
COPY email email
RUN mkdir auth

COPY tools/run-app.sh run-app.sh

# install app
RUN make install

#make final image
FROM python:3.9-slim
COPY --from=1 /opt/venv /opt/venv
COPY --from=1 /app /app

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN mkdir -p /var/log/hopeit

WORKDIR /app
ENV PATH="/app:$PATH"
COPY tools/docker-update-openapi.sh .

ENV REDIS_URL="redis://localhost:6379"
ENV LOGS_PATH="/var/log/hopeit"
ENV MONGO_URL="mongodb://rootuser:rootpass@localhost:27017"
ENV OBJECT_STORAGE_ACCESS_KEY_ID="minio"
ENV OBJECT_STORAGE_SECRET_ACCESS_KEY="minio123"
ENV OBJECT_STORAGE_ENDPOINT_URL="http://minio:9000"

# ENV CORS_ORIGIN="localhost"
ENV DOMAIN="localhost"

ENV CONFIG_FILES="app0-admin/config/server-dev.json,plugins/platform-auth/config/1x0.json,app0-admin/config/app0-admin.json,app0-admin/config/config-manager.json"
# To disable OPEN API set empty value to ENV API_FILE
ENV API_FILE="app0-admin/config/openapi.json"
ENV PORT=8021
# RUN sh docker-update-openapi.sh

EXPOSE $PORT
ENTRYPOINT ["run-app.sh"]
