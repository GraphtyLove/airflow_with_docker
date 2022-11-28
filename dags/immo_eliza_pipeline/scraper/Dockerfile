FROM selenium/standalone-chrome

USER root

RUN apt update && apt install -y python3 python3-pip


RUN mkdir /app
COPY scraper/* /app
COPY common.py /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]