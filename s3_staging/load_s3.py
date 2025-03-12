import dotenv
import json
from boto3 import client, resource
from boto3.session import Session
from botocore.exceptions import ClientError

from logging_service import setup_logger
from ytmusic_api.ytmusicapi_client import YTAPIClient
from ytmusic_api.exceptions import InvalidQueryType

from metadata.metadata_repository import MetadataRepository

import datetime
import os


logger = setup_logger(__name__, os.getcwd() + "/logs/load_s3.log")

# Prime with env variables used for AWS S3 interaction.
dotenv.load_dotenv(override=True)


class S3Loader:
    def __init__(self, ytapi_client: YTAPIClient):
        self.ytapi_client: YTAPIClient = ytapi_client
        self.s3_client: Session.client = client(
            "s3", 
            region_name=os.environ["AWS_REGION_NAME"],
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
            )
        self.s3_resource: Session.resource = resource(
            "s3", 
            region_name=os.environ["AWS_REGION_NAME"],
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
            )
        self.metadata = MetadataRepository()

    def get_and_serialize_data(self, query_type):
        logger.info(f"Getting data with query type '{query_type}'")
        data = None
        try:
            req = self.ytapi_client.make_query(query_type)
            data = self.convert_to_json(req)
            logger.info(f"Request with query type '{query_type}' successful.")
        except InvalidQueryType as e:
            print("INVALID QUERY TYPE:", query_type)
            logger.error(f"Error handling query type. Full error message: {e}")
        finally:
            return data

    def convert_to_json(self, obj):
        
        if not obj:
            raise ValueError("Argument 'obj' must be specified.")
        
        d = {}
        d["data"] = obj

        if isinstance(obj, list):
            # Count number of items in object.
            self.metadata.add_item(f"data_size", len(obj))

        return json.dumps(d)

    def _new_extract_required(self, dir_timestamp):
        # TODO: Test!
        """
        If the delta between now and the timestamp 
        is longer than a month, return True. Otherwise, 
        return False.

        Technically I guess this is not required if 
        the ETL DAG is scheduled to be ran every month,
        but I thought it was a safe bet to put it in.

        Params:
            - dir_timestamp: The timestamp provided for the
                             latest object's dirname.
            
        Returns:
            - True: If delta between timestamp and now is greater 
                    than one month.
            - False: If delta is less than one month.
        """
    
    def _get_now(self):
        """
        Return a datetime object representing the present time.
        """

        return datetime.date.today()

    def get_or_create_timestamped_object_path(self):
        """
        Supplements the S3 object key with the date
        of extraction.
        """
        now = self._get_now()
    
        key_name = os.environ["AWS_OBJECT_BASE_PATH"]

        timestamp = now.strftime("%d%m%Y")

        enriched_key = key_name + "/" + timestamp
        return enriched_key
    
    def _create_bucket(self):
        """
        Create an S3 bucket.

        Returns:
            None - Whether or not bucket exists.
        """

        bucket_name = os.environ["AWS_BUCKET_NAME"]
        region_name = os.environ["AWS_REGION_NAME"]

        try:
            res = self.s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": region_name
                }
            )

            logger.info(f"Created bucket with name '{bucket_name}'")
            return res
        except ClientError as err:
            logger.error(err)
            return None

    def perform_load(self, query_type):
        """
        Make the request, convert into a JSON serialize dict,
        and attempt load to S3.

        Args:
            query_type:
                Any query type supported by the enum 'QueryTypes'
        
        Returns:
            None

        """
        self._create_bucket()

        json_data = self.get_and_serialize_data(query_type)

        if json_data is None:
            logger.error(f"There was a problem loading data with the query '{query_type}'")
            return None

        object_path = self.get_or_create_timestamped_object_path()

        res = self.s3_client.put_object(
                    Bucket=os.environ["AWS_BUCKET_NAME"],
                    Body=bytes(json_data, encoding="utf-8"),
                    Key=object_path + f"/{query_type}.json",
                    Metadata=self.metadata.metadata
                )
        
        return res