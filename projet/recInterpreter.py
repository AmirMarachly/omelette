import AST
from AST import OpNode, addToClass
from context import Context
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
currentContext = Context()

functions = {} # the key is the name of the functions, 
                            # the values is:
                                # (the ProgramNode,
                                # the args names,
                                # the scope where the function is declared)


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
                r = currentContext[self.tok]
                if r != None:
                    return r
            except KeyError:
                print("*** Error : variable %s undefined ! " % self.tok)
    if has_quote:
        return self.tok[1:-1]
        
    return self.tok

@addToClass(AST.DefineNode)
def execute(self):
    functions[self.name] = (self.children[0], self.args, currentContext)

@addToClass(AST.CallNode)
def execute(self):
    argsNames = functions[self.name][1]
    argsValues = [i.execute() for i in self.args]
    d = dict(zip(argsNames,argsValues))

    #context.insert(0,d)
    global currentContext
    oldContext = currentContext
    currentContext = functions[self.name][2].createChildren()
    for k,v in d.items():
        currentContext[k] = v

    functions[self.name][0].execute()

    currentContext = oldContext
    #del context[0]

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
                currentContext[self.children[0].tok] = bools[value]
            else:
                currentContext[self.children[0].tok] = value
        else:
            currentContext[self.children[0].tok] = value
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
    global currentContext

    currentContext = currentContext.createChildren()
    while self.children[0].execute():
        self.children[1].execute()
    currentContext = currentContext.parent

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

