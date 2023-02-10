# type: ignore
# pylint: disable=missing-module-docstring
from prefect.infrastructure.docker import DockerContainer # pylint: disable=import-error

# alternative to creating DockerContainer block in the UI
docker_block = DockerContainer(
    image="premdocker2022/prefect-flow:fhv_tripdata_v1",  # insert your image here
    image_pull_policy="ALWAYS",
    auto_remove=True,
    # network_mode="bridge",
)

docker_block.save("fhv-tripdata-container-prefect-flow", overwrite=True)
