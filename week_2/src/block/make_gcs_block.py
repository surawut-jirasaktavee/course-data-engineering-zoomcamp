# type: ignore
# pylint: disable=missing-module-docstring

from prefect_gcp import GcpCredentials  # pylint: disable=import-error
from prefect_gcp.cloud_storage import GcsBucket  # pylint: disable=import-error

# alternative to creating GCP blocks in the UI
# insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!


credentials_block = GcpCredentials(
    service_account_info={}  # enter your credentials info or use the file method.
)
credentials_block.save("prefect-data-eng-zoomcamp-sa", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("prefect-data-eng-zoomcamp-sa"),
    bucket="data_lake_taxi-trip-dataset",  # insert your  GCS bucket name
)

bucket_block.save("gcs-taxi-trip-data", overwrite=True)
