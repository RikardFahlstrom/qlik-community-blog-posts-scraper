FROM python:3.7-alpine

RUN pip3 install -U pip setuptools wheel
RUN pip3 install datasette datasette-vega

RUN mkdir /app
COPY qlik_posts.db /app
WORKDIR /app

EXPOSE 8001

CMD ["datasette", "qlik_posts.db"]
