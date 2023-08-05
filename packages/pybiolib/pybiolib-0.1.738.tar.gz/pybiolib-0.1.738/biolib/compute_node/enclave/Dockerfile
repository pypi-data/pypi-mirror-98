FROM ubuntu:latest
RUN apt update -y  
RUN apt install docker.io haveged bash strace python3.8 python3-pip -y

WORKDIR /app

COPY ./ ./
RUN pip3 install -r requirements.txt
RUN chmod +x run.sh

CMD ["/app/run.sh"]

