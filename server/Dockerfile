FROM python:3.8

COPY . app

COPY ./requirements.txt /app/requirements.txt

WORKDIR app

EXPOSE 8000:8000

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["sh", "./run.sh"]