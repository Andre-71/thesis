FROM muhandre/fogverse:inference-gpu

WORKDIR /app
COPY fogverse/ fogverse/
RUN pip install ultralytics gitpython Pillow numpy
COPY local-executor/cam/main.py .
CMD ["python", "main.py"]
