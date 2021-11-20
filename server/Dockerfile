FROM python:3.8

COPY . app

COPY ./requirements.txt /app/requirements.txt

WORKDIR app

EXPOSE 8000:8000

RUN pip install -r requirements.txt

CMD ["sh", "./run.sh"]