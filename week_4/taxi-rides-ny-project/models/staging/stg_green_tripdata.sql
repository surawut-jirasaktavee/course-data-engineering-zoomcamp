{{ config(materialized='table') }}

select * from {{ source("staging", "external_green_tripdata") }}
limit 100