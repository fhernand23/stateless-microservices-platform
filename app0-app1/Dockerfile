# syntax=docker/dockerfile:1
#hopeit source:
FROM python:3.9-slim

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ARG ENGINE_VERSION

RUN pip install --upgrade pip
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
#RUN make hopeit-deps
RUN make deps-app0-admin

RUN pip install -r requirements.lock
#prepare app files
COPY app0-app1 app0-app1
COPY plugins plugins

COPY tools/run-app.sh run-app.sh

# install app
RUN make 
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
ENV CLAIMSBASE_HOST="http://localhost:8021"
ENV CLAIMSATTENDANT_HOST="http://localhost:8022"
ENV ENV_TYPE="DEV"
ENV CLAIMSBASE_URL="http://localhost/claims"
ENV CLAIMSATTENDANT_URL="http://localhost/app0-app1"
ENV OBJECT_STORAGE_ACCESS_KEY_ID="minio"
ENV OBJECT_STORAGE_SECRET_ACCESS_KEY="minio123"
ENV OBJECT_STORAGE_ENDPOINT_URL="http://minio:9000"
ENV MAPBOX_ACCESS_TOKEN="pk.eyJ1IjoiZmVkZWNsYWltcyIsImEiOiJja3lsbWpybTcyN29vMzFwbHNkeGJpMmNhIn0.xTo7E9ECkfXTyB0D4e0TBA"

# ENV CORS_ORIGIN="localhost"
ENV DOMAIN="localhost"

ENV CONFIG_FILES="app0-app1/config/server-dev.json,plugins/platform-auth/config/1x0.json,app0-app1/config/app0-app1.json,app0-app1/config/config-manager.json"
# To disable OPEN API set empty value to ENV API_FILE
ENV API_FILE="app0-app1/config/openapi.json"
ENV PORT=8022
# RUN sh docker-update-openapi.sh

EXPOSE $PORT
ENTRYPOINT ["run-app.sh"]
