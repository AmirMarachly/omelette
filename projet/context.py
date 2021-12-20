class Context:

    def __init__(self):
        self.childrens = []
        self.vars = {}
        self.parent = None

    def createChildren(self):
        children = Context()
        children.parent = self
        self.childrens.append(children)
        return children

    def __setitem__(self, var, value):
        self.vars[var] = value

    def __getitem__(self, var):
        c = self
        while(c != None):
            try:
                return c.vars[var]
            except KeyError:
                pass
            c = c.parent

        return None