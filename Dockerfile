FROM python:3.9

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

RUN groupadd -r admin && useradd -r -g admin admin

USER admin

ENV RUNNING_ENV=dev

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]