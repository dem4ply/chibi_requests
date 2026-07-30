from requests.exceptions import HTTPError


class Client_error( HTTPError ):
    def __init__( self, response ):
        # self.response = response
        super().__init__(
            response=response, request=response._response.request )

    def __str__( self ):
        try:
            native = self.response.native
        except:
            native = self.response.body
        return (
            f"Client Error: {self.response.status_code} {self.response.url}\n"
            f"{native}"
        )

    def __repr__( self ):
        class_str = self.__class__.__qualname__
        return (
            f"{class_str}( status_code={self.response.status_code} "
            f"{self.response.url} )"
        )
