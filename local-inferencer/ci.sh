set -x
docker buildx build --platform linux/amd64 -t muhandre/fogverse:local-inferencer -f local-inferencer/Dockerfile .