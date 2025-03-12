import boto3
from botocore.exceptions import ClientError

from logging_service import setup_logger

import dotenv
import os
import datetime

dotenv.load_dotenv(override=True)

logger = setup_logger(__name__, os.getcwd() + "/logs/s3_client.log")


class S3Client:
    """
    S3 Client, used to query objects in bucket.

    Methods:
        - _list_objects:
            Lists all objects in the bucket
        -  get_latest_uploaded_object:
            Extracts the most recently-uploaded object.
            Uses the list_objects as a private function.
    """
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            region_name=os.environ["AWS_REGION_NAME"],
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
        )
    
    def _list_objects(self, bucket_name):
        """
        List the objects under a given bucket.
        """

        try:
            logger.info(f"Listing objects in bucket '{bucket_name}'")
            return self.s3_client.list_objects(
                Bucket=bucket_name
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucket":
                msg = f"Bucket doesn't seem to exist. Full error: {e}"
                print(msg)
                logger.error(msg)
                return None
        
    def get_latest_upload(self, bucket_name):
        """
        Find the S3 object that has been uploaded most recently.
        """

        objects = self._list_objects(os.environ["AWS_BUCKET_NAME"])

        if not objects:
            return None

        track = {
            "min_delta": float("inf"),
            "object_contents": None
        }
        for i in objects["Contents"]:
            
            date_of_upload: datetime.datetime = i["LastModified"]
            now: datetime.datetime = datetime.datetime.now()
            delta: datetime.timedelta = now - date_of_upload.replace(tzinfo=None)

            if delta.days < track["min_delta"]:
                track["min_delta"] = delta.days
                track["object_contents"] = i
            
        return track["object_contents"]
