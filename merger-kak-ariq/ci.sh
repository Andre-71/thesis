set -x
docker buildx build --platform linux/amd64 -t muhandre/fogverse:merger-kak-ariq -f merger-kak-ariq/Dockerfile --no-cache .
