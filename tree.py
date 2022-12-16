from ete3 import Tree, TreeStyle, TextFace, faces, add_face_to_node, NodeStyle, CircleFace

def parseTreeList(treeList):
    t = Tree()
    A = []
    A.append(t.add_child(name="root"))
    B = []
    C = []
    D = []
    E = []
    F = []

    size = len(treeList)
    if (size >= 1):
        level1 = treeList[0]
        value = 0
        for key in level1:
            value += (level1[key] / 1000)
            A[0].add_features(weight = value/500, level = 0)
        for index1, (key1, value1) in enumerate(level1.items()):
            label = key1 + ' -> ' +str(value1) + '  '
            size1 = ((value1 / 1000) / value) * 75
            B.append(A[0].add_child(name = label))
            B[-1].add_features(weight = size1, level = 1)
            if (size >= 2):
                level2 = treeList[1]
                for index2, (key2, value2) in enumerate(level2.items()):
                    if (key2.startswith("('" + key1)):
                        label = key2 + ' -> ' +str(value2) + '  '
                        size2 = ((value2 / 1000) / (value1 / 1000)) * 75
                        C.append(B[index1].add_child(name = label))
                        C[-1].add_features(weight = size2, level = 2)
                        if (size >= 3):
                            level3 = treeList[2]
                            for index3, (key3, value3) in enumerate(level3.items()):
                                if (key3.startswith(key2[:-1])):
                                    label = key3 + ' -> ' +str(value3) + '  '
                                    size3 = ((value3 / 1000) / (value2 / 1000)) * 75
                                    D.append(C[index2].add_child(name = label))
                                    D[-1].add_features(weight = size3, level = 3)
                                    if (size >= 4):
                                        level4 = treeList[3]
                                        for index4, (key4, value4) in enumerate(level4.items()):
                                            if (key4.startswith(key3[:-1])):
                                                label = key4 + ' -> ' +str(value4) + '  '
                                                size4 = ((value4 / 1000) / (value3 / 1000)) * 75
                                                E.append(D[index3].add_child(name = label))
                                                E[-1].add_features(weight = size4, level = 4)
                                                if (size >= 5):
                                                    level5 = treeList[4]
                                                    for index5, (key5, value5) in enumerate(level5.items()):
                                                        if (key5.startswith(key4[:-1])):
                                                            label = key5 + ' -> ' +str(value5) + '  '
                                                            size5 = ((value5 / 1000) / (value4 / 1000)) * 75
                                                            F.append(E[index4].add_child(name = label))
                                                            F[-1].add_features(weight = size5, level = 5)


    return t

def drawTree(treeList) :
    # varSize = len (treeList)
    t = parseTreeList(treeList)

    ts = TreeStyle()
    ts.root_opening_factor = 1
    ts.show_leaf_name = False
    ts. show_scale = False
    color = ["blue", "red", "green", "blue", "black", "violet"]
    def my_layout(node):
            F = TextFace(node.name, tight_text=True, fsize=20, penwidth=50)
            faces.add_face_to_node(F, node, column=0, position="branch-right")

            if "weight" in node.features:
                C = CircleFace(radius=node.weight, color=color[node.level], style="sphere")
                C.opacity = 0.5
                faces.add_face_to_node(C, node, 0, position="float")

    ts.layout_fn = my_layout

    ts.mode = "c"
    ts.arc_start = -45
    ts.arc_span = 270
    ts.branch_vertical_margin = 50

    t.render("tree.png", tree_style=ts)
