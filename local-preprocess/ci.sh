set -x
docker buildx build --platform linux/amd64 -t muhandre/fogverse:local-preprocess -f local-preprocess/Dockerfile .
