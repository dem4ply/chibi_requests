from unittest import TestCase, skip
from unittest.mock import Mock, patch

import requests
from bs4 import BeautifulSoup
from chibi.atlas import Chibi_atlas
from chibi.file.temp import Chibi_temp_path
from chibi.metaphors import Book
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError
from chibi_requests import Chibi_url, Response
from vcr_unittest import VCRTestCase


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
