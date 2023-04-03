set -x
docker buildx build \
    --platform linux/amd64 \
    -t muhandre/fogverse:inference-gpu-jetson \
    -f fog/jetson_nano/Dockerfile \
    --push .
