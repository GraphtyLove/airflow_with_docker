FROM python:3.10

RUN mkdir /app
COPY data_cleaner/* /app
COPY common.py /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]