FROM prefecthq/prefect:2.7.7-python3.9

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

ENV PREFECT_API_URL=http://host.docker.internal:4200/api

RUN prefect config set PREFECT_API_URL="${PREFECT_API_URL}"

RUN mkdir -p /opt/prefect/data/green

RUN mkdir -p /opt/prefect/deployment

COPY deployment /opt/prefect/deployment
