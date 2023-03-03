FROM --platform=linux/amd64 ubuntu:20.04

RUN apt-get update && apt-get install -y locales \
    && apt-get install -y python3-pip \
    && pip install jupyter \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/* && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN mkdir -p /home/de-zoomcamp

WORKDIR /home/de-zoomcamp

ENV HOME="/home/de-zoomcamp"

RUN mkdir -p ${HOME}/spark && cd ${HOME}/spark \
    && wget https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_linux-x64_bin.tar.gz \
    && tar xzfv openjdk-11.0.1_linux-x64_bin.tar.gz \
    && rm openjdk-11.0.1_linux-x64_bin.tar.gz

ENV JAVA_HOME="${HOME}/spark/jdk-11.0.1"
ENV PATH="${JAVA_HOME}/bin:${PATH}"

RUN cd ${HOME}/spark \
    && wget https://dlcdn.apache.org/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz \
    && tar xzfv spark-3.3.2-bin-hadoop3.tgz \
    && rm spark-3.3.2-bin-hadoop3.tgz

ENV SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
ENV PATH="${SPARK_HOME}/bin:${PATH}"

ENV PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
ENV PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"

RUN mkdir -p ${HOME}/spark/data
RUN mkdir -p ${HOME}/spark/code
