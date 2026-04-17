#!/bin/bash
set -e

echo "=== Pulling the API image ==="
docker image pull datascientest/fastapi:1.0.0

echo "=== Building test images ==="
docker build -t fastapi-test-authentication:1.0.0 -f Dockerfile.authentication .
docker build -t fastapi-test-authorization:1.0.0  -f Dockerfile.authorization  .
docker build -t fastapi-test-content:1.0.0        -f Dockerfile.content        .

echo "=== Running the CI/CD pipeline ==="
docker compose up --abort-on-container-exit

echo "=== Copying logs to log.txt ==="
docker run --rm \
  -v "$(docker compose config --volumes | grep test_logs | awk '{print $2}' 2>/dev/null || echo "$(basename $(pwd))_test_logs")":/logs \
  alpine cat /logs/api_test.log > log.txt 2>/dev/null || \
  docker cp test_content:/logs/api_test.log ./log.txt

echo "=== Logs written to log.txt ==="
cat log.txt

echo "=== Cleaning up ==="
docker compose down --volumes