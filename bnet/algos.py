"""
Algorithms for Bayesian Networks
"""

import copy
import random
import pdb

def cdf( pdf ):
    """Make a choice from a value set in correspondence with attached probabilities"""
    cdf_ = []
    P = 0
    for v,pr in pdf:
        P += pr
        cdf_.append( (v, P) )

    return cdf_

def binsearch(items, val, key=lambda x: x):
    """
    Returns the item in items whose bucket contains val - assumes items is (item, bottom of bucket)
    """
    low, high = 0, len(items)-1
    while ((high - low) > 0):
        if val < key(items[(low+high)/2]):
            high = (low+high)/2 
        elif val == key(items[(low+high)/2]):
            low = high = (low+high)/2
        else:
            low = (low+high)/2 + 1

    return items[high]

def select( items, key = lambda x: x):
    """Randomly select an item based on the (val, pr) list given"""
    return binsearch(items, random.random(), key) 


def roulette(items, num, key=lambda x: x):
    """
    Runs a roulette selection algorithm on the items in the list given. 
    The algorithm is roughly a binary search on the list to find out which item is to be selected (with random values)
    """

    selection = [ select( items ) for i in xrange(num)]
    return selection

def gibbsSample( net, ctx, burnIn=100, samples=1000 ):
    """
    Apply gibbs sampling to infer a new Network
    """
    def gibbsChoice( net, ctx, node ):
        # Get the nodes for the Markov Blanket
        children = map( net.get, net.getChildren( node.id ) )
        parents = map( net.get , net.getParents( node.id ) )

        Pr = []
        # Get P( V | p)
        prVector = ctx.prVector( node.id )
        for val, prP in prVector.items():
            # Pr of any value Pr( V | p, c ) = P( c | V ) * P( V | p ) 
            ctx.setVariable( node.id, val )
            pr = prP
            for child in net.getChildren( node.id ):
                prVector_ = ctx.prVector( child )
                pr *= prVector_[ ctx.get( child ) ]
            Pr.append( (val, pr ) )
        total = sum( [ pr for v, pr in Pr ] )
        Pr = [ (v,pr/total) for v,pr in Pr ] 

        val = select( cdf( Pr ), key = lambda vPr: vPr[1] )
        return val[0]


    # Create a deep copy of the net to modify
    net = copy.deepcopy( net )
    ctx = copy.deepcopy( ctx )

    # Set the variables present in the context to be equal to the value in the
    # context
    net.applyContext( ctx )

    # List of variables whose value is to be modified
    variables = net.variables.keys()
    for k,v in ctx.getVariables():
        variables.remove( k )

    # Choose a random initial value for all variables 
    for var in variables:
        ctx.setVariable( var, random.choice( net.get( var ).values ) )

    # Just follow the MC
    for i in xrange( burnIn ):
        # Choose one variable, a randomly 
        var = random.choice( variables )
        node = net.get( var )
        val = gibbsChoice( net, ctx, node )
        ctx.setVariable( node.id, val )


    return net

