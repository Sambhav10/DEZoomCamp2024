FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app

COPY injest-data.py injest-data.py

ENTRYPOINT [ "python", "injest-data.py" ]


