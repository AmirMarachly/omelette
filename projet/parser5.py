import ply.yacc as yacc
import AST
from lex5 import tokens

vars = {}

precedence = (
    ('left', 'OP'),
    ('left', 'ID'),
    ('left', 'VAUT')
)

operators = {
    "additionne" : lambda x,y: x+y,
    "soustrait" : lambda x,y: x-y
}

def p_program_sentence(p):
    'program : sentence'
    p[0] = AST.ProgramNode(p[1])

def p_program_recursive(p):
    'program : sentence program'
    p[0] = AST.ProgramNode([p[1]] + p[2].children)

def p_sentence_subordinate(p):
    'sentence : subordinate "."'
    p[0] = p[1]

def p_sentence_recursive(p):
    '''sentence : subordinate PUIS sentence
        | subordinate "," sentence'''
    #A MODIFIER
    p[0] = AST.ProgramNode([p[1]] + p[3].children)

def p_print(p):
    'print : AFFICHER expression'
    p[0] = AST.PrintNode(p[2])

def p_subordinate_assign(p):
    '''subordinate : assign
        | print'''
    p[0] = p[1]

def p_assign(p):
    'assign : ID VAUT expression'
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])

def p_expression_num(p):
    '''expression : NUMBER'''
    p[0] = AST.TokenNode(p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = AST.TokenNode(p[1])

def p_operator(p):
    '''operator : ADDITIONNE DE %prec OP
        | SOUSTRAIT DE %prec OP'''
    p[0] = p[1]
    
def p_expression_op(p):
    'expression : expression operator expression %prec OP'
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    yacc.errok()

yacc.yacc(outputdir="generated")

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1] ).read()
    result = yacc.parse(prog)

    print(result)
    import os
    graph = result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
    graph.write_pdf(name)
    print("wrote ast to ", name)

