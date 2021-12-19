import AST
from AST import addToClass
from functools import reduce

operations = {
    "additionne" : lambda x,y: x+y,
    "soustrait" : lambda x,y: x-y,
    "multiplie" : lambda x,y: x*y,
    "divise" : lambda x,y: x/y
}

types = {
    "text" : str,
    "nombre" : float,
    "booleen" : bool 
}

vars = {}


@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()


@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            #TODO
            print("*** Error : variable %s undefined ! " % self.tok)
    return self.tok


@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    if not isinstance(args[0], type(args[1])):
        print("*** Error : %s and %s aren't same type ! " % (self.children[0].tok, self.children[1].tok))
    else:
        return reduce(operations[self.op], args)


@addToClass(AST.AssignNode)
def execute(self):
    if isinstance(self.children[1].tok, types[self.type]):
        if isinstance(self.children[1].tok, str):
            vars[self.children[0].tok] = self.children[1].tok
        else:
            vars[self.children[0].tok] = self.children[1].execute()
    else:
        print("*** Error : type of %s isn't right ! " % self.children[0].tok)


@addToClass(AST.PrintNode)
def execute(self):
    print(self.children[0].execute())


@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()


if __name__ == '__main__':
    from parser5 import parse
    import sys, os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    ast.execute()

