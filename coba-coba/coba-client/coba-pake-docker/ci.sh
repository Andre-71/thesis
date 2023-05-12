set -x
docker buildx build \
    --platform linux/amd64 \
    -t muhandre/fogverse:try-client-local \
    -f coba-coba/client-local-without-preprocess-but-with-dockerization/Dockerfile .
