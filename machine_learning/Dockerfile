FROM bitnami/spark:latest

WORKDIR .

USER root
RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER 1001

#CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master"]
