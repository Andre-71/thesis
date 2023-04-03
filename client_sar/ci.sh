set -x
docker buildx build \
    --platform linux/amd64 \
    --network=host \
    -t muhandre/fogverse:client_sar \
    -f client_sar/Dockerfile \
    --push .
