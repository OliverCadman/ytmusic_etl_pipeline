from load_s3 import S3Loader
from ytmusic_api.ytmusicapi_client import YTAPIClient
from ytmusicapi import YTMusic

import os
import sys

print("OS PATH", os.getcwd())
print("SYS PATH", sys.path)

def main():
    ytmusic = YTMusic("browser.json")
    ytmusic_loader_client = YTAPIClient(ytmusic)
    
    loader = S3Loader(ytmusic_loader_client)
    loader.perform_load("history")


if __name__ == "__main__":
    main()
