import collections
import sys

import node
import token

class S:
    def __init__(self):
        self.scope_size = 0
        self.var_count = 0
        self.scope_start = 0
        self.offset = 0
s = S()

scope = [token.Token() for _ in range(100)]

def scope_push(tk):
    if s.scope_size >= 100:
        print "ERROR: Stack of size", s.scope_size, " caused overflow"
        sys.exit(1)
    else:
        for i in xrange(s.scope_start, s.scope_size, 1): 
            if scope[i].instance == tk.instance:
                print "ERROR:", tk.instance, "previously declared within scope"
                sys.exit(1)
        scope[s.scope_size] = tk
        s.scope_size = s.scope_size + 1

def scope_pop(scope_start): 
    for i in xrange(s.scope_size, scope_start, -1):
        s.scope_size = s.scope_size - 1
        scope[i].instance = ""

def scope_find(tk):
    for i in xrange(s.scope_size, s.scope_start - 1, -1):
        if scope[i-1].instance == tk.instance:
            s.offset = s.scope_size - i
            return s.offset
    return -1

def var_in_scope(tk):
    for i in xrange(s.scope_size - 1, -1, -1):
        if scope[i].instance == tk.instance:
            return True
    return False

def static_semantics(node, count):
    if node == None:
        return
    if node.label == "<program>":
        s.var_count = 0
        if node.child1 != None:
            static_semantics(node.child1, s.var_count)
        if node.child2 != None:
            static_semantics(node.child2, s.var_count)

    elif node.label == "<vars>":
        s.offset = scope_find(node.token1)
        s.scope_start = s.scope_size
        if s.offset == -1 or s.offset > count:
            scope_push(node.token1)
            count = count + 1
        elif s.offset < count:
            print "ERROR:", node.token1.instance, "previously declared within scope"
            sys.exit(1)
        if node.child1 != None:
            static_semantics(node.child1, count)

    elif node.label == "<block>":
        s.var_count = 0
        s.scope_start = s.scope_size
        if node.child1 != None:
            static_semantics(node.child1, s.var_count)
        if node.child2 != None:
            static_semantics(node.child2, s.var_count)
        scope_pop(s.scope_start)

    elif node.label == "<expr>":
        if node.token1.identity == "PLUS_tk":
            if node.child1 != None:
                static_semantics(node.child1, count)
            if node.child2 != None:
                static_semantics(node.child2, count)
        elif node.child1 != None:
            static_semantics(node.child1, count)

    elif node.label == "<R>":
        if node.token1.identity == "ID_tk":
            if var_in_scope(node.token1) == False:
                print "ERROR:", node.token1.instance, "undeclared within scope"
                sys.exit(1)
        elif node.child1 != None:
            static_semantics(node.child1, count)

    elif node.label == "<in>":
        if var_in_scope(node.token1) == False:
            print "ERROR:", node.token1.instance, "undeclared within scope"
            sys.exit(1)

    elif node.label == "<assign>":
        if var_in_scope(node.token1) == False:
            print "ERROR:", node.token1.instance, "undeclared within scope"
            sys.exit(1)
        if node.child1 != None:
            static_semantics(node.child1, count)
    else:
        if node.child1 != None:
            static_semantics(node.child1, count)
        if node.child2 != None:
            static_semantics(node.child2, count)
        if node.child3 != None:
            static_semantics(node.child3, count)
        if node.child4 != None:
            static_semantics(node.child4, count)