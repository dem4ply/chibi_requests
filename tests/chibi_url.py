from unittest import TestCase
from unittest.mock import Mock, patch

import requests
from bs4 import BeautifulSoup
from chibi.atlas import Chibi_atlas
from chibi.file.temp import Chibi_temp_path
from chibi.metaphors import Book
from requests.auth import HTTPBasicAuth

from chibi_requests import Chibi_url, Response


class Test_url( TestCase ):
    def setUp( self ):
        self.url = Chibi_url( "https://google.com" )


class Test_base_name( Test_url ):
    def test_base_name_should_return_the_last_part( self ):
        self.url = self.url + "1234567"
        base_name = self.url.base_name
        self.assertEqual( "1234567", base_name )


class Test_url_add( Test_url ):
    def test_can_add_parts( self ):
        self.assertIsInstance( self.url + "cosa", Chibi_url )
        self.assertEqual( "https://google.com/cosa", self.url + "cosa" )
        self.assertEqual(
            "https://google.com/cosa/cosa2", self.url + "cosa/cosa2" )
        self.assertEqual(
            "https://google.com/cosa/cosa2/cosa3",
            ( self.url + "cosa/cosa2" ) + "cosa3" )

        self.assertEqual(
            "https://google.com/cosa4",
            ( self.url + "cosa/cosa2" ) + '/cosa4' )

    def test_add_a_query( self ):
        result = self.url + "?param1=value1"
        self.assertEqual( { 'param1': 'value1' }, result.params )
        self.assertEqual(
            { 'param1': 'value1', 'param2': 'value2' },
            ( result + "?param2=value2" ).params )

    def test_add_a_dict_should_add_the_query( self ):
        result = self.url + { 'param1': 'value1' }
        self.assertEqual( { 'param1': 'value1' }, result.params )

        result = result + { 'param2': 'value2' }
        self.assertEqual(
            { 'param1': 'value1', 'param2': 'value2' },
            result.params )

        result = self.url + { 'param1': 'value1', 'param2': 'value2' }
        self.assertEqual(
            { 'param1': 'value1', 'param2': 'value2' }, result.params )

    def test_add_root_with_parameters_should_be_removed( self ):
        result = self.url + { 'param1': 'value1' }
        result = result + '/cosa1'
        self.assertEqual( result, self.url + '/cosa1' )

    def test_add_a_book_should_add_the_query( self ):
        book = Book( page=20, page_size=10, total_elements=1000 )
        result = self.url + book
        offset = { k: str( v ) for k, v in book.offset.items() }
        self.assertEqual( result.params, offset )

    def test_add_a_complete_url_should_renplace_all( self ):
        result = self.url + 'http://ifconfig.me'
        self.assertEqual( result, 'http://ifconfig.me' )


class Test_add_mainteing_the_response_class( Test_url ):
    def setUp( self ):
        super().setUp()
        self.response_class = Mock
        self.url = Chibi_url(
            "https://google.com", response_class=self.response_class )

    def test_with_dict_should_mainteing_the_response_class( self ):
        result = self.url + { 'param1': 'value1' }
        self.assertEqual( result.response_class, self.response_class )

    def test_with_str_should_mainteing_the_response_class( self ):
        result = self.url + 'cosa'
        self.assertEqual( result.response_class, self.response_class )

    def test_with_query_should_mainteing_the_response_class( self ):
        result = self.url + "?param1=value1"
        self.assertEqual( result.response_class, self.response_class )

    def test_with_book_should_mainteing_the_response_class( self ):
        book = Book( page=20, page_size=10, total_elements=1000 )
        result = self.url + book
        self.assertEqual( result.response_class, self.response_class )


class Test_property( Test_url ):
    def test_host_should_return_host( self ):
        host = self.url.host
        self.assertEqual( "google.com", host )

    def test_schema_should_return_schema( self ):
        schema = self.url.schema
        self.assertEqual( "https", schema )


