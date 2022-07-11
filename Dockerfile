FROM python:3.8.10

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /src

COPY poetry.lock pyproject.toml ./
RUN apt-get -y install --no-install-recommends make=* && \
    pip install poetry==1.1.6 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . ./

ENTRYPOINT ["make"]