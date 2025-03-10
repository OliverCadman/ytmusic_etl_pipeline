from pyspark.sql import SparkSession, functions as f
from dotenv import load_dotenv
import os

load_dotenv()

print("OS ENVIRON", os.environ)

spark: SparkSession = SparkSession.builder \
.appName("etl") \
.config(
    "spark.hadoop.fs.s3a.aws.credentials.provider", 
    "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
.config("fs.s3a.access.key", os.environ["AWS_ACCESS_KEY_ID"]) \
.config("fs.s3a.secret.key", os.environ["AWS_SECRET_ACCESS_KEY"]) \
.getOrCreate()

artists = spark.read.json("s3a://ytmusic-etl-staging-bucket/etl/staging/07032025/get_artists.json")

exploded_artists = artists.select(f.explode(f.col("data")))

exploded_artists.printSchema()
