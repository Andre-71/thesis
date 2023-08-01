FROM muhandre/fogverse:inference-gpu

WORKDIR /app
COPY fogverse/ fogverse/
RUN pip install ultralytics gitpython Pillow numpy
COPY local-executor/main.py .
CMD ["python", "main.py"]
