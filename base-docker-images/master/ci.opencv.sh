docker buildx build \
    --platform linux/amd64 \
    -t muhandre/opencv:v4.5.5-py3.8.10 \
    -f base-docker-images/master/Dockerfile.opencv \
    --push .
