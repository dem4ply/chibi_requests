from functools import reduce

from marshmallow import Schema, pre_load, INCLUDE, fields, post_load
from marshmallow.experimental.context import Context

from chibi_requests import Chibi_url, Response
from vcr_unittest import VCRTestCase


class Four_chan_schema( Schema ):
    id = fields.Integer( data_key='no' )
    replies = fields.Integer()
    url = fields.Function(
        lambda x: Context.get()["url"]
    )

    class Meta:
        unknown = INCLUDE

    @pre_load( pass_collection=True )
    def pre_load( self, data, **kw ):
        threads = reduce(
            ( lambda x, y: x + y ),
            ( page[ 'threads' ] for page in data ) )
        return threads


class Four_chan_context_schema( Schema ):
    id = fields.Integer( data_key='no' )
    replies = fields.Integer()
    url = fields.Function(
        lambda x: Context.get()["url"]
    )

    class Meta:
        unknown = INCLUDE

    @pre_load( pass_collection=True )
    def pre_load( self, data, **kw ):
        threads = reduce(
            ( lambda x, y: x + y ),
            ( page[ 'threads' ] for page in data ) )
        return threads

    @post_load( pass_collection=True )
    def post_data( self, data, **kw ):
        url = Context.get()[ 'url' ]
        for d in data:
            d[ 'url' ] = url
        return data


class Response_threads( Response ):
    serializer = Four_chan_schema
    is_raise_when_is_not_ok = True


class Response_threads_context( Response ):
    serializer = Four_chan_context_schema
    is_raise_when_is_not_ok = True


threads = Chibi_url(
    'http://a.4cdn.org/{board}/threads.json',
    response_class=Response_threads ).format( board='w' )

threads_context = Chibi_url(
    'http://a.4cdn.org/{board}/threads.json',
    response_class=Response_threads_context ).format( board='w' )


class Test_four_chan_with_schema( VCRTestCase ):
    def test_should_work( self ):
        response = threads.get()
        native = response.native
        self.assertIsInstance( native, list )
        self.assertTrue( native )
        for n in native:
            self.assertIn( 'id', n )
            self.assertIsInstance( n[ 'id' ], int )
            self.assertIn( 'replies', n )
            self.assertIsInstance( n[ 'replies' ], int )

    def test_with_context( self ):
        response = threads_context.get()
        native = response.native
        self.assertIsInstance( native, list )
        self.assertTrue( native )
        for n in native:
            self.assertIn( 'id', n )
            self.assertIsInstance( n[ 'id' ], int )
            self.assertIn( 'replies', n )
            self.assertIsInstance( n[ 'replies' ], int )
            self.assertIn( 'url', n )
            self.assertEqual( n.url, threads_context )
