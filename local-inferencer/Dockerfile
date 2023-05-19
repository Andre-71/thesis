FROM muhandre/fogverse:inference-cpu

WORKDIR /app
COPY fogverse/ fogverse/
RUN pip install psutil ultralytics
COPY local-inferencer/main.py .
CMD ["python", "main.py"]
