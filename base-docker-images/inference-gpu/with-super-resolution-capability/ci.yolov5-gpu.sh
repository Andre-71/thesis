docker buildx build --platform linux/amd64 -t muhandre/pytorch:23.04-py3-yolov5-gpu-with-super-resolution-capability -f base-docker-images/inference-gpu/with-super-resolution-capability/Dockerfile.yolov5-gpu .