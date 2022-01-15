import AST
from AST import OpNode, addToClass
from context import Context
from functools import reduce

#  all the operation's lambdas that can be implemented
operations = {
    "additionne" : lambda x,y: x+y,
    "soustrait" : lambda x,y: x-y,
    "multiplie" : lambda x,y: x*y,
    "divise" : lambda x,y: x/y,
    "est plus grand" : lambda x,y: x>y,
    "est plus petit" : lambda x,y: x<y,
    "est plus grand que ou egal" : lambda x, y: x>=y,
    "est plus petit que ou egal" : lambda x, y: x<=y,
    "est egal a" : lambda x, y: x == y
}

types = {
    "texte" : str,
    "nombre" : float,
    "booleen" : str 
}
currentContext = Context()

functions = {} # the key is the name of the functions, 
                            # the values is:
                                # (the DefinNode
                                # the scope where the function is declared)

# to convert the string boolean value to a real boolean value
bools = {
    "vrai" : True,
    "faux" : False
}

@addToClass(AST.ProgramNode)
def execute(self):
    '''execute all the node's childrens'''
    for c in self.children:
        c.execute()

@addToClass(AST.TokenNode)
def execute(self):
    has_quote = False

    # true => can be boolean, string, or a var
    if isinstance(self.tok, str):
        # true if the first and last chars are "
        has_quote = self.tok[0] == "\"" and self.tok[-1] == "\""
        
        # check if not a boolean value
        if self.tok in bools.keys():
            return bools[self.tok]

        # if not string => it's a var
        elif not has_quote:
            try:
                # get the var's value in the current scope
                r = currentContext[self.tok]
                if r != None:
                    return r
            except KeyError:
                print("*** Error : variable %s undefined ! " % self.tok)
        # it's a string
        else:
            return self.tok[1:-1]

    return self.tok

@addToClass(AST.DefineNode)
def execute(self):
    # add the function to the dictionnary
    functions[self.name] = (self, currentContext)

@addToClass(AST.CallNode)
def execute(self):    

    # we create a new child of the context where the function has been defined
    global currentContext
    oldContext = currentContext
    currentContext = functions[self.name][1].createChildren()

    # for each arguments
    for i in range(1, len(functions[self.name][0].children)):

        # we create the var in the context by executing the assign node
        d = functions[self.name][0].children[i]
        d.execute() 
        
        # assign the right value to the arg
        currentContext[d.children[0].tok] = self.children[i-1].execute()

    # executing the function's content
    functions[self.name][0].children[0].execute()

    # return to the content where the function has been called
    currentContext = oldContext

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0, 0)
    if not isinstance(args[0], type(args[1])):
        print("*** Error : %s and %s aren't same type ! " % (self.children[0].tok, self.children[1].tok))
    else:
        # apply the operation to the arguments
        return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
    if isinstance(self.children[1], OpNode):
        # if is opNode => execute it
        value = self.children[1].execute()
    else:
        # not OpNode => it's a TokenNode => we take the value
        value = self.children[1].tok
    
    # if None => we apply the type's default value
    if value is None:
        if self.type == "texte":
            value = ""
        elif self.type == "booleen":
            value = True
        elif self.type == "nombre":
            value = 0.
    
    # check that the type matches the value
    if isinstance(value, types[self.type]):
        # true => can be boolean or string
        if isinstance(value, str):
            if value in bools.keys():
                currentContext[self.children[0].tok] = bools[value] # translate the string boolean to a real boolean
            else:
                currentContext[self.children[0].tok] = value[1:-1]  # with deleting the quotes
        # false => it's a number
        else:
            currentContext[self.children[0].tok] = value
    else:
        print("*** Error : type of %s is a %s and %s isn't ! " % (self.children[0].tok, self.type, self.children[1].tok))


@addToClass(AST.PrintNode)
def execute(self):
    # if boolean => translate the value in french
    if isinstance(self.children[0].execute(), bool):
        if self.children[0].execute():
            print("C'est vrai!")
        else:
            print("C'est faux!")
    else:
        print(self.children[0].execute())
    
@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute():
        self.children[1].execute()

@addToClass(AST.CompareNode)
def execute(self):
    if self.children[0].execute():
        self.children[1].execute()
    else:
        self.children[2].execute()


if __name__ == '__main__':
    from parseur import parse
    import sys, os

    file = sys.argv[1]
    ext = os.path.splitext(file)[1][1:]

    if ext == "oml":
        prog = open(sys.argv[1]).read()
        ast = parse(prog)
        ast.execute()
    else:
        print("Wrong extension for " + file)
        raise IOError
