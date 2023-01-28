provider "google" {
  project = local.project_id
  region  = local.region
  #   credentials = file(local.credentials) # Use this if you do not want to set env-var GOOGLE_APPLICATION_CREDENTIALS
}
