import ply.lex as lex

reserved_words = (
    'additionne',
    'soustrait',
    'de',
    'vaut',
    'puis',
    'afficher'
)

tokens = (
    'NUMBER',
    'ID',
    ) + tuple(map(lambda s:s.upper(), reserved_words))

literals = '.,'

def t_NUMBER(t):
    r'([0-9]*[.])?[0-9]+'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[A-Za-z]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'


def t_error(t):
    print("Illegal character'%s'"%t.value[0])
    t.lexer.skip(1)

lex.lex()

if __name__ == "__main__" :
    import sys
    prog = open(sys.argv[1] ).read()
    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break

        print("line %d : %s(%s)" % (tok.lineno, tok.type, tok.value))
