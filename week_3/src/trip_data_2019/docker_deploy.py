# type: ignore
# pylint: disable=missing-module-docstring
from etl_web_to_gcs import trip_data_2019_etl_parent_flow  # pylint: disable=import-error

from prefect.deployments import Deployment  # pylint: disable=import-error
from prefect.infrastructure.docker import DockerContainer # pylint: disable=import-error, ungrouped-imports
from prefect.filesystems import GitHub  # pylint: disable=import-error

github_block = GitHub.load("github-prefect-flow")
docker_container_block = DockerContainer.load("fhv-tripdata-container-prefect-flow")

docker_dep = Deployment.build_from_flow(
    flow=trip_data_2019_etl_parent_flow,
    name="trip_data_2019-wh-docker-flow",
    version="1",
    description="load data from web and save it to gcs",
    tags=["docker-infra", "github-storage", "web-to-gcs"],
    storage=github_block,
    infrastructure=docker_container_block,
    work_queue_name="default",
    path="",
    entrypoint="week_3/src/trip_data_2019/etl_web_to_gcs.py:trip_data_2019_etl_parent_flow",
    parameters={"months": [12], "year": 2019, "dataset_name": "fhv_tripdata"},
    output="./week_3/src/trip_data_2019/prefect-docker-deployment-web-to-gcs-trip_data2019.yaml",
)


if __name__ == "__main__":
    docker_dep.apply()
