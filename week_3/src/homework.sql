-- Question 1
-- CREATE OR REPLACE EXTERNAL TABLE `winter-campus-375209.taxi_trips_dataset.external_fhv_tripdata`
-- OPTIONS (
--   format = 'PARQUET',
--   uris = ['gs://data_lake_taxi-trip-dataset/data/fhv_tripdata/*.parquet']
--   -- encoding = 'UTF-8'
-- );

-- CREATE OR REPLACE TABLE `winter-campus-375209.taxi_trips_dataset.fhv_tripdata` 
-- OPTIONS (
--   description = "fhv trip dataset"
-- ) AS
-- SELECT  *
--   FROM `winter-campus-375209.taxi_trips_dataset.external_fhv_tripdata`;


-- Question 2 
-- SELECT COUNT(DISTINCT(Affiliated_base_number)) FROM `winter-campus-375209.taxi_trips_dataset.external_fhv_tripdata`

-- SELECT COUNT(DISTINCT(Affiliated_base_number)) FROM `winter-campus-375209.taxi_trips_dataset.fhv_tripdata`

-- Question 3 
-- SELECT COUNT(*)
--   FROM `winter-campus-375209.taxi_trips_dataset.fhv_tripdata`
--  WHERE (PUlocationID IS NULL) AND (DOlocationID IS NULL)

-- Question 4 
-- CREATE OR REPLACE TABLE `winter-campus-375209.taxi_trips_dataset.fhv_tripdata_partitioned_clustered`
-- PARTITION BY DATE(pickup_datetime)
-- CLUSTER BY Affiliated_base_number AS
-- SELECT * FROM `winter-campus-375209.taxi_trips_dataset.fhv_tripdata`;

-- SELECT DISTINCT(Affiliated_base_number)
--   FROM `winter-campus-375209.taxi_trips_dataset.fhv_tripdata`
--  WHERE pickup_datetime BETWEEN '2019-03-01' AND '2019-03-31';

-- SELECT DISTINCT(Affiliated_base_number)
--   FROM `winter-campus-375209.taxi_trips_dataset.fhv_tripdata_partitioned_clustered`
--  WHERE pickup_datetime BETWEEN '2019-03-01' AND '2019-03-31';

