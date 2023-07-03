FROM muhandre/fogverse:inference-gpu

WORKDIR /app
COPY fogverse/ fogverse/
RUN pip install ultralytics gitpython
COPY local-inferencer/default/main.py .
CMD ["python", "main.py"]
