docker buildx build --platform linux/amd64 -t muhandre/pytorch:23.04-py3-yolov5-gpu -f base-docker-images/inference-gpu/Dockerfile.yolov5-gpu .