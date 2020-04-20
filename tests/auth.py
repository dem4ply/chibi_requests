from unittest.mock import Mock

from chibi_requests import Chibi_url
from chibi_requests.auth import Token, Bearer
from tests.chibi_url import Test_url


class Test_auth_token( Test_url ):
    def setUp( self ):
        self.url = Chibi_url( "https://google.com" )

    def test_when_is_called_should_add_the_header( self ):
        token = Token( token='hello' )
        mock = Mock( headers=dict() )
        result = token( mock )
        self.assertIs( mock, result )
        self.assertEqual( mock.headers, { 'Authorization': 'Token hello' } )

    def test_when_have_the_name_should_change_the_name_of_the_token( self ):
        token = Token( token='hello', name='Bearer' )
        mock = Mock( headers=dict() )
        result = token( mock )
        self.assertIs( mock, result )
        self.assertEqual( mock.headers, { 'Authorization': 'Bearer hello' } )

    def test_bearer__by_default_should_be_bearer( self ):
        token = Bearer( token='hello' )
        mock = Mock( headers=dict() )
        result = token( mock )
        self.assertIs( mock, result )
        self.assertEqual( mock.headers, { 'Authorization': 'Bearer hello' } )
