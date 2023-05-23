FROM muhandre/fogverse:inference-cpu

WORKDIR /app
RUN git clone --depth=1 --branch=v6.1 https://github.com/ultralytics/yolov5.git \
    && cp -r yolov5/utils/ utils/
COPY fogverse/ fogverse/ 
COPY merger/*.py .
CMD ["python", "main.py"]

