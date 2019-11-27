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
        self.temps = ["" for _ in range(100)]
s = S()

scope = [token.Token() for _ in range(100)]

def fetch_temp():
    temp = "Temp" + str(s.temp_count + 1)
    s.temps[s.temp_count] = temp
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
        fout.write("PUSH\n")
        s.scope_size = s.scope_size + 1

def scope_pop(scope_start, fout): 
    for i in xrange(s.scope_size, scope_start, -1):
        s.scope_size = s.scope_size - 1
        scope[i].instance = ""
        fout.write("POP\n")

def scope_find(tk):
    for i in xrange(s.scope_size, s.scope_start - 1, -1):
        if scope[i-1].instance == tk.instance:
            s.offset = s.scope_size - i
            return s.offset
    return -1

def var_in_scope(tk):
    for i in xrange(s.scope_size - 1, -1, -1):
        if scope[i].instance == tk.instance:
            return i
    return -1

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
        for temp_variable in s.temps:
            if temp_variable != "":
                fout.write(temp_variable + "\n")


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
                temp_variable = fetch_temp()
                fout.write("STORE " + temp_variable + "\n")
            if node.child2 != None:
                static_semantics(node.child2, count, fout, storage_names)
        elif node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)

    elif node.label == "<A>":
        if node.token1.identity == "MINUS_tk":
            if node.child2 != None:
                static_semantics(node.child2, count, fout, storage_names)
            temp_variable = fetch_temp()
            fout.write("STORE " + temp_variable + "\n")
            if node.child1 != None:
                static_semantics(node.child1, count, fout, storage_names)
            fout.write("SUB " + temp_variable + "\n")
        elif node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)


    elif node.label == "<N>":
        if node.token1.identity == "FSLASH_tk":
            if node.child2 != None:
                static_semantics(node.child2, count, fout, storage_names)
            temp_variable = fetch_temp()
            fout.write("STORE " + temp_variable + "\n")
            if node.child1 != None:
                static_semantics(node.child1, count, fout, storage_names)
            fout.write("DIV " + temp_variable + "\n")
        elif node.token1.identity == "ASTERISK_tk":
            if node.child2 != None:
                static_semantics(node.child2, count, fout, storage_names)
            temp_variable = fetch_temp()
            fout.write("STORE " + temp_variable + "\n")
            if node.child1 != None:
                static_semantics(node.child1, count, fout, storage_names)
            fout.write("MULT " + temp_variable + "\n")
        elif node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)


    elif node.label == "<M>":
        if node.token1.identity == "MINUS_tk":
            if node.child1 != None:
                static_semantics(node.child1, count, fout, storage_names)
            fout.write("MULT -1\n")
        else:
            if node.child1 != None:
                static_semantics(node.child1, count, fout, storage_names)


    elif node.label == "<R>":
        if node.token1.identity == "ID_tk":
            var_location = var_in_scope(node.token1)
            if var_location == -1:
                print "ERROR:", node.token1.instance, "undeclared within scope"
                sys.exit(1)
            fout.write("STACKR " + str(var_location) + "\n")
        elif node.token1.identity == "INT_tk":
            fout.write("LOAD " + node.token1.instance + "\n")
        elif node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)


    elif node.label == "<in>":
        var_location = var_in_scope(node.token1)
        if var_location == -1:
            print "ERROR:", node.token1.instance, "undeclared within scope"
            sys.exit(1)
        else:
            temp_variable = fetch_temp()
            fout.write("READ " + temp_variable + "\n")
            fout.write("LOAD " + temp_variable + "\n")
            fout.write("STACKW " + str(var_location) + "\n")

    
    elif node.label == "<out>":
        if node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)
        temp_variable = fetch_temp()
        fout.write("STORE " + temp_variable + "\n")
        fout.write("WRITE " + temp_variable + "\n")


    elif node.label == "<loop>":
        relational_operator1 = node.child2.token1.identity
        relational_operator2 = node.child2.token2.identity
        temp_variable = fetch_temp()
        begin_label = fetch_label()
        cease_label = fetch_label()
        fout.write(begin_label + ": NOOP\n")
        if node.child3 != None:
            static_semantics(node.child3, count, fout, storage_names)
        fout.write("STORE " + temp_variable + "\n")
        if node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)
        fout.write("SUB " + temp_variable + "\n")
        if relational_operator1 == "GT_tk":
            if relational_operator2 == "ASSIGN_tk":
                fout.write("BRNEG " + cease_label + "\n")
            else:
                fout.write("BRZNEG " + cease_label + "\n")
        elif relational_operator1 == "LT_tk":
            if relational_operator2 == "ASSIGN_tk":
                fout.write("BRPOS " + cease_label + "\n")
            else:
                fout.write("BRZPOS " + cease_label + "\n")
        elif relational_operator1 == "ASSIGN_tk":
            if relational_operator2 == "ASSIGN_tk":
                fout.write("BRZERO " + cease_label + "\n")
            else:
                fout.write("BRPOS " + cease_label + "\n")
                fout.write("BRNEG " + cease_label + "\n")
        if node.child4 != None:
            static_semantics(node.child4, count, fout, storage_names)
        fout.write("BR " + begin_label + "\n")
        fout.write(cease_label + ": NOOP\n")


    elif node.label == "<if>":
        relational_operator1 = node.child2.token1.identity
        relational_operator2 = node.child2.token2.identity
        if node.child3 != None:
            static_semantics(node.child3, count, fout, storage_names)
        temp_variable = fetch_temp()
        fout.write("STORE " + temp_variable + "\n")
        if node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)
        fout.write("SUB " + temp_variable + "\n")
        cond_label = fetch_label()
        if relational_operator1 == "GT_tk":
            if relational_operator2 == "ASSIGN_tk":
                fout.write("BRNEG " + cond_label + "\n")
            else:
                fout.write("BRZNEG " + cond_label + "\n")
        elif relational_operator1 == "LT_tk":
            if relational_operator2 == "ASSIGN_tk":
                fout.write("BRPOS " + cond_label + "\n")
            else:
                fout.write("BRZPOS " + cond_label + "\n")
        elif relational_operator1 == "ASSIGN_tk":
            if relational_operator2 == "ASSIGN_tk":
                fout.write("BRZERO " + cond_label + "\n")
            else:
                fout.write("BRPOS " + cond_label + "\n")
                fout.write("BRNEG " + cond_label + "\n")
        if node.child4 != None:
            static_semantics(node.child4, count, fout, storage_names)
        fout.write(cond_label + ": NOOP\n")


    elif node.label == "<assign>":
        var_location = var_in_scope(node.token1)
        if var_location == -1:
            print "ERROR:", node.token1.instance, "undeclared within scope"
            sys.exit(1)
        if node.child1 != None:
            static_semantics(node.child1, count, fout, storage_names)
        fout.write("STACKW " + str(var_location) + "\n")
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
    static_semantics(node, count, fout, storage_names)
    fout.close() 