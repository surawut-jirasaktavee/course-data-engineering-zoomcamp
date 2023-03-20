# Running Spark and Kafka Clusters with Docker-compose

## Build Required Images for running Spark up

```zsh
cd spark
./build_spark.sh
```

Follow this blogpost to read more details about spark ![Medium blog](https://towardsdatascience.com/apache-spark-cluster-on-docker-ft-a-juyterlab-interface-418383c95445)

## Create network and volume for docker

```zsh
docker network  create kafka-spark-network
docker volume create --name=hadoop-distributed-file-system
```

## Run Services on Docker-compose

```zsh
docker compose up -d
```

## Stop Services on Docker-compose

```zsh
docker compose down
```

Or run below command to remove volume

```zsh
docker compose down -v 
```
