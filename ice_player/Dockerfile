FROM python:3.13-alpine3.22 AS venv_builder

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install virtualenv && python -m venv /venv
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc g++ libc-dev python3-dev zlib-dev
RUN /venv/bin/pip install -r /tmp/requirements.txt


FROM python:3.13-alpine3.22

RUN mkdir /app
WORKDIR /app

COPY --from=venv_builder /venv /venv
RUN ln -fs $(which python) /venv/bin/python

COPY player.py /app/player.py
CMD ["python", "player.py"]
