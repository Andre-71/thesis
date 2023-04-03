set -x
docker buildx build \
    --platform linux/amd64 \
    -t muhandre/fogverse:input \
    -f docker-images/master/Dockerfile \
    --push .
