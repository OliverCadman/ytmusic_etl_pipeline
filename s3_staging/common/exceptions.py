class RequestException(BaseException):
    def __init__(self, param: str):
        self.param = param

    def __str__(self):
        return f"Request with param '{self.param}' not supported. "