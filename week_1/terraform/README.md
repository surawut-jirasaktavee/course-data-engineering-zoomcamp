# Terraform GCP

## Setup environment variable that navigate to service account key of GCP

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/Users/premsurawut/Github/Data-Engineer/course-data-engineering-zoomcamp/keys/terraform-sa.json

echo $GOOGLE_APPLICATION_CREDENTIALS

gcloud auth application-default login
```
