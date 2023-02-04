# type: ignore
# pylint: disable=missing-module-docstring
from pathlib import Path
from datetime import timedelta  # pylint: disable=import-error

import pandas as pd

from prefect import flow, task  # pylint: disable=import-error
from prefect_gcp.cloud_storage import GcsBucket  # pylint: disable=import-error
from prefect.tasks import task_input_hash # pylint: disable=ungrouped-imports, import-error


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""

    df = pd.read_csv(dataset_url)  # pylint: disable=invalid-name
    return df


@task(log_prints=True)
def clean(df: pd.DataFrame) -> pd.DataFrame:  # pylint: disable=invalid-name
    """Fix dtype issues"""
    df["tpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path: # pylint: disable=invalid-name, redefined-outer-name)
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    data_dir = Path(f"data/{color}")
    data_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("gcs-taxi-trip-data")
    gcs_block.upload_from_path(from_path=path, to_path=path)
    return


@flow()
def etl_web_to_gcs(month: int, year: int, color: str) -> None:  # pylint: disable=redefined-outer-name
    """The main ETL function"""

    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"  # pylint: disable=line-too-long

    df = fetch(dataset_url)  # pylint: disable=invalid-name
    df_clean = clean(df)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)


@flow()
def etl_parent_flow(months: list[int], year: int, color: str):  # pylint: disable=redefined-outer-name

    """
    run parametize flow to main etl function
    """

    for month in months:  # pylint: disable=redefined-outer-name
        etl_web_to_gcs(month, year, color)


if __name__ == "__main__":

    color = "green" # pylint: disable=invalid-name
    year = 2019 # 2020 # pylint: disable=invalid-name
    months = [
        4,
    ] # 11

    etl_parent_flow(months, year, color)
