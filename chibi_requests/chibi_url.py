import requests
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from chibi_requests.response import Response

from chibi.atlas import Chibi_atlas


class Chibi_url( str ):
    def __add__( self, other ):
        if isinstance( other, Chibi_url ):
            raise NotImplementedError
        if isinstance( other, str ) and other.startswith( '?' ):
            parts = list( urlparse( self ) )
            current = parse_qs( parts[4], keep_blank_values=True )
            news = parse_qs( other[1:], keep_blank_values=True )
            current.update( news )
            parts[4] = urlencode( current, doseq=True )
            return Chibi_url( urlunparse( parts ) )
        elif isinstance( other, dict ):
            parts = list( urlparse( self ) )
            current = parse_qs( parts[4], keep_blank_values=True )
            current.update( other )
            parts[4] = urlencode( current, doseq=True )
            return Chibi_url( urlunparse( parts ) )
        return Chibi_url( "/".join( self.split( '/' ) + [ other ] ) )

    def __eq__( self, other ):
        if isinstance( other, Chibi_url ):
            return str( self ) == str( other )
        if isinstance( other, str ):
            return str( self ) == other
        return False

    def __hash__( self ):
        return hash( str( self ) )

    @property
    def base_name( self ):
        return self.rsplit( '/', 1 )[-1]

    @property
    def parts( self ):
        try:
            return self._parts
        except AttributeError:
            self._parts = list( urlparse( self ) )
            return self._parts

    @property
    def params( self ):
        current = parse_qs( self.parts[4], keep_blank_values=True )
        for k, v in current.items():
            if isinstance( v, list ) and len( v ) == 1:
                current[k] = v[0]
        return Chibi_atlas( current )

    @property
    def schema( self ):
        return self.parts[0]

    @property
    def host( self ):
        return self.parts[1]

    def get( self, *args, **kw ):
        response = requests.get( self, *args, **kw )
        return Response( response )

    def post( self, *args, **kw ):
        response = requests.post( self, *args, **kw )
        return Response( response )
