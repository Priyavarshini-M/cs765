from ete3 import Tree, TreeStyle, TextFace, add_face_to_node
from PIL import Image  

variables = [['age', 3], ['gender', 2], ['emp', 5], ['sports', 24]]
labels = [['g1', 'g2', 'g3'], ['M', 'F'], ['type1', 'type2', 'type3', 'type4','type5'],
['s1', 's2', 's3']]
varSize = len(variables)
print (varSize)

def createNextLevel(prevLevelLength, prevLevel, root):
    nodeList = []
    for i in range (0, prevLevelLength):
        for j in range(0, variables[prevLevel][1]):
            nodeList.append(root[i]
                .add_child(name=labels[prevLevel][j]))
    print (nodeList)
    return nodeList

t = Tree()
A = []
A.append(t.add_child(name=variables[0][0]))
if (varSize >= 2):
    B = createNextLevel(len(A), 0, A)
    if (varSize >= 3):
        C = createNextLevel(len(B), 1, B)
        if (varSize >= 4):
            D = createNextLevel(len(C), 2, C)
            if (varSize >= 5):
                E = createNextLevel(len(D), 3, C)

print (t.get_ascii(show_internal=True))


ts = TreeStyle()
ts.show_leaf_name = True
ts.show_leaf_name = False
def my_layout(node):
        F = TextFace(node.name, tight_text=True)
        add_face_to_node(F, node, column=0, position="branch-right")
ts.layout_fn = my_layout

t.render("mytree.png", tree_style=ts)

#  
