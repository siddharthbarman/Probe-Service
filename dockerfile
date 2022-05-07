FROM python:3.8-slim-buster
LABEL org.opencontainers.image.authors="Siddharth B <sbytestream@outlook.com>"
WORKDIR /opt/probesvc
COPY cmdline.py .
COPY probesvc.py .
COPY requirements.txt .
RUN apt-get -y update
RUN apt install curl -y
RUN apt install procps -y
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["python3", "./probesvc.py"]
