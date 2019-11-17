import token

# Node class holds
# a label consiste
# nt with the name
# of each function
# that creates eac
# h node. every fu
# nction creates e
# xactly one singl
# e tree node, eit
# her that or no t
# ree nodes. the c
# hildren are four
# max. all syntact
# ic tokens are ca
# st away, while a
# ll the other tok
# ens will be stor
# ed. 
class Node(object):
    def __init__(self, label = "", depth = None, child1 = None, child2 = None, child3 = None, child4 = None, token1 = token.Token(), token2 = token.Token(), token3 = token.Token(), token4 = token.Token(), toks = []):
        self.label = label
        self.depth = depth
        self.child1 = child1
        self.child2 = child2
        self.child3 = child3
        self.child4 = child4
        self.token1 = token1
        self.token2 = token2
        self.token3 = token3
        self.token4 = token4
        self.toks = toks