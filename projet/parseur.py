import ply.yacc as yacc
import AST
from lex import tokens

precedence = (
    ('left', 'OP'),
    ('left', 'ID'),
    ('left', 'VAUT'),
    ('left', 'SI')
)

operators = {
    "additionne" : lambda x,y: x+y,
    "soustrait" : lambda x,y: x-y,
    "multiplie" : lambda x,y: x*y,
    "divise" : lambda x,y: x/y,
    "egal" : lambda x,y: x == y,
    "plus grand" : lambda x,y: x>y,
    "plus petit" : lambda x,y: x<y,
    "moins grand" : lambda x,y: x<y,
    "moins petit" : lambda x,y: x>y,
    "plus grand que ou egal" : lambda x, y: x>=y,
    "plus petit que ou egal" : lambda x, y: x<=y
}

### A program is serie of sentences
def p_program_sentence(p):
    'program : sentence'
    p[0] = AST.ProgramNode(p[1])

def p_program_recursive(p):
    'program : sentence program'
    p[0] = AST.ProgramNode(p[1] + p[2].children)

### A sentence is a list of subordinates.
def p_sentence_subordinate(p):
    'sentence : subordinate "."'
    p[0] = [p[1]]

def p_sentence_recursive(p):
    '''sentence : subordinate PUIS sentence
        | subordinate "," sentence'''
    p[0] = [p[1]] + p[3]

def p_subordinate_assign(p):
    '''subordinate : assign
        | print'''
    p[0] = p[1]

def p_print(p):
    'print : AFFICHER expression'
    p[0] = AST.PrintNode(p[2])
    

### A function is a sentence executed when called with specifics arguments
def p_args(p):
    'args : LE type ID'
    p[0] = [AST.AssignNode(p[2], AST.TokenNode(p[3]), AST.TokenNode(None))]

def p_args_rec(p):
    'args : LE type ID args'
    p[0] = [AST.AssignNode(p[2], AST.TokenNode(p[3]), AST.TokenNode(None))] + p[4]

def p_definefunction(p):
    '''sentence : DEFINIR ID AVEC args ":" sentence'''
    p[0] = [AST.DefineNode(p[2], [AST.ProgramNode(p[6])] + p[4])]

def p_callargs_expression(p):
    '''callargs : expression'''
    p[0] = [p[1]]

def p_callargs_rec(p):
    '''callargs : expression callargs'''
    p[0] = [p[1]] + p[2]

def p_callfunction(p):
    '''subordinate : APPELER ID AVEC callargs'''
    p[0] = AST.CallNode(p[2], p[4])

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
    p[0] = AST.TokenNode(p[1])

def p_expression_bool(p):
    '''expression : VRAI
        | FAUX'''
    p[0] = AST.TokenNode(p[1])

def p_expression_id(p):
    'expression : ID'
    p[0] = AST.TokenNode(p[1])


def p_sentence_while(p):
    'sentence : TANT QUE expression ALORS sentence'
    p[0] = [AST.WhileNode([p[3], AST.ProgramNode(p[5])])]


def p_sentence_compare(p):
    '''sentence : SI expression ALORS sentence SINON sentence'''
    p[0] = [AST.CompareNode([p[2], AST.ProgramNode(p[4]), AST.ProgramNode(p[6])])]


def p_operator(p):
    '''operator : ADDITIONNE DE %prec OP
        | SOUSTRAIT DE %prec OP
        | MULTIPLIE PAR %prec OP
        | DIVISE PAR %prec OP'''
    p[0] = p[1]


def p_operator_comparator(p):
    '''operator : EST PLUS GRAND QUE
    | EST PLUS PETIT QUE
    | EST EGAL A'''
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3]


def p_operator_comparator_equal(p):
    '''operator : EST PLUS GRAND QUE OU EGAL
    | EST PLUS PETIT QUE OU EGAL
    | EST MOINS GRAND QUE OU EGAL
    | EST MOINS PETIT QUE OU EGAL'''
    p[0] = p[1] + ' ' + p[2] + ' ' + p[3] + ' ' + p[4] + ' ' + p[5] + ' ' + p[6] 


def p_sentence_nothing(p):
    '''sentence : RIEN "." '''
    p[0] = AST.ProgramNode()


def p_expression_op(p):
    '''expression : expression operator expression %prec OP'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])
    

def p_error(p):
    print("Syntax error in line %d" % p.lineno)
    # yacc.errok()


def parse(prog):
    return yacc.parse(prog)


yacc.yacc(outputdir="generated", debug=False)

if __name__ == "__main__":
    import sys
    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog, debug=1)

    print(result)
    import os
    graph = result.makegraphicaltree()
    name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
    graph.write_pdf(name)
    print("wrote ast to ", name)

