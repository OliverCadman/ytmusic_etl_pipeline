import enum


class QueryTypes(enum.Enum):
    """
    A collection of supported query types.

    If a request is made with a query type
    that is not listed here, an InvalidQuery exception
    will be raised.
    """
 
    ARTISTS = "get_artists"
    LIKES = "get_likes"
    HISTORY = "history"