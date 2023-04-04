FROM muhandre/fogverse:inference-cpu

WORKDIR /app
COPY fog/inferencer/main.py .
COPY fogverse/ fogverse/
CMD ["python", "main.py"]
