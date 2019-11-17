import collections
import sys

import node
import token

class S:
    def __init__(self):
        self.label_count = 0
        self.scope_start = 0
        self.scope_size = 0
        self.temp_count = 0
        self.var_count = 0
        self.offset = 0
s = S()

scope = [token.Token() for _ in range(100)]
# temps = ["" for _ in range(100)]

def fetch_temp():
    temp = "T" + str(s.temp_count + 1)
    temps[s.temp_count] = temp
    s.temp_count = s.temp_count + 1 
    return temp

def fetch_label():
    labeling = "L" + str(s.label_count + 1)
    s.label_count = s.label_count + 1
    return labeling

def scope_push(tk, fout):
    if s.scope_size >= 100:
        print "ERROR: Stack of size", s.scope_size, " caused overflow"
        sys.exit(1)
    else:
        for i in xrange(s.scope_start, s.scope_size, 1): 
            if scope[i].instance == tk.instance:
                print "ERROR:", tk.instance, "previously declared within scope"
                sys.exit(1)
        scope[s.scope_size] = tk
        #fout.write("PUSH\n")
        s.scope_size = s.scope_size + 1

def scope_pop(scope_start, fout): 
    for i in xrange(s.scope_size, scope_start, -1):
        s.scope_size = s.scope_size - 1
        scope[i].instance = ""
        #fout.write("POP\n")

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

def static_semantics(node, count, fout, storage_names):
    if node == None:
        return
    if node.label == "<program>":
        s.var_count = 0
        if node.child1 != None:
            static_semantics(node.child1, s.var_count, fout, storage_names)
        if node.child2 != None:
            static_semantics(node.child2, s.var_count, fout, storage_names)
        fout.write("STOP\n")
        for storage_name in storage_names:
            if storage_name != "":
                fout.write(storage_name + "\n")

    elif node.label == "<vars>":
        s.offset = scope_find(node.token1)
        s.scope_start = s.scope_size
        if s.offset == -1 or s.offset > count:
            scope_push(node.token1, fout)
            count = count + 1
        elif s.offset < count:
            print "ERROR:", node.token1.instance, "previously declared within scope"
            sys.exit(1)
        if node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)

    elif node.label == "<block>":
        s.var_count = 0
        s.scope_start = s.scope_size
        if node.child1 != None:
            static_semantics(node.child1, s.var_count, fout, storage_names)
        if node.child2 != None:
            static_semantics(node.child2, s.var_count, fout, storage_names)
        scope_pop(s.scope_start, fout)

    elif node.label == "<expr>":
        if node.token1.identity == "PLUS_tk":
            if node.child1 != None:
                static_semantics(node.child1, count, fout, storage_names)
            if node.child2 != None:
                static_semantics(node.child2, count, fout, storage_names)
        elif node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)

    elif node.label == "<R>":
        if node.token1.identity == "ID_tk":
            if var_in_scope(node.token1) == False:
                print "ERROR:", node.token1.instance, "undeclared within scope"
                sys.exit(1)
        elif node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)

    elif node.label == "<in>":
        if var_in_scope(node.token1) == False:
            print "ERROR:", node.token1.instance, "undeclared within scope"
            sys.exit(1)

    elif node.label == "<assign>":
        if var_in_scope(node.token1) == False:
            print "ERROR:", node.token1.instance, "undeclared within scope"
            sys.exit(1)
        if node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)
    else:
        if node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)
        if node.child2 != None:
            static_semantics(node.child2, count, fout, storage_names)
        if node.child3 != None:
            static_semantics(node.child3, count, fout, storage_names)
        if node.child4 != None:
            static_semantics(node.child4, count, fout, storage_names)

def virtual_machine(node, count):
    fout = open("out.txt","w+")
    storage_names = []
    for tok in node.toks:
        instance = tok.instance
        if tok.instance[0].islower() == True and tok.instance not in storage_names:
            storage_names.append(tok.instance)
        # if tok.instance[0].isdigit() == True:
        #     print "val:", tok.instance
    print "variables:", storage_names
    static_semantics(node, count, fout, storage_names)
    fout.close() 