from unittest import TestCase
from unittest.mock import Mock

from chibi_requests import Chibi_url, Response


class New_respone( Response ):
    pass


class Test_Response( TestCase ):
    def setUp( self ):
        super().setUp()
        self.url = Chibi_url( "https://google.com" )
        self.response = Response( Mock(), self.url )

    def test_response_by_default_should_have_parent_none( self ):
        self.assertIsNone( self.response.parent )

    def test_from_response_should_generate_a_response( self ):
        response = New_respone.from_response( self.response )
        self.assertIsInstance( response, New_respone )

    def test_from_response_should_add_parent( self ):
        response = New_respone.from_response( self.response )
        self.assertIs( response.parent, self.response )

    def test_response_should_have_context( self ):
        self.assertTrue( self.response.context )
        self.assertIsInstance( self.response.context, dict )

    def test_context_should_have_url( self ):
        self.assertEqual( self.response.context.url, self.url )

    def test_context_can_add_new_keys( self ):
        self.response.context.other_key = "other"
        self.assertEqual( self.response.context.other_key, "other" )
