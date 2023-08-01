FROM muhandre/fogverse:master
WORKDIR /app
COPY fogverse/ fogverse/
RUN pip install Pillow
COPY local-preprocessor/main.py .
CMD ["python", "main.py"]