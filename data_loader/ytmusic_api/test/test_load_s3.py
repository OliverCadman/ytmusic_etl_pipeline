import moto
from unittest import TestCase, mock
from botocore.exceptions import ClientError
from ytmusicapi import YTMusic
from data_loader.load_s3 import S3Loader
from data_loader.ytmusic_api.ytmusicapi_client import YTAPIClient

import json
import datetime

from dotenv import load_dotenv
import os

load_dotenv()

def mocked_get_now():
    return datetime.date(2025, 2, 20)


class S3LoadIntegrationTests(TestCase):
    def setUp(self):
        self.ytmusic_api = YTMusic("browser.json")
        self.yt_api_client = YTAPIClient(self.ytmusic_api)
        self.s3_loader = S3Loader(self.yt_api_client)

    @moto.mock_aws
    def test_create_bucket_successful(self):
        """
        Confirm that the _create_bucket method
        creates an S3 bucket successfully.
        """
        res = self.s3_loader._create_bucket()

        print("bucket...", res)

        self.assertTrue(res)
        self.assertEqual(res.name, "ytmusic_etl_staging_bucket")
    
    @moto.mock_aws
    def test_error_raised_when_bucket_exists(self):
        """
        Confirm that boto3's BucketAlreadyExists error is
        raised when a bucket with the same name is attempted to 
        be created.
        """

        res = self.s3_loader._create_bucket()
        self.assertTrue(res)

        res = self.s3_loader._create_bucket()
        self.assertEqual(res, None)

    @moto.mock_aws
    @mock.patch("data_loader.load_s3.S3Loader._get_now", side_effect=mocked_get_now)
    def test_create_timestamped_object_path(self, patched_date):
        """
        Confirm that an object's path name includes the date at which
        the object is being loaded to S3.
        """
        patched_date.return_value = datetime.datetime(2025, 1, 1)
        
        res = self.s3_loader.get_or_create_timestamped_object_path()

        expected_strftime = mocked_get_now().strftime("%d%m%Y")
        
        expected_res = os.environ["AWS_OBJECT_BASE_PATH"] + "/" + expected_strftime
        self.assertEqual(res, expected_res)

    def test_new_extract_required(self):
        pass
        
    def test_load_with_timestamped_directory(self):
        pass

    def test_metadata_push_successful(self):
        pass

    def test_get_timestamped_file(self):
        pass


class S3LoadE2ETests(TestCase):
    def setUp(self):
        self.ytmusic_api = YTMusic("browser.json")
        self.yt_api_client = YTAPIClient(self.ytmusic_api)
        self.s3_loader = S3Loader(self.yt_api_client)
    
    @moto.mock_aws
    @mock.patch("data_loader.load_s3.S3Loader._get_now", side_effect=mocked_get_now)
    def test_get_and_load(self, patched_now):
        """
        Verify the lifecycle flow of:
            - Getting data
            - Saving to Temp JSON file
            - Loading JSON file to S3 bucket with expected object name.
        """

        with mock.patch.object(self.yt_api_client, "make_query") as mocked_query:
            mocked_return = {
                "test_e2e": "example"
            }

            mocked_query.return_value = mocked_return

            query_type = "history"

            res = self.s3_loader.perform_load(query_type)

            print(res)
            self.assertIn("ResponseMetadata", res)
            self.assertEqual(res["ResponseMetadata"]["HTTPStatusCode"], 200)
