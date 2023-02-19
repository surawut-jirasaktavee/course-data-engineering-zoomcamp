FROM prefecthq/prefect:2.7.7-python3.9

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir

ENV PREFECT_API_URL=http://host.docker.internal:4200/api

RUN prefect config set PREFECT_API_URL="${PREFECT_API_URL}"

RUN mkdir -p /opt/prefect/data
RUN mkdir -p /opt/prefect/data/trip_data_all
RUN mkdir -p /opt/prefect/trip_data_all

COPY etl_trip_data/etl_web_to_gcs.py /opt/prefect/trip_data_all/
COPY etl_trip_data/config.py /opt/prefect/trip_data_all/