class Test_methods( Test_url ):
    def setUp( self ):
        self.url = Chibi_url( 'http://ifconfig.me' )

    def test_get( self ):
        response = self.url.get()
        self.assertTrue( response )
        self.assertIsInstance( response, Response )
        self.assertTrue( response.is_text )
        self.assertIsInstance( response.native, str )
        self.assertTrue( response.native )

    def test_post( self ):
        response = self.url.post()
        self.assertTrue( response )
        self.assertIsInstance( response, Response )
        self.assertTrue( response.is_json )
        self.assertIsInstance( response.native, Chibi_atlas )
        self.assertTrue( response.native )


class Test_download_lenna( TestCase ):
    def setUp( self ):
        self.download_folder = Chibi_temp_path()
        self.lenna_url = Chibi_url( 'http://www.lenna.org/len_std.jpg' )

    def test_download_lenna( self ):
        lenna = self.lenna_url.download( self.download_folder )
        self.assertTrue( lenna.exists )
        self.assertGreater( lenna.properties.size, 10000 )

    def test_download_wiith_file_name( self ):
        lenna = self.lenna_url.download(
            self.download_folder + 'helloooo_lenna.png' )
        self.assertEqual( lenna.base_name, 'helloooo_lenna.png' )
        self.assertTrue( lenna.exists )
        self.assertGreater( lenna.properties.size, 10000 )


class Test_meta( Test_url ):
    def test_meta_empty( self ):
        self.assertEqual( self.url.kw, {} )

    def test_meta_with_values( self ):
        url = Chibi_url(
            "https://www.google.com", cosa1="cosa1", cosa2="cosa2" )
        self.assertEqual( url.kw, { 'cosa1': 'cosa1', 'cosa2': 'cosa2' } )


class Test_str_functions( Test_url ):
    def setUp( self ):
        super().setUp()
        self.url = Chibi_url( 'http://a.4cdn.org/{board}/threads.json' )

    def test_format( self ):
        result = self.url.format( board='a' )
        self.assertIsInstance( result, Chibi_url )
        self.assertEqual( result, "http://a.4cdn.org/a/threads.json" )

    def test_format_with_params( self ):
        url = self.url + { 'param1': 'value1' }
        result = url.format( board='a' )
        self.assertIsInstance( result, Chibi_url )
        self.assertEqual(
            result, "http://a.4cdn.org/a/threads.json?param1=value1" )
        self.assertEqual(
            result.params, { 'param1': 'value1' } )

    def test_format_shoudl_add_meta( self ):
        url = self.url.format( board='a' )
        self.assertEqual( url.kw, { 'board': 'a' } )

    def test_format_should_conservate_meta( self ):
        url = Chibi_url( self.url, cosa1="cosa1" )
        url = url.format( board='a' )
        self.assertEqual( url.kw, { 'board': 'a', "cosa1": "cosa1" } )

    def test_format_should_conservate_response_class( self ):
        url = Chibi_url( self.url, response_class=Mock )
        url = url.format( board='a' )
        self.assertEqual( url.response_class, Mock )


class Test_auth( Test_url ):
    def setUp( self ):
        super().setUp()
        self.url = Chibi_url( 'http://a.4cdn.org/{board}/threads.json' )

    def test_when_add_a_auth_class_should_create_a_new_object( self ):
        url_other = self.url + HTTPBasicAuth( 'some_user', 'some_password' )
        self.assertIsNot( self.url, url_other )
        self.assertEqual( str( self.url ), str( url_other ) )
        self.assertIsNotNone( url_other.auth )
        self.assertIsNone( self.url.auth )

    def test_using_iadd_should_add_iternaly_the_auth( self ):
        auth = HTTPBasicAuth( 'some_user', 'some_password' )
        self.url += auth
        self.assertIsNotNone( self.url.auth )
        self.assertEqual( self.url.auth, auth )

    def test_add_parmas_to_the_url_shoudl_carry_the_auth( self ):
        auth = HTTPBasicAuth( 'some_user', 'some_password' )
        self.url += auth
        other_url = self.url + { 'param1': 'value1' }

        self.assertNotEqual( self.url , other_url )
        self.assertEqual( self.url.auth, other_url.auth )

    @patch( 'requests.get' )
    def test_should_send_the_auth_using_get( self, requests ):
        self.url += HTTPBasicAuth( 'some_user', 'some_password' )
        self.url.get()
        self.assertEqual( requests.call_args[1][ 'auth' ], self.url.auth )

    @patch( 'requests.post' )
    def test_should_send_the_auth_using_post( self, requests ):
        self.url += HTTPBasicAuth( 'some_user', 'some_password' )
        self.url.post()
        self.assertEqual( requests.call_args[1][ 'auth' ], self.url.auth )


