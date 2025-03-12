from pyspark.sql import SparkSession, functions as f
from s3_client.client import S3Client

from dotenv import load_dotenv
import os

load_dotenv(override=True)

spark: SparkSession = SparkSession.builder \
.appName("etl") \
.config(
    "spark.hadoop.fs.s3a.aws.credentials.provider", 
    "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
.config("fs.s3a.access.key", os.environ["AWS_ACCESS_KEY_ID"]) \
.config("fs.s3a.secret.key", os.environ["AWS_SECRET_ACCESS_KEY"]) \
.getOrCreate()

s3 = S3Client()

# TODO: This currently returns only a single S3 object. Will need to modify how the dict is accessed.
latest_object = s3.get_latest_upload(os.environ["AWS_BUCKET_NAME"])

history_df = spark.read.json(f"s3a://{os.environ['AWS_BUCKET_NAME']}/{latest_object['Key']}")

exploded_history = history_df.select(f.explode(f.col("data")))

exploded_history.select(
    f.col("col.videoId"),
    f.col("col.title"),
    f.col("col.played"),
    f.col("col.views")
    )\
.show(truncate=False, n=exploded_history.count())
exploded_history.printSchema()

num_listens_per_artist = exploded_history.groupBy(
    f.col("col.videoId"), f.col("col.artists")
    ).count()

num_listens_per_artist.sort(f.col("count").desc()).show(truncate=False)
