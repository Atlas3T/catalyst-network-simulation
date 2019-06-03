from anytree import Node, RenderTree
from anytree.exporter import DotExporter


# pip install anytree
# pip install graphviz

# example
udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)

for pre, fill, node in RenderTree(udo):
    print("%s%s" % (pre, node.name))

DotExporter(udo).to_picture("udo.png")

#main that execute


#def can you read from excel --> True


#def read from excel --> array (a,b,c,d)


#def build the tree (one per P)