class Test_session( Test_url ):
    def test_add_a_session_should_create_a_new_url( self ):
        session = requests.Session()
        url_other = self.url + session
        self.assertIsNot( self.url, url_other )
        self.assertEqual( str( self.url ), str( url_other ) )
        self.assertIsNotNone( url_other.session )
        self.assertIsNone( self.url.session )

    def test_iadd_a_session_should_create_a_new_url( self ):
        session = requests.Session()
        self.url += session
        self.assertEqual( self.url.session, session )
        self.assertIsNotNone( self.url.session )

    def test_add_parmas_to_the_url_shoudl_carry_the_session( self ):
        session = requests.Session()
        self.url += session
        other_url = self.url + { 'param1': 'value1' }

        self.assertNotEqual( self.url , other_url )
        self.assertEqual( self.url.session, other_url.session )

    @patch( 'requests.Session.get' )
    def test_should_use_the_session_when_using_get( self, get ):
        session = requests.Session()
        self.url += session
        self.url.get()
        get.assert_called()

    @patch( 'requests.Session.post' )
    def test_should_use_the_session_when_using_post( self, post ):
        session = requests.Session()
        self.url += session
        self.url.post()
        post.assert_called()


class Test_html_parser( Test_url ):
    def test_get( self ):
        response = self.url.get()
        self.assertTrue( response )
        self.assertIsInstance( response, Response )
        self.assertTrue( response.is_html )
        self.assertIsInstance( response.native, BeautifulSoup )
        self.assertTrue( response.native )


class Test_properties( Test_url ):
    def test_url( self ):
        with self.subTest( "is a chibi_url" ):
            self.assertIsInstance( self.url.url, Chibi_url )
        with self.subTest( "normal url are equals" ):
            self.assertEqual( self.url, self.url.url )
        with self.subTest( "with parans url are equals" ):
            url = self.url + { 'param': 'value' }
            self.assertEqual( self.url, url.url )


class Test_headers( Test_url ):
    def setUp( self ):
        super().setUp()
        self.url = Chibi_url( 'http://a.4cdn.org/{board}/threads.json' )

    def test_headers_by_default_should_be_a_empty_dict( self ):
        self.assertIsInstance( self.url.headers, dict )
        self.assertEqual( self.url.headers, {} )

    def test_should_add_the_content_type( self ):
        self.url.headers.content_type = 'application/json'
        self.assertEqual( self.url.headers.content_type, 'application/json' )

    @patch( 'requests.get' )
    def test_should_send_the_auth_using_get( self, requests ):
        self.url.headers.content_type = 'application/json'
        self.url.get()
        self.assertEqual(
            requests.call_args[1][ 'headers' ], self.url.headers )

    @patch( 'requests.post' )
    def test_should_send_the_auth_using_post( self, requests ):
        self.url.headers.content_type = 'application/json'
        self.url.post()
        self.assertEqual(
            requests.call_args[1][ 'headers' ], self.url.headers )

    @patch( 'requests.post' )
    def test_should_be_parse_data_with_content_type( self, requests ):
        self.url.headers.content_type = 'application/json'
        self.url.post( { 'data': 'asdf' } )
        j = requests.call_args[0][1]
        self.assertEqual( j, '{"data": "asdf"}' )
