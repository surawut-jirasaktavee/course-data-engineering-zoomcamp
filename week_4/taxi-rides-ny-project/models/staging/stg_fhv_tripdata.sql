{{ config(materialized='view') }}

-- with fhv_tripdata as 
-- (
--   select *,
--     row_number() over(partition by cast(dispatching_base_num as integer), pickup_datetime) as rn
--   from {{ source('staging','external_fhv_tripdata') }}
--   where vendorid is not null 
-- )
select
    -- identifiers
    {{ dbt_utils.surrogate_key(['dispatching_base_num', 'pickup_datetime']) }} as tripid,
    dispatching_base_num,
    cast(pulocationid as integer) as  pickup_locationid,
    cast(dolocationid as integer) as dropoff_locationid,
    
    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,
    
    -- trip info
    sr_flag,
    Affiliated_base_number
from {{ source('staging','external_fhv_tripdata') }}
where dispatching_base_num is not null
-- from fhv_tripdata
-- where rn = 1


-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=false) %}

  limit 100

{% endif %}