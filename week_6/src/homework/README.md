# Kafka producer and Kafka consumer application

## Install requirement libraries

```zsh
pip install -r requirements.txt
```

## Datasets

### Download dataset and save it to directory

```zsh
mkdir ../../datasets
cd ../../datasets
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_2019-01.csv.gz
```

## Kafka producer

Navigate to `./src/homework`

### Run fhv taxi producer

```zsh
chmod u+x kafka_ride_producer.py
kafka_ride_producer.py -f "../../datasets/fhv_tripdata_2019-01.csv.gz"
```

### Run green taxi producer

```zsh
chmod u+x kafka_ride_producer.py
kafka_ride_producer.py -f "../../datasets/fhv_tripdata_2019-01.csv.gz"
```

## Kafka consumer

### Run Kafka consumer

```zsh
faust -A consumer worker -l info
```
