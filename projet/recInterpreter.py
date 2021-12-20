import AST
from AST import OpNode, addToClass
from functools import reduce

operations = {
    "additionne" : lambda x,y: x+y,
    "soustrait" : lambda x,y: x-y,
    "multiplie" : lambda x,y: x*y,
    "divise" : lambda x,y: x/y,
    "est plus grand" : lambda x,y: x>y,
    "est plus petit" : lambda x,y: x<y,
    "est moins grand" : lambda x,y: x<y,
    "est moins petit" : lambda x,y: x>y,
    "est plus grand que ou egal" : lambda x, y: x>=y,
    "est plus petit que ou egal" : lambda x, y: x<=y,
    "est egal a" : lambda x, y: x == y
}

types = {
    "text" : str,
    "nombre" : float,
    "booleen" : str 
}

bools = {
    "vrai" : True,
    "faux" : False
}

vars = {}

@addToClass(AST.ProgramNode)
def execute(self):
    # print("program")
    for c in self.children:
        c.execute()


@addToClass(AST.TokenNode)
def execute(self):
    # print("token")
    has_quote = False
    if isinstance(self.tok, str):
        has_quote = self.tok[0] == "\"" and self.tok[-1] == "\""
        if self.tok in bools.keys():
            return bools[self.tok]
        if not has_quote:
            try:
                return vars[self.tok]
            except KeyError:
                #TODO
                print("*** Error : variable %s undefined ! " % self.tok)
    if has_quote:
        return self.tok[1:-1]
    else:
        return self.tok


@addToClass(AST.OpNode)
def execute(self):
    # print("opnode")
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    if not isinstance(args[0], type(args[1])):
        print("*** Error : %s and %s aren't same type ! " % (self.children[0].tok, self.children[1].tok))
    else:
        return reduce(operations[self.op], args)


@addToClass(AST.AssignNode)
def execute(self):
    # print("assign")
    if isinstance(self.children[1], OpNode):
        value = self.children[1].execute()
    else:
        value = self.children[1].tok
    if isinstance(value, types[self.type]):
        if isinstance(value, str):
            if value in bools.keys():
                vars[self.children[0].tok] = bools[value]
            else:
                vars[self.children[0].tok] = value
        else:
            vars[self.children[0].tok] = value
    else:
        print("*** Error : type of %s isn't right ! " % self.children[0].tok)


@addToClass(AST.PrintNode)
def execute(self):
    # print("print")
    if isinstance(self.children[0].execute(), bool):
        if self.children[0].execute():
            print("C'est vrai!")
        else:
            print("C'est faux!")
    else:
        print(self.children[0].execute())


@addToClass(AST.WhileNode)
def execute(self):
    # print("while")
    while self.children[0].execute():
        self.children[1].execute()


@addToClass(AST.CompareNode)
def execute(self):
    # print("compare")
    if self.children[0].execute():
        self.children[1].execute()
    else:
        self.children[2].execute()


if __name__ == '__main__':
    from parser5 import parse
    import sys, os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    ast.execute()

