# base
FROM python:3.9-buster AS base

RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y openjdk-11-jre-headless

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY . .

# production
FROM python:3.9-slim-buster AS main

RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y \
    iproute2 make coreutils procps sudo openjdk-11-jre-headless python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=base /app/src /app/src
COPY --from=base /app/entrypoint.py /app/
COPY --from=base /app/Makefile /app/
COPY --from=base /app/README.md /app/
COPY --from=base /app/poetry.lock /app/
COPY --from=base /app/pyproject.toml /app/
COPY --from=base /usr/bin/make /app/make

RUN ./make install
RUN pip install tensorflow

# Make port 5000 available to the world outside this container
EXPOSE 5000

CMD ["make", "run-api"]
