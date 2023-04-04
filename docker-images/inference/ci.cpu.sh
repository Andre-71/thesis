docker buildx build \
    --platform linux/amd64 \
    -t muhandre/fogverse:inference-cpu \
    -f docker-images/inference/Dockerfile.cpu \
    --push .
