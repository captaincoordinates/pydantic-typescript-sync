FROM python:3.8-slim

RUN python -m pip install --upgrade pip
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update --fix-missing \
    && apt-get install --no-install-recommends -y \
    curl \
    jq \
    && apt-get clean

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

RUN npm install -g json-schema-to-typescript@^10.1.5

COPY entrypoint.sh /

WORKDIR /tsgen
COPY src/ .

RUN mkdir /input
RUN mkdir /output

ENV INPUT_BASE_DIR=/input
ENV OUTPUT_DIR=/output

ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "sh", "-c", "python -m generation.watch ${INPUT_BASE_DIR} ${OUTPUT_DIR}" ]
