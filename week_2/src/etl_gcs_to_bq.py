# type: ignore
# pylint: disable=missing-module-docstring
from pathlib import Path
import pandas as pd
from prefect import flow, task  # pylint: disable=import-error
from prefect_gcp.cloud_storage import GcsBucket  # pylint: disable=import-error
from prefect_gcp import GcpCredentials  # pylint: disable=import-error
from prefect.tasks import task_input_hash # pylint: disable=ungrouped-imports, import-error

from datetime import timedelta  # pylint: disable=wrong-import-order


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_from_gcs(month: int, year: int, color: str) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("gcs-taxi-trip-data")
    gcs_block.get_directory(from_path=gcs_path, local_path="./data/")
    return Path(f"./data/{gcs_path}")


@task()
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)  # pylint: disable=invalid-name
    # print(f"pre: missing passenger count: {df['passenger_count'].isna().sum()}")
    # df["passenger_count"].fillna(0, inplace=True)
    # print(f"post: missing passenger count: {df['passenger_count'].isna().sum()}")
    return df


@task()
def write_bq(df: pd.DataFrame) -> None:  # pylint: disable=invalid-name
    """Write DataFrame to BiqQuery"""

    gcp_credentials_block = GcpCredentials.load("prefect-data-eng-zoomcamp-sa")

    df.to_gbq(
        destination_table="taxi_trips_data.rides",
        project_id="winter-campus-375209",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow()
def etl_gcs_to_bq():
    """Main ETL flow to load data into Big Query"""
    color = "yellow"
    year = 2019
    months = [2, 3]

    for month in months:
        path = extract_from_gcs(month, year, color)
        df = transform(path) # pylint: disable=invalid-name
        write_bq(df)


if __name__ == "__main__":
    etl_gcs_to_bq()
