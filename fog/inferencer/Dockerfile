FROM muhandre/fogverse:inference-cpu

WORKDIR /app
RUN pip install psutil
COPY fogverse/ fogverse/
COPY fog/inferencer/main.py .
CMD ["python", "main.py"]
