from s3_staging.common.exceptions import RequestException


class InvalidURL(RequestException):
    def __init__(self, param):
        super().__init__(param)
