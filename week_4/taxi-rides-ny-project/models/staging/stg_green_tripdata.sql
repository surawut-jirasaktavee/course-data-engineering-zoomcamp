{{ config(materialized='table') }}

select * from {{ source("staging", "green_tripdata") }}
limit 100