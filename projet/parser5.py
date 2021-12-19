import ply.yacc as yacc
import AST
from lex5 import tokens

precedence = (
    ('left', 'OP'),
    ('left', 'ID'),
    ('left', 'VAUT')
)

operators = {
    "additionne" : lambda x,y: x+y,
    "soustrait" : lambda x,y: x-y,
    "multiplie" : lambda x,y: x*y,
    "divise" : lambda x,y: x/y
}

def p_program_sentence(p):
    'program : sentence'
    p[0] = AST.ProgramNode(p[1])

def p_program_recursive(p):
    'program : sentence program'
    p[0] = AST.ProgramNode(p[1] + p[2].children)

def p_sentence_subordinate(p):
    'sentence : subordinate "."'
    p[0] = [p[1]]

def p_sentence_recursive(p):
    '''sentence : subordinate PUIS sentence
        | subordinate "," sentence'''
    p[0] = [p[1]] + p[3]

def p_print(p):
    'print : AFFICHER expression'
    p[0] = AST.PrintNode(p[2])

def p_subordinate_assign(p):
    '''subordinate : assign
        | print'''
    p[0] = p[1]

def p_type(p):
    '''type : NOMBRE
        | TEXT
        | BOOLEEN'''
    p[0] = p[1]

def p_assign(p):
    '''assign : LE type ID VAUT expression'''
    p[0] = AST.AssignNode(p[2], AST.TokenNode(p[3]), p[5])

def p_expression_num(p):
    '''expression : NUMBER'''
    p[0] = AST.TokenNode(p[1])

def p_expression_str(p):
    '''expression : STRING'''
    p[0] = AST.TokenNode(p[1][1:-1])

def p_expression_id(p):
    'expression : ID'
    p[0] = AST.TokenNode(p[1])

def p_sentence_while(p):
    'sentence : TANT QUE expression ALORS sentence'
    p[0] = [AST.WhileNode([p[3], AST.ProgramNode(p[5])])]

def p_operator(p):
    '''operator : ADDITIONNE DE %prec OP
        | SOUSTRAIT DE %prec OP
        | MULTIPLIE PAR %prec OP
        | DIVISE PAR %prec OP'''
    p[0] = p[1]
    
def p_expression_op(p):
    'expression : expression operator expression %prec OP'
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    yacc.errok()

def parse(prog):
    return yacc.parse(prog)    

yacc.yacc(outputdir="generated", debug=False)

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1] ).read()
    result = yacc.parse(prog, debug=True)

    print(result)
    import os
    graph = result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
    graph.write_pdf(name)
    print("wrote ast to ", name)

