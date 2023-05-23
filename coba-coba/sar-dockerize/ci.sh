set -x
docker buildx build \
    --platform linux/amd64 \
    --network=host \
    -t muhandre/fogverse:sar \
    -f sar/Dockerfile \
    --push .
