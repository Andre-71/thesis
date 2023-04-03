docker buildx build \
    --platform linux/amd64 \
    -t ${DREG}muhandre/fogverse:inference-gpu \
    -f docker-images/inference/Dockerfile.gpu \
    --push .
