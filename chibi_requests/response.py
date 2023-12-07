from bs4 import BeautifulSoup
from chibi.atlas import Chibi_atlas_ignore_case, _wrap, loads, Atlas
from marshmallow import Schema


class Response:
    serializer = None

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
    def content( self ):
        return self._response.content

    @property
    def pagination( self ):
        try:
            return self._pagination
        except AttributeError:
            raise NotImplementedError(
                "in the response {} is not implemented the pagination".format(
                    str( type( self ) )
                ) )

    @property
    def content_type( self ):
        return self.headers[ 'Content-Type' ]

    @property
    def is_json( self ):
        return 'application/json' in self.content_type

    @property
    def is_xml( self ):
        return (
            self.content_type == 'application/xml'
            or 'text/xml' in self.content_type
        )

    @property
    def is_text( self ):
        return 'text/plain' in self.content_type

    @property
    def is_html( self ):
        return 'text/html' in self.content_type

    @property
    def status_code( self ):
        return self._response.status_code

    def parse_like_json( self ):
        json_result = self._response.json()
        return _wrap( json_result )

    def parse_like_xml( self ):
        return loads( self.body )

    def parse_content_type( self ):
        if self.is_json:
            return self.parse_like_json()
        elif self.is_xml:
            return self.parse_like_xml()
        elif self.is_html:
            return BeautifulSoup( self.body, 'html.parser' )
        elif self.is_text:
            return self.body
        else:
            raise NotImplementedError(
                f'no puede parsear el content-type: {self.content_type}' )

    def get_serializer( self ):
        if self.serializer is None:
            return None
        if isinstance( self.serializer, type ):
            serializer = self.serializer
            if issubclass( serializer, Schema ):
                return serializer
            else:
                raise NotImplementedError(
                    'No implementados los serializadores que '
                    'no son de marshmallow' )
        elif isinstance( self.serializer, Schema ):
            return type( self.serializer )
        else:
            raise NotImplementedError(
                'No implementados los serializadores que '
                'no son de marshmallow' )

    def parse_native( self ):
        parse = self.parse_content_type()
        serializer = self.get_serializer()
        if serializer:
            many = self.native_is_many
            serializer = serializer()
            serializer.context[ 'url' ] = self.url
            parse = serializer.load( parse, many=many )
            if isinstance( parse, ( dict, list ) ):
                parse = Atlas( parse )
        return parse

    @property
    def native_is_many( self ):
        parse = self.parse_content_type()
        return isinstance( parse, list )

    @property
    def ok( self ):
        return self.status_code == 200

    def __bool__( self ):
        return self.ok
