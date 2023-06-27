FROM muhandre/fogverse:master
WORKDIR /app
COPY fogverse/ fogverse/
RUN pip install Pillow
COPY local-preprocessor/pillow-compression/main.py .
CMD ["python", "main.py"]