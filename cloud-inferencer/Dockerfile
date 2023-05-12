FROM muhandre/fogverse:inference-cpu

WORKDIR /app
COPY fogverse/ fogverse/
RUN pip install psutil
COPY cloud-inferencer/main.py .
CMD ["python", "main.py"]
