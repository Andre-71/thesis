set -x
docker buildx build --platform linux/amd64 -t muhandre/fogverse:cloud-inferencer -f cloud-inferencer/Dockerfile .
