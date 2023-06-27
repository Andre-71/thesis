FROM muhandre/fogverse:inference-gpu

WORKDIR /app
COPY fogverse/ fogverse/
RUN pip install ultralytics gitpython Pillow numpy
COPY local-inferencer/opencv-reduction-pillow-compression/main.py .
CMD ["python", "main.py"]
