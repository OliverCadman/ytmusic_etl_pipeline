import requests
from bs4 import BeautifulSoup
from data_loader.metabrainz.exceptions import InvalidURL
from data_loader.logging import setup_logger


logger = setup_logger(__name__, "./data_loader/logs/scraper.log")


class MetaBrainzScraper:
    def __init__(self, url):
        self.url = url

    def perform_request(self):
        try:
            req = requests.get(self.url)
            if req.status_code == 404:
                raise InvalidURL(self.url)
            else:
                return req
        except requests.HTTPError as e:
            logger.error(f"Error performing request. Full error: {e}")
            return None
            
    def extract_links(self):
        req = self.perform_request()
        if not req:
            return None
        
        soup = BeautifulSoup(req.text, features="html.parser")
     