import sys, os
import collections

import node
import token
import scanner

tk = token.Token()
de_tokens = collections.deque()
line_list = collections.deque()

def fetch_tokens(fn):
    line_number = 1
    with open(fn) as fp:
        while True:
            tk, line_number = scanner.driver(fp, line_number)
            de_tokens.append(tk)
            line_list.append(line_number)
            if tk.identity == token.token_ids.token_names[35]: 
                print fn, 'scanned without error...'
                break
            if tk.identity == token.token_ids.token_names[36]: 
                break  

def fetch_node(datum):
    this_node = node.Node()
    this_node.label = datum
    return this_node

def lookahead(token_list):
    return token_list[0].identity

def error(expected, received):
    print "ERROR: expected", expected, "but received", received
    sys.exit(1)

# <assign> -> Identifier < < <expr> 
def assign():
    if lookahead(de_tokens) == "ID_tk":
        np = fetch_node("<assign>")
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        if lookahead(de_tokens) == "LT_tk":
            tk = de_tokens.popleft()
            (np.toks).append(tk)
            np.token2 = tk
            if lookahead(de_tokens) == "LT_tk":
                tk = de_tokens.popleft()
                (np.toks).append(tk)
                np.token3 = tk
                np.child1 = expr()
                return np
            else:
                error("LT_tk", lookahead(de_tokens))
        else:
            error("LT_tk", lookahead(de_tokens))
    else:
        error("ID_tk", lookahead(de_tokens))

# <if> -> cond ( ( <expr> <RO> <expr> ) ) <stat>
def cond():
    if lookahead(de_tokens) == "COND_tk":
        np = fetch_node("<if>")
        tk = de_tokens.popleft()
        if lookahead(de_tokens) == "LPAREN_tk":
            tk = de_tokens.popleft()
            (np.toks).append(tk)
            np.token1 = tk
            if lookahead(de_tokens) == "LPAREN_tk":
                tk = de_tokens.popleft()
                (np.toks).append(tk)
                np.token2 = tk
                np.child1 = expr()
                np.child2 = RO()
                np.child3 = expr()
                if lookahead(de_tokens) == "RPAREN_tk":
                    tk = de_tokens.popleft()
                    (np.toks).append(tk)
                    np.token3 = tk
                    if lookahead(de_tokens) == "RPAREN_tk":
                        tk = de_tokens.popleft()
                        (np.toks).append(tk)
                        np.token4 = tk
                        np.child4 = stat()
                        return np
                    else:
                        error("RPAREN_tk", lookahead(de_tokens))
                else:
                    error("RPAREN_tk", lookahead(de_tokens))
            else:
                error("LPAREN_tk", lookahead(de_tokens))
        else:
            error("LPAREN_tk", lookahead(de_tokens))
    else:
        error("COND_tk", lookahead(de_tokens))


# <loop> -> iterate ( ( <expr> <RO> <expr> ) ) <stat>
def loop():
    if lookahead(de_tokens) == "ITER_tk":
        np = fetch_node("<loop>")
        tk = de_tokens.popleft()
        if lookahead(de_tokens) == "LPAREN_tk":
            tk = de_tokens.popleft()
            (np.toks).append(tk)
            np.token1 = tk
            if lookahead(de_tokens) == "LPAREN_tk":
                tk = de_tokens.popleft()
                (np.toks).append(tk)
                np.token2 = tk
                np.child1 = expr()
                np.child2 = RO()
                np.child3 = expr()
                if lookahead(de_tokens) == "RPAREN_tk":
                    tk = de_tokens.popleft()
                    (np.toks).append(tk)
                    np.token3 = tk
                    if lookahead(de_tokens) == "RPAREN_tk":
                        tk = de_tokens.popleft()
                        (np.toks).append(tk)
                        np.token4 = tk
                        np.child4 = stat()
                        return np
                    else:
                        error("RPAREN_tk", lookahead(de_tokens))
                else:
                    error("RPAREN_tk", lookahead(de_tokens))
            else:
                error("LPAREN_tk", lookahead(de_tokens))
        else:
            error("LPAREN_tk", lookahead(de_tokens))
    else:
        error("ITER_tk", lookahead(de_tokens))

# <RO> -> < | < < | > | > > | = | < > 
def RO():
    np = fetch_node("<RO>")
    if lookahead(de_tokens) == "LT_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        if lookahead(de_tokens) == "LT_tk":
            tk = de_tokens.popleft()
            (np.toks).append(tk)
            np.token2 = tk
            return np
        elif lookahead(de_tokens) == "GT_tk":
            tk = de_tokens.popleft()
            (np.toks).append(tk)
            np.token2 = tk
            return np
        else:
            return np
    elif lookahead(de_tokens) == "GT_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        if lookahead(de_tokens) == "GT_tk":
            tk = de_tokens.popleft()
            (np.toks).append(tk)
            np.token2 = tk
            return np
        else:
            return np
    elif lookahead(de_tokens) == "ASSIGN_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        return np
    else:
        error("LT_tk or GT_tk or ASSIGN_tk", lookahead(de_tokens))
        
# <R> -> [ <expr> ] | Identifier | Integer
def R():
    np = fetch_node("<R>")
    if lookahead(de_tokens) == "LBRACKET_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        np.child1 = expr()
        if lookahead(de_tokens) == "RBRACKET_tk":
            tk = de_tokens.popleft()
            (np.toks).append(tk)
            np.token2 = tk
            return np
        else:
            error("RBRACKET_tk", lookahead(de_tokens))
    elif lookahead(de_tokens) == "ID_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        return np
    elif lookahead(de_tokens) == "INT_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        return np
    else:
        error("ID_tk, INT_tk, or LBRACKET_tk", lookahead(de_tokens))

