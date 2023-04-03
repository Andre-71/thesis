docker buildx build \
    --platform linux/amd64 \
    -t muhandre/opencv:v4.5.5-py3.8.10 \
    -f docker-images/base-images/Dockerfile.opencv \
    --push .
