# type: ignore
# pylint: disable=missing-module-docstring
from etl_web_to_gcs_parametize_4 import etl_parent_flow  # pylint: disable=import-error

from prefect.deployments import Deployment  # pylint: disable=import-error
from prefect.infrastructure.docker import DockerContainer # pylint: disable=import-error, ungrouped-imports
from prefect.filesystems import GitHub  # pylint: disable=import-error

github_block = GitHub.load("github-prefect-flow")
docker_container_block = DockerContainer.load("container-prefect-flow")

docker_dep = Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="docker-flow",
    version="1",
    description="load data from web and save it to gcs",
    tags=["docker-infra", "github-storage", "web-to-gcs"],
    storage=github_block,
    infrastructure=docker_container_block,
    work_queue_name="default",
    path="",
    entrypoint="week_2/src/deployment/etl_web_to_gcs_parametize_4.py:etl_parent_flow",
    parameters={"months": [11], "year": 2022, "color": "green"},
    output="./week_2/src/deployment/prefect-docker-deployment-web-to-gcs-green.yaml",
)


if __name__ == "__main__":
    docker_dep.apply()
