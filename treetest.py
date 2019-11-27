import node

labels = [
    "<program>",
    "<vars>",
    "<block>",
    "<stats>",
    "<mstat>",
    "<stat>",
    "<in>",
    "<out>",
    "<expr>",
    "<A>",
    "<N>",
    "<M>",
    "<R>",
    "<RO>",
    "<loop>",
    "<if>",
    "<assign>",
]

def printing(root, level):
    if root == None:
        return
    else:
        i = 0
        print "\n",
        while i < level:
            print " ",
            i = i + 1
        
        level = level + 1
        print root.label, " ",

        if root.token1.instance != None:
            print root.token1.instance, " ",
        if root.token2.instance != None: 
            print root.token2.instance, " ",
        if root.token3.instance != None: 
            print root.token3.instance, " ",
        if root.token4.instance != None: 
            print root.token4.instance, " ",

        if root.child1 != None:
            printing(root.child1, level)
        if root.child2 != None:
            printing(root.child2, level)
        if root.child3 != None:
            printing(root.child3, level)
        if root.child4 != None:
            printing(root.child4, level)