"""
Libbnet shell
"""

from bnet.parsers import RaviParser, BNIFParser
from bnet.BNet import *

import sys
import readline

class NetShell():
    """
    Shell to interact with a Bayesian network
    """

    def __init__( self, net ):
        self.net = net
        self.running = False
        self.context = []

    def getContext( self ):
        if self.context:
            return self.context[-1]
        else:
            return None

    def run( self ):
        self.running = True
        self.context = [ Context( self.net ) ]
        while self.running:
            try:
                line = raw_input("[bnet]$ ")

                if line.startswith('%'): self.shellFunc( line[1:] )

            except EOFError:
                break
    
    def shellFunc( self, cmd ):
        args = cmd.split()
        if args[0] == "vars":
            if len( args ) > 1:
                id = args[1]
                print str( self.net.variables[ id ] )
            else:
                print self.net.variables.keys()
        elif args[0] == "push":
            self.context.append( Context( self.net, self.getContext() ) )
        elif args[0] == "pop":
            if len( self.context ) == 1:
                print "Error: At base context"
            else:
                self.context.pop()
        elif args[0] == "quit" or args[0] == "q":
            self.running = False

def main():
    if len( sys.argv ) != 2:
        print "Usage: %s <file>"%( sys.argv[ 0 ] )
        sys.exit( 1 )

    filename = sys.argv[ 1 ]

    p = BNIFParser()
    n = p.parseFile( filename )

    shell = NetShell( n )

    shell.run()



if __name__ == "__main__": main()

