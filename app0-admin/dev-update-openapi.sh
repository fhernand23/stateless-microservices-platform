#!/bin/bash
export REDIS_URL='redis://localhost:6379'
export LOGS_PATH='./logs'
export MONGO_URL="mongodb://rootuser:rootpass@localhost:27017"
export ENV_TYPE="DEV"
export DOMAIN="localhost"
export APP0ADMIN_API_URL="http://localhost:8021"
export APP0CLAIMS_API_URL="http://localhost:8022"
export APP0ADMIN_URL="http://localhost/admin"
export APP0CLAIMS_URL="http://localhost/claims"
export MAIL_APP_FROM="sender@app0.com"
export MAILTO_OVERWRITE="sender@app0.com"
export MAIL_ATTACH_OVERWRITE="./email/test_document.pdf"
export OBJECT_STORAGE_ACCESS_KEY_ID="minio"
export OBJECT_STORAGE_SECRET_ACCESS_KEY="minio123"
export OBJECT_STORAGE_ENDPOINT_URL="http://localhost:9000"
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
export AWS_REGION="some-region"

hopeit_openapi create --title="Claims Platform" --description="Claims Platform" --api-version="1.0" \
--config-files="app0-admin/config/server-dev.json,plugins/platform-auth/config/1x0.json,app0-admin/config/app0-admin.json,app0-admin/config/config-manager.json" \
--output-file="app0-admin/config/openapi.json"
