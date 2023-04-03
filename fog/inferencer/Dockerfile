FROM muhandre/fogverse:inference-gpu

WORKDIR /app
COPY fog/inferencer/main.py .
COPY fogverse/ fogverse/
CMD ["python3", "main.py"]
