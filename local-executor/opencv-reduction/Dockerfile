FROM muhandre/fogverse:inference-gpu

WORKDIR /app
COPY fogverse/ fogverse/
RUN pip install ultralytics gitpython
COPY local-inferencer/opencv-reduction/main.py .
CMD ["python", "main.py"]
