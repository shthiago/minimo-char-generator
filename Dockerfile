FROM python:3.8

LABEL mainteiner="Thiago Sant' Helena <thiago.sant.helena@gmail.com>"

ARG POETRY_VERSION=1.0.3

WORKDIR opt/app

# Copy files
COPY src ./src
COPY Makefile .
COPY poetry.lock .
COPY pyproject.toml .


# Install poetry
RUN pip install "poetry==${POETRY_VERSION}"

RUN poetry export -f requirements.txt > requirements.txt

RUN pip install -r requirements.txt

# Entrypoint settings
COPY scripts/entrypoint.sh ./entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000/tcp
CMD ["run"]

