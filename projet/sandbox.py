from context import Context

c1 = Context()



c1["test"] = 3

c2 = c1.createChildren()

print(c2["test"])