docker buildx build \
    --platform linux/amd64 \
    -t muhandre/pytorch:v1.10-py3.8.2-cpu \
    -f base-docker-images/inference-cpu/Dockerfile.pytorch-cpu \
    --push .
