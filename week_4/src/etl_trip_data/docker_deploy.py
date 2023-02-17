# type: ignore
# pylint: disable=missing-module-docstring
from etl_web_to_gcs import trip_data_etl_parent_flow  # pylint: disable=import-error

from prefect.deployments import Deployment  # pylint: disable=import-error
from prefect.infrastructure.docker import DockerContainer # pylint: disable=import-error, ungrouped-imports
from prefect.filesystems import GitHub  # pylint: disable=import-error

github_block = GitHub.load("github-prefect-flow")
docker_container_block = DockerContainer.load("tripdata-all-container-prefect-flow")

docker_dep = Deployment.build_from_flow(
    flow=trip_data_etl_parent_flow,
    name="trip_data-wh-docker-flow",
    version="1",
    description="load data from web and save it to gcs",
    tags=["docker-infra", "github-storage", "web-to-gcs"],
    storage=github_block,
    infrastructure=docker_container_block,
    work_queue_name="default",
    path="",
    entrypoint="week_4/src/etl_trip_data/etl_web_to_gcs.py:trip_data_etl_parent_flow",
    parameters={
        "months": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
        ],
        "years": [2019, 2020],
        "colors": ["yellow", "green"]
    },
    output="./prefect-docker-deployment-web-to-gcs-trip_data.yaml",
)


if __name__ == "__main__":
    docker_dep.apply()
