import AST
from AST import addToClass
from functools import reduce

operations = {
    '+': 'ADD',
    '-': 'SUB',
    '*': 'PRODUCT',
    '/': 'DIVIDE'
}

i = 1

@addToClass(AST.ProgramNode)
def compile(self):
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode

@addToClass(AST.TokenNode)
def compile(self):
    bytecode = ""
    if isinstance(self.tok, str):
        bytecode += "PUSHV %s\n" % self.tok
    else:
        bytecode += "PUSHC %s\n" % self.tok

    return bytecode

@addToClass(AST.OpNode)
def compile(self):
    bytecode = ""
    bytecode += ''.join([c.compile() for c in self.children])
    if len(self.children) == 1:
        bytecode += "PUSHC 0.0"

    bytecode += operations[self.op] + "\n"
    return bytecode

@addToClass(AST.AssignNode)
def compile(self):
    bytecode = ""
    bytecode += self.children[1].compile()
    bytecode += "SET %s\n" % self.children[0].tok
    return bytecode

@addToClass(AST.PrintNode)
def compile(self):
    bytecode = ""
    bytecode += self.children[0].compile()
    bytecode += "PRINT\n"
    return bytecode

@addToClass(AST.WhileNode)
def compile(self):
    bytecode = ""
    condEt = "cond" + str(i)
    bodyEt = "body" + str(i)

    bytecode += "JMP " + condEt + "\n"
    bytecode += bodyEt + ":"
    bytecode += self.children[1].compile()

    bytecode += condEt + ":"
    bytecode += self.children[0].compile()
    bytecode += "JINZ " + bodyEt

    return bytecode

if __name__ == '__main__':
    from parser5 import parse
    from threader import thread
    import sys
    import os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)
    compiled = ast.compile()

    name = os.path.splitext(sys.argv[1])[0]+'.vm'
    outfile = open(name, 'w')
    outfile.write(compiled)
    outfile.close()
    print("Wrote o u t p u t t o " , name)