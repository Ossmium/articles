FROM python:3.11.3

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . /usr/src/app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0","--port", "8000", "--reload"]