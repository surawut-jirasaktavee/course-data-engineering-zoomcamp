locals {
  common_tags = merge(jsondecode(file("${path.module}/common_tags.json")),
    {
      environment = terraform.workspace
    }
  )
  project_id   = "winter-campus-375209"
  region       = "asia-southeast1"
  prefix       = "data_lake"
  bucket_name  = "taxi-trip-dataset"
  project_name = "data-engineering-zoomcamp"
  #   credentials      = file("${path.module}/../../keys/terraform-sa.json")
}

# variable "project" {
#   description = "Your GCP Project ID"
# }

# variable "region" {
#   description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
#   default     = "asia-southeast1"
#   type        = string
# }

variable "storage_class" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type        = string
  default     = "taxi_trips_dataset"
}
