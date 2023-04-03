docker buildx build \
    --platform linux/amd64 \
    -t muhandre/pytorch:v1.9-py3.6.9-yolov5-gpu \
    -f docker-images/base-images/Dockerfile.yolov5-gpu \
    --push .
