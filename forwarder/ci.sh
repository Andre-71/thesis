set -x
docker buildx build --platform linux/amd64 -t muhandre/fogverse:forwarder -f forwarder/Dockerfile --push .
