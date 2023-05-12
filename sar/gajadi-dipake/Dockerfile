FROM muhandre/fogverse:input

RUN pip install --upgrade djitellopy

WORKDIR /app

COPY fogverse/ fogverse/

COPY sar/main.py .

CMD ["python", "main.py"]
