from unittest import TestCase, mock, main as unittest_main
from data_loader.ytmusic_api.ytmusicapi_client import YTAPIClient
from data_loader.ytmusic_api.exceptions import InvalidQueryType
from ytmusicapi import YTMusic


class QuerySubmissionTests(TestCase):
    """
    Test GET requests with YTMusic.
    """

    def setUp(self):
        self.ytmusic = YTMusic("browser.json")
        self.ytmusicapi_client = YTAPIClient(self.ytmusic)

    def test_get_artists(self):
        """
        Confirm that the mapped query_method
        'get_artists' calls the correct function
        'get_library_artist', which is provided by the YTMusic package.
        """

        expected_res = self.ytmusic.get_library_artists()

        query_param = "get_artists"
        res = self.ytmusicapi_client.make_query(query_param)
        self.assertEqual(res, expected_res)
    
    def test_error_raised_when_invalid_query_supplied(self):
        """
        Confirm that InvalidQuery exception raised when 
        the 'get_data' method of Extractor class is provided
        a query_type which is not supported.
        """

        invalid_query_type = "invalid_query"

        with self.assertRaises(InvalidQueryType):
            self.ytmusicapi_client.query_to_method(invalid_query_type)

    def test_error_not_raised_when_valid_query_supplied(self):
        """
        Confirm that InvalidQuery does not raise exception when
        the 'get_data' method of Extractor class is provided
        with a supported query_type.
        """
        
        valid_query_type = "get_artists"

        res = self.ytmusicapi_client.query_to_method(valid_query_type)
        expected_res = self.ytmusicapi_client.method_map[valid_query_type]
        self.assertEqual(res, expected_res)


if __name__ == "__main__":
    unittest_main()