# <M> -> - <M> | <R>
def M():
    np = fetch_node("<M>")
    if lookahead(de_tokens) == "MINUS_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        np.child1 = M()
        return np
    else:
        np.child1 = R()
        return np   

# <N> -> <M> / <N> | <M> * <N> | <M>
def N():
    np = fetch_node("<N>")
    np.child2 = M()
    if lookahead(de_tokens) == "FSLASH_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        np.child3 = N()
        return np
    elif lookahead(de_tokens) == "ASTERISK_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        np.child3 = N()
        return np
    else:
        return np

# <A> -> <N> - <A> | <N>
def A():
    np = fetch_node("<A>")
    np.child1 = N()
    if lookahead(de_tokens) == "MINUS_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        np.child2 = A()
        return np
    else:
        return np

# <expr> -> <A> + <expr> | <A>
def expr():
    np = fetch_node("<expr>")
    np.child1 = A()
    if lookahead(de_tokens) == "PLUS_tk":
        tk = de_tokens.popleft()
        (np.toks).append(tk)
        np.token1 = tk
        np.child2 = expr()
        return np
    else:
        return np
        
# <out> -> out <expr>
def out():
    if lookahead(de_tokens) == "OUT_tk":
        np = fetch_node("<out>")
        tk = de_tokens.popleft()
        np.child1 = expr()
        return np
    else:
        error("OUT_tk", lookahead(de_tokens))

# <in> -> in Identifier
def ins():
    if lookahead(de_tokens) == "IN_tk":
        tk = de_tokens.popleft()
        if lookahead(de_tokens) == "ID_tk":
            np = fetch_node("<in>")
            tk = de_tokens.popleft()
            (np.toks).append(tk)
            np.token1 = tk
            return np
        else:
            error("ID_tk", lookahead(de_tokens))
    else:
        error("IN_tk", lookahead(de_tokens))

# <stat> -> <in> | <out> | <block> | <if> | <loop> | <assign>
def stat():
    np = fetch_node("<stat>")
    if lookahead(de_tokens) == "IN_tk":
        np.child1 = ins()
        return np
    elif lookahead(de_tokens) == "OUT_tk":
        np.child1 = out()
        return np
    elif lookahead(de_tokens) == "START_tk":       
        np.child1 = block()  
        return np
    elif lookahead(de_tokens) == "COND_tk":
        np.child1 = cond()
        return np
    elif lookahead(de_tokens) == "ITER_tk":
        np.child1 = loop()
        return np
    elif lookahead(de_tokens) == "ID_tk":
        np.child1 = assign()
        return np
    else:
        error("IN_tk, OUT_tk, START_tk, COND_tk, ITER_tk, or ID_tk", lookahead(de_tokens))

# <mStat> -> empty | <stat> ; <mStat>
def mstat():
    np = fetch_node("<mstat>")
    if lookahead(de_tokens) == 'ID_tk' or lookahead(de_tokens) == 'IN_tk' or lookahead(de_tokens) == 'OUT_tk' or lookahead(de_tokens) == 'START_tk' or lookahead(de_tokens) == 'COND_tk' or lookahead(de_tokens) == 'ITER_tk' or lookahead(de_tokens) == 'ASSIGN_tk':
        np.child1 = stat()
        if lookahead(de_tokens) == "SEMICOLON_tk":
            tk = de_tokens.popleft()
            np.child2 = mstat()
            return np
        else:
            error("SEMICOLON_tk", lookahead(de_tokens))
    else:
        return None

# <stats> -> <stat> ; <mStat>
def stats():
    np = fetch_node("<stats>")
    np.child1 = stat()
    if lookahead(de_tokens) == "SEMICOLON_tk":
        tk = de_tokens.popleft()
        np.child2 = mstat()
        return np
    else:
        error("SEMICOLON_tk", lookahead(de_tokens))

# <block> -> start <vars> <stats> stop
def block():
    np = fetch_node("<block>")
    if lookahead(de_tokens) == "START_tk":
        tk = de_tokens.popleft()
        np.child1 = vars()
        np.child2 = stats()
        if lookahead(de_tokens) == "STOP_tk":
            tk = de_tokens.popleft()
            return np
        else:
            error("STOP_tk", lookahead(de_tokens))
    else:
        error("START_tk", lookahead(de_tokens)) 

# <vars> -> empty | var Identifier : Integer <vars>
def vars():
    if lookahead(de_tokens) == "VAR_tk":
        np = fetch_node("<vars>")
        tk = de_tokens.popleft()
        if lookahead(de_tokens) == "ID_tk":
            tk = de_tokens.popleft()
            (np.toks).append(tk)
            np.token1 = tk
            if lookahead(de_tokens) == "COLON_tk":
                tk = de_tokens.popleft()
                if lookahead(de_tokens) == "INT_tk":
                    tk = de_tokens.popleft()
                    (np.toks).append(tk)
                    np.token2 = tk
                    np.child1 = vars()
                    return np
                else:
                    error("INT_tk", lookahead(de_tokens))
            else:
                error("COLON_tk", lookahead(de_tokens))
        else:
            error("ID_tk", lookahead(de_tokens))
    else:
        return None

# <program> -> <vars> <block>
def program(fn):
    np = fetch_node("<program>")
    np.child1 = vars()
    np.child2 = block()
    if lookahead(de_tokens) == "EOF_tk":
        print fn, "parsed without error..."  
    else:
        error("EOF_tk", lookahead(de_tokens))
    return np

def parser(fn):
    fetch_tokens(fn)
    root = node.Node()
    root = program(fn)
    return root