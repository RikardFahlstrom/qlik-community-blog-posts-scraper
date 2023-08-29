FROM python:3.10-alpine

RUN pip3 install -U pip setuptools wheel
RUN pip3 install datasette datasette-vega

RUN mkdir /app
COPY qlik_posts.db /app
WORKDIR /app
RUN datasette inspect qlik_posts.db

EXPOSE 8001

CMD ["datasette", "serve", "qlik_posts.db", "--port", "8001", "--host", "0.0.0.0", "--config", "sql_time_limit_ms:2500"]
