# type: ignore
# pylint: disable=missing-module-docstring
from etl_web_to_gcs import etl_web_to_gcs  # pylint: disable=import-error

from prefect.deployments import Deployment  # pylint: disable=import-error
from prefect.infrastructure.docker import DockerContainer # pylint: disable=import-error, ungrouped-imports
from prefect.filesystems import GitHub  # pylint: disable=import-error

github_block = GitHub.load("github-prefect-flow")
docker_container_block = DockerContainer.load("container-prefect-flow")

docker_dep = Deployment.build_from_flow(
    flow=etl_web_to_gcs,
    name="docker-flow",
    description="load data from web and save it to gcs",
    version="1",
    infrastructure=docker_container_block,
    storage=github_block,
    work_queue_name="default",
    path="",
    entrypoint="week_2/src/flows/etl_web_to_gcs.py:etl_web_to_gcs",
    tags=["docker-infra", "github-storage", "web-to-gcs"],
)


if __name__ == "__main__":
    docker_dep.apply()
