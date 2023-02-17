# type: ignore
# pylint: disable=missing-module-docstring
from pathlib import Path
from datetime import timedelta  # pylint: disable=import-error

import pandas as pd

from prefect import flow, task  # pylint: disable=import-error
from prefect_gcp.cloud_storage import GcsBucket  # pylint: disable=import-error
# from prefect.tasks import task_input_hash # pylint: disable=ungrouped-imports, import-error


@task(retries=3) #, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""

    try:
        print(f"Start download file from the given url: {dataset_url}")
        df = pd.read_csv(dataset_url)  # pylint: disable=invalid-name
        return df
    except Exception as e: # pylint: disable=invalid-name
        print(f"something went wrong with: {e}") # pylint: disable=invalid-name


@task(log_prints=True)
def clean(df: pd.DataFrame, color: str) -> pd.DataFrame:  # pylint: disable=invalid-name, redefined-outer-name
    """Fix dtype issues"""

    if color == "green":
        df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
        df["lpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
        return df
    elif color == "yellow":
        df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
        df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
        return df
    
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    


@task()
def write_local(
    df: pd.DataFrame, dataset_name: str, dataset_file: str) -> Path:  # pylint: disable=invalid-name, redefined-outer-name)
    """Write DataFrame out locally as parquet file"""
    path = Path(f"data/{dataset_name}/{dataset_file}.parquet")
    data_dir = Path(f"data/{dataset_name}")
    data_dir.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload local parquet file to GCS"""
    gcs_block = GcsBucket.load("gcs-taxi-trip-data", validate=False)
    gcs_block.upload_from_path(from_path=path, to_path=path, timeout=10000)
    return


@flow()
def etl_web_to_gcs(month: int, year: int, color: str) -> None:  # pylint: disable=redefined-outer-name
    """The main ETL function"""

    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/{dataset_file}.csv.gz"  # pylint: disable=line-too-long
    
    # https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz
    # https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz
    
    df = fetch(dataset_url)  # pylint: disable=invalid-name
    df_clean = clean(df, color)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)


@flow()
def send_message():

    """
    Send message when the flow and sub task is complete
    """

    from prefect_slack import SlackWebhook  # pylint: disable=import-error, import-outside-toplevel
    from prefect_slack.messages import send_incoming_webhook_message # pylint: disable=import-error, import-outside-toplevel

    slack_webhook_block = SlackWebhook.load("slack-prefect-webhook-block")
    send_incoming_webhook_message(
        slack_webhook=slack_webhook_block,
        text="Complete to download data from web and store in Google Cloud Storage",
    )


@flow()
def trip_data_etl_parent_flow(months: list[int], years: list[int], colors: list[str]):  # pylint: disable=redefined-outer-name

    """
    run parametize flow to main etl function
    """
    try:
        for color in colors: # pylint: disable=redefined-outer-name
            for year in years: # pylint: disable=redefined-outer-name
                for month in months:  # pylint: disable=redefined-outer-name
                    etl_web_to_gcs(month, year, color)
                send_message()
    except: # pylint: disable=bare-except
        print("Flow is not complete...")


if __name__ == "__main__":

    colors = ["yellow", "green"]  # pylint: disable=invalid-name
    years = [2019, 2020]  # pylint: disable=invalid-name
    months = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    ] # pylint: disable=invalid-name
 
    trip_data_etl_parent_flow(months, years, colors)
