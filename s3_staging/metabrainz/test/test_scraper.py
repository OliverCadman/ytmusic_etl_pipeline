from unittest import TestCase

from requests import Response

from s3_staging.metabrainz.scraper import MetaBrainzScraper
from s3_staging.metabrainz.constants import BASE_URL, JSON_DATA_URL
from s3_staging.metabrainz.exceptions import InvalidURL


class MetaBrainzScraperTests(TestCase):
    """
    Testing request and parsing methods
    attributed to MetaBrainzScraper object.
    """


    def test_successful_request_correct_url(self):
        """
        Test that a 200 response is returned
        when accessing MetaBrainz JSON index via URL.
        """

        scraper = MetaBrainzScraper(JSON_DATA_URL)
        res: Response = scraper.perform_request()

        self.assertEqual(res.status_code, 200)

    def test_incorrect_url_raises_error(self):
        """
        Test that an InvalidURL error is raised
        if request is made with invalid url.
        """

        INVALID_URL = BASE_URL + "/invalid"
        scraper = MetaBrainzScraper(INVALID_URL)

        with self.assertRaises(InvalidURL):
            scraper.perform_request()

    def test_extract_artist_json_links_successful(self):
        """
        Test extracting a collection of links to
        download MetaBrainz JSON objects related
        to artist data.
        """

        scraper = MetaBrainzScraper(JSON_DATA_URL)

        scraper.extract_links()
