import AST
from AST import addToClass
from context import Context
from functools import reduce

operations = {
    "additionne" : lambda x,y: x+y,
    "soustrait" : lambda x,y: x-y,
    "multiplie" : lambda x,y: x*y,
    "divise" : lambda x,y: x/y
}

currentContext = Context()

functions = {} # the key is the name of the functions, 
                            # the values is:
                                # (the ProgramNode,
                                # the args names,
                                # the scope where the function is declared)



@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.TokenNode)
def execute(self):
    if isinstance(self.tok, str):
        
        r = currentContext[self.tok]
        if r != None:
            return r
        print("*** Error : variable %s undefined ! " % self.tok)
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
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
    currentContext[self.children[0].tok] = self.children[1].execute()

@addToClass(AST.PrintNode)
def execute(self):
    print(self.children[0].execute())
    
@addToClass(AST.WhileNode)
def execute(self):
    global currentContext

    currentContext = currentContext.createChildren()
    while self.children[0].execute():
        self.children[1].execute()
    currentContext = currentContext.parent

if __name__ == '__main__':
    from parser5 import parse
    import sys, os

    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    ast.execute()

