"""
BNet:
    Bayesian Network data structures, and associated parsers
"""

from exceptions import *
import operator
import pdb

class BNode:
    """Variable in a bayesian network.
    Has an associated list of parents, and a probability table"""

    def __init__( self, id, parents=(), values=(), table=None ):
        """
        @id - Node reference id
        @parents - list of parents
        @table - Pr( X | parents )
        """
        self.id = id
        self.parents = parents
        self.values = values
        self.table = table

    def setValues( self, values ):
        self.values = values

    def setTable( self, table ):
        self.table = table

    def setParents( self, parents ):
        self.parents = tuple( parents )

    def __str__( self ):
        ret = "[Node %s %s]"%( str( self.id ), self.parents ) + '\n'
        ret += ' '.join( self.parents ) + ' | ' + ' '.join( self.values ) + '\n'
        if self.table: ret += '\n'.join( map( str, self.table ) )
        return ret

    def __repr__( self ):
        return "[Node %s]"%( str( self.id ) )

class BNet:
    """Graph on Bayesian variables"""

    def __init__( self ):
        self.variables = {}

    def add( self, node ):
        self.variables[ node.id ] = node

    def get( self, id ):
        return self.variables[ id ]

    def __str__( self ):
        return "[Net %s]"%( str( self.variables ) )


