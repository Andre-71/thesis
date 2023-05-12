set -x
docker buildx build --platform linux/amd64 -t muhandre/fogverse:master -f docker-images/master/Dockerfile .