#!/bin/bash
export REDIS_URL='redis://localhost:6379'
export LOGS_PATH='../logs'
export MONGO_URL="mongodb://rootuser:rootpass@localhost:27017"
export ENV_TYPE="DEV"
export DOMAIN="localhost"
export APP0_ADMIN_API_URL="http://localhost:8021"
export APP0_APP1_API_URL="http://localhost:8022"
export APP0_ADMIN_URL="http://localhost/admin"
export APP0_APP1_URL="http://localhost/app1"
export MAIL_APP_FROM="sender@app0.com"
export OBJECT_STORAGE_ACCESS_KEY_ID="minio"
export OBJECT_STORAGE_SECRET_ACCESS_KEY="minio123"
export OBJECT_STORAGE_ENDPOINT_URL="http://localhost:9000"
export DOMAIN="localhost"

hopeit_openapi create --title="App0 Platform" --description="App0 Platform" --api-version="1.0" \
--config-files="app0-admin/config/server-dev.json,plugins/platform-auth/config/1x0.json,app0-admin/config/app0-admin.json,app0-admin/config/config-manager.json" \
--output-file="app0-admin/config/openapi.json"
