FROM muhandre/fogverse:inference-gpu-with-super-resolution-capability

WORKDIR /app
COPY fogverse/ fogverse/
RUN pip3 install ultralytics gitpython
RUN pip3 uninstall -y opencv-python
RUN pip3 install opencv-contrib-python
COPY local-inferencer/super-resolution/FSRCNN-small_x2.pb .
COPY local-inferencer/super-resolution/main.py .
CMD ["python", "main.py"]
