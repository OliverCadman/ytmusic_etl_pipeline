from ytmusicapi import YTMusic
from s3_staging.ytmusic_api.enums import QueryTypes
from s3_staging.ytmusic_api.exceptions import InvalidQueryType

class YTAPIClient:
    def __init__(self, ytmusic_api: YTMusic):
        self.ytmusic_api = ytmusic_api
        self.method_map = {
            QueryTypes.ARTISTS.value: self.ytmusic_api.get_library_artists,
            QueryTypes.LIKES.value: self.ytmusic_api.get_liked_songs,
            QueryTypes.HISTORY.value: self.ytmusic_api.get_history
        }

    def query_to_method(self, query_type):
        """
        Forward a given query type to object's method map.
        Choices are:
            - get_artists
            - get_likes
            - get_history
        """
        if query_type not in [i.value for i in QueryTypes]:
            print(f"query '{query_type} not listed in available query types")
            raise InvalidQueryType(query_type)
     
        return self.method_map[query_type] 
    
    def make_query(self, query_type):
        """
        Public factory method, delegating query type
        to the associated method provided by YTMusic API.
        """
        if query_type == QueryTypes.HISTORY.value:
            return self.query_to_method(query_type)()
        return self.query_to_method(query_type)(limit=None)
