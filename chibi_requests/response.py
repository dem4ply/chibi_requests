from chibi.atlas import Chibi_atlas_ignore_case
from chibi.atlas import _wrap


class Response:
    def __init__( self, response, url ):
        self._response = response
        self.url = url

    @property
    def headers( self ):
        try:
            return self._headers
        except AttributeError:
            self._headers = Chibi_atlas_ignore_case( self._response.headers )
            return self._headers

    @property
    def body( self ):
        return self._response.text

    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            self._native = self.parse_native()
            return self._native

    @property
    def content_type( self ):
        return self.headers[ 'Content-Type' ]

    @property
    def is_json( self ):
        return 'application/json' in self.content_type

    @property
    def is_xml( self ):
        return self.content_type == 'application/xml'

    @property
    def is_text( self ):
        return 'text/plain' in self.content_type

    @property
    def status_code( self ):
        return self._response.status_code

    def parse_like_json( self ):
        json_result = self._response.json()
        return _wrap( json_result )

    def parse_like_xml( self ):
        raise NotImplementedError

    def parse_native( self ):
        if self.is_json:
            return self.parse_like_json()
        elif self.is_xml:
            return self.parse_like_xml()
        elif self.is_text:
            return self.body
        else:
            raise NotImplementedError
