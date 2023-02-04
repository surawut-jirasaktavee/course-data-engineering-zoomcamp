```bash
prefect deployment build week_2/src/deployment/etl_web_to_gcs.py:etl_web_to_gcs \
--name docker-flow \
--version v1 \
--tag "docker-infra, github-storage, web-to-gcs" \
--work-queue default \
--storage-block github/github-prefect-flow \
--infra-block docker-container/container-prefect-flow \
--output prefect-docker-deployment \
--apply
```
