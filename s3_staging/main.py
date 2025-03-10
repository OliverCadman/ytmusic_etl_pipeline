from s3_staging.load_s3 import S3Loader
from s3_staging.ytmusic_api.ytmusicapi_client import YTAPIClient
from ytmusicapi import YTMusic

def main():
    ytmusic = YTMusic("browser.json")
    ytmusic_loader_client = YTAPIClient(ytmusic)
    
    loader = S3Loader(ytmusic_loader_client)
    loader.perform_load("get_likes")


if __name__ == "__main__":
    main()
