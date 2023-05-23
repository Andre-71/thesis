docker buildx build \
    --platform linux/amd64 \
    -t muhandre/fogverse:inference-cpu \
    -f base-docker-images/inference-cpu/Dockerfile.cpu \
    --push .
