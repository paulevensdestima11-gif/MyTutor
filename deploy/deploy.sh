
#!/bin/bash
set -Eeuo pipefail

# ==========================================
# TutorFlow deployment configuration
# ==========================================

AWS_REGION="eu-central-1"
ECR_REGISTRY="442879245415.dkr.ecr.eu-central-1.amazonaws.com"
ECR_REPOSITORY="tutorflow"

APP_CONTAINER="tutorflow"
CANDIDATE_CONTAINER="tutorflow-candidate"

APP_PORT="8000"
CANDIDATE_PORT="8001"

echo "Starting TutorFlow deployment..."

# ==========================================
# 1. Identify the Docker image
# ==========================================

IMAGE_TAG="${1:?Usage: deploy.sh <image-tag>}"
IMAGE="${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"

echo "Deployment image: ${IMAGE}"

# ==========================================
# 2. Authenticate with Amazon ECR
# ==========================================

aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$ECR_REGISTRY"

# Pull the exact image
docker pull "$IMAGE"

echo "Image successfully pulled."

# ==========================================
# 3. Preserve production configuration
# ==========================================

umask 077
ENV_FILE="$(mktemp)"
trap 'rm -f "$ENV_FILE"' EXIT

docker inspect "$APP_CONTAINER" \
  --format '{{range .Config.Env}}{{println .}}{{end}}' \
  | grep -E '^(SECRET_KEY|DATABASE_SECRET_ARN|AWS_REGION)=' > "$ENV_FILE"

# Verify required environment variables
for variable in SECRET_KEY DATABASE_SECRET_ARN AWS_REGION; do
  if ! grep -q "^${variable}=" "$ENV_FILE"; then
    echo "ERROR: Required configuration ${variable} is missing."
    exit 1
  fi
done

# ==========================================
# 4. Start candidate container
# ==========================================

docker rm -f "$CANDIDATE_CONTAINER" 2>/dev/null || true

docker run --detach \
  --name "$CANDIDATE_CONTAINER" \
  --restart no \
  --publish "127.0.0.1:${CANDIDATE_PORT}:8000" \
  --env-file "$ENV_FILE" \
  "$IMAGE"

echo "Candidate container started."

# ==========================================
# 5. Validate candidate
# ==========================================

CANDIDATE_HEALTHY=false

for attempt in $(seq 1 30); do
  if curl --fail --silent \
    "http://127.0.0.1:${CANDIDATE_PORT}/" > /dev/null; then
    CANDIDATE_HEALTHY=true
    break
  fi

  echo "Waiting for candidate... (${attempt}/30)"
  sleep 2
done

if [ "$CANDIDATE_HEALTHY" != "true" ]; then
  echo "ERROR: Candidate health check failed."
  docker logs "$CANDIDATE_CONTAINER" --tail 50
  docker rm -f "$CANDIDATE_CONTAINER"
  exit 1
fi

echo "Candidate validation successful."

# ==========================================
# 6. Prepare production cutover
# ==========================================

ROLLBACK_CONTAINER="tutorflow-rollback-$(date +%Y%m%d%H%M%S)"

echo "Starting production cutover..."

# Remove candidate to release the application port
docker rm "$CANDIDATE_CONTAINER"

# Stop existing production container
if ! docker stop "$APP_CONTAINER"; then
  echo "ERROR: Could not stop existing production container."
  exit 1
fi

# Rename existing production container for rollback
if ! docker rename "$APP_CONTAINER" "$ROLLBACK_CONTAINER"; then
  echo "ERROR: Could not rename old container. Restarting it..."
  docker start "$APP_CONTAINER"
  exit 1
fi

# ==========================================
# 7. Start new production container
# ==========================================

if ! docker run --detach \
  --name "$APP_CONTAINER" \
  --restart unless-stopped \
  --publish "${APP_PORT}:8000" \
  --env-file "$ENV_FILE" \
  "$IMAGE"; then

  echo "ERROR: New production container failed to start."

  docker rm -f "$APP_CONTAINER" 2>/dev/null || true
  docker rename "$ROLLBACK_CONTAINER" "$APP_CONTAINER"
  docker start "$APP_CONTAINER"

  exit 1
fi

# ==========================================
# 8. Validate production
# ==========================================

HEALTHY=false

for attempt in $(seq 1 30); do
  if curl --fail --silent \
    "http://127.0.0.1:${APP_PORT}/" > /dev/null; then
    HEALTHY=true
    break
  fi

  echo "Waiting for production application... (${attempt}/30)"
  sleep 2
done

# ==========================================
# 9. Automatic rollback if necessary
# ==========================================

if [ "$HEALTHY" != "true" ]; then
  echo "ERROR: Production health check failed. Rolling back..."

  docker logs "$APP_CONTAINER" --tail 50
  docker rm -f "$APP_CONTAINER"
  docker rename "$ROLLBACK_CONTAINER" "$APP_CONTAINER"
  docker start "$APP_CONTAINER"

  exit 1
fi

# ==========================================
# 10. Deployment successful
# ==========================================

echo "Production deployment successful."
echo "Deployed image: $IMAGE"
echo "Rollback container retained: $ROLLBACK_CONTAINER"
