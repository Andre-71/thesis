mkdir docker-images
mkdir docker-images/base-images
touch docker-images/base-images/ci.pytorch-cpu.sh
touch docker-images/base-images/ci.yolov5-cpu
touch docker-images/base-images/Dockerfile.pytorch-cpu
touch docker-images/base-images/Dockerfile.yolov5-cpu
chmod +x docker-images/base-images/ci.pytorch-cpu.sh
chmod +x docker-images/base-images/ci.yolov5-cpu
chmod +x docker-images/base-images/Dockerfile.pytorch-cpu
chmod +x docker-images/base-images/Dockerfile.yolov5-cpu
mkdir docker-images/inference
touch docker-images/inference/ci.cpu.sh
touch docker-images/inference/Dockerfile.cpu
chmod +x docker-images/inference/ci.cpu.sh
chmod +x docker-images/inference/Dockerfile.cpu