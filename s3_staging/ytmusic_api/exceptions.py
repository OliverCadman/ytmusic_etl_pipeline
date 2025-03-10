from s3_staging.ytmusic_api.enums import QueryTypes

from s3_staging.common.exceptions import RequestException

class InvalidQueryType(RequestException):
    """
    Exception raised when a request is made using a query type
    that is not listed in the QueryTypes enum object.
    """
    def __init__(self, query_type: str):
        super().__init__(query_type)
        self.available_types: QueryTypes = ", ".join([i.value for i in QueryTypes])

    def __str__(self):
        parent_msg = super().__str__()
        return parent_msg + f"Available params are '{self.available_types}'"
