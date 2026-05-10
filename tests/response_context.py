from unittest import TestCase
from unittest.mock import Mock

from chibi_requests import Chibi_url, Response

from marshmallow import Schema
from chibi_marshmallow import fields as chibi_fields


class Context_schema( Schema ):
    url = chibi_fields.Context()
    other = chibi_fields.Context()


class New_respone( Response ):
    serializer = Context_schema


class Test_Response_context( TestCase ):
    def setUp( self ):
        super().setUp()
        self.url = Chibi_url( "https://google.com" )
        self.mock = Mock()
        self.mock.headers = { "Content-Type": "application/json" }
        self.mock.json.return_value = {}
        self.response = New_respone( self.mock, self.url )

    def test_context_can_add_new_keys( self ):
        self.response.context.other = "other"
        self.assertEqual( self.response.native.url, self.url )
        self.assertEqual( self.response.native.other, "other" )
