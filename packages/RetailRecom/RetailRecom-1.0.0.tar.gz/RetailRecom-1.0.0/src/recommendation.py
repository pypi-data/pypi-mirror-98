import pyspark
from pyspark.sql import SparkSession
import os
from elasticsearch import Elasticsearch
from pyspark.sql import functions as sf
from pyspark.ml.recommendation import ALS

def setup_environment(elastic_spark_connector_path,mysql_spark_connector_path):
    os.environ[
            'PYSPARK_SUBMIT_ARGS'] = "--driver-memory 4g --driver-class-path file:///"+elastic_spark_connector_path+" --jars file:///"+mysql_spark_connector_path+" pyspark-shell"
