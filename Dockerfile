FROM puckel/docker-airflow:1.9.0-3

USER root

RUN apt-get update \
 && apt-get install jq default-jdk
 && apt-get clean

USER airflow
