from ete3 import Tree, TreeStyle, TextFace, faces, add_face_to_node, NodeStyle, CircleFace
from PIL import Image 
import random 
import copy

def parseTreeList(treeList):
    t = Tree()
    A = []
    A.append(t.add_child(name="root"))
    B = []
    C = []
    D = []
    E = []

    size = len(treeList)
    if (size >= 1):
        level1 = treeList[0]
        value = 0
        for key in level1:
            value += (level1[key] / 1000)
            A[0].add_features(weight = value/1000)
        for index1, (key1, value1) in enumerate(level1.items()):
            label = key1 + ' -> ' +str(value1) + '  '
            size1 = ((value1 / 1000) / value) * 75
            B.append(A[0].add_child(name = label))
            B[-1].add_features(weight = size1)
            if (size >= 2):
                level2 = treeList[1]
                for index2, (key2, value2) in enumerate(level2.items()):
                    if (key2.startswith('(' + key1)):
                        label = key2 + ' -> ' +str(value2) + '  '
                        size2 = ((value2 / 1000) / (value1 / 1000)) * 75
                        C.append(B[index1].add_child(name = label))
                        C[-1].add_features(weight = size2)
                        if (size >= 3):
                            level3 = treeList[2]
                            for index3, (key3, value3) in enumerate(level3.items()):
                                if (key3.startswith(key2[:-1])):
                                    label = key3 + ' -> ' +str(value3) + '  '
                                    size3 = ((value3 / 1000) / (value2 / 1000)) * 75
                                    D.append(C[index2].add_child(name = label))
                                    D[-1].add_features(weight = size3)
                                    if (size >= 4):
                                        level4 = treeList[3]
                                        for index4, (key4, value4) in enumerate(level4.items()):
                                            if (key4.startswith(key3[:-1])):
                                                label = key4 + ' -> ' +str(value4) + '  '
                                                size4 = ((value4 / 1000) / (value3 / 1000)) * 75
                                                E.append(D[index2].add_child(name = label))
                                                E[-1].add_features(weight = size4)

    return t

def drawTree(treeList) :
    varSize = len (treeList)
    t = parseTreeList(treeList)

    ts = TreeStyle()
    ts.root_opening_factor = 1
    ts.show_leaf_name = False
    ts. show_scale = False
    def my_layout(node):
            F = TextFace(node.name, tight_text=True, fsize=20, penwidth=50)
            faces.add_face_to_node(F, node, column=0, position="branch-right")

            if "weight" in node.features:
                C = CircleFace(radius=node.weight, color="Red", style="sphere")
                C.opacity = 0.5
                faces.add_face_to_node(C, node, 0, position="float")

    ts.layout_fn = my_layout

    ts.mode = "c"
    ts.arc_start = 0
    ts.arc_span = 180
    ts.branch_vertical_margin = 50

    # for n in t.traverse():
    #     # print (n)
    #     nstyle = NodeStyle()
    #     nstyle["shape"] = "sphere"
    #     nstyle["fgcolor"] = "red"
    #     # change size based on percentage of shares
    #     nstyle["size"] = 25
    #     nstyle["vt_line_width"] = 10
    #     nstyle["hz_line_width"] = 10
    #     # nstyle["vt_line_color"] = "red"
    #     # nstyle["hz_line_color"] = "red"
    #     n.set_style(nstyle)

    colorPalette = [["#fde725", "#e3cf21", "#cab81d", "#b1a119", "#978a16", "#7e7312", "#655c0e", "#746c26"],
                     ["#a0da39", "#90c433", "#80ae2d", "#709827", "#608222", "#506d1c", "#405716", "#53672d"],
                     ["#4ac16d", "#42ad62", "#3b9a57", "#33874c", "#2c7341", "#256036", "#1d4d2b", "#335e40"], 
                     ["#1fa187", "#1b9079", "#18806c", "#15705e", "#126051", "#0f5043", "#0c4036", "#24534a"],
                     ["#277f8e", "#23727f", "#1f6571", "#1b5863", "#174c55", "#133f47", "#0f3238", "#576f73"],
                     ["#365c8d", "#30527e", "#2b4970", "#254062", "#203754", "#1b2e46", "#152438", "#5b6573"],
                     ["#46327e", "#3f2d71", "#382864", "#312358", "#2a1e4b", "#23193f", "#1c1432", "#605a6f"],
                     ["#440154", "#561a65", "#693376", "#c6b2cb", "#7c4d87", "#8e6698", "#a180a9", "#b499ba"]                  
                    ]

    def nodeColorForLevels (t):
        if (varSize >= 2):
            level1 = t.get_children()[0].get_children()
            for i in range(0, len(level1)):
                level1[i] = setColor(level1[i], colorPalette[i], i)
                if (varSize >= 3):
                    level2 = level1[i].get_children()
                    for j in range(0, len(level2)):
                        level2[j] = setColor(level2[j], colorPalette[i], j)
                        if (varSize >= 4):
                            level3 = level2[j].get_children()
                            for k in range(0, len(level3)):
                                level3[k] = setColor(level3[k], colorPalette[i], k)
                                if (varSize >= 5):
                                    level4 = level3[k].get_children()
                                    for l in range(0, len(level4)):
                                        level4[l] = setColor(level4[l], colorPalette[i], l)

    def setColor(node, colorPalette, i):
        nstyle = NodeStyle()
        nstyle["shape"] = "sphere"
        nstyle["fgcolor"] = "White"
        # change size based on percentage of shares
        nstyle["size"] = 5
        nstyle["bgcolor"] = colorPalette[i]
        node.set_style(nstyle)

        nstyle["vt_line_width"] = 5
        nstyle["hz_line_width"] = 5
        # nstyle["vt_line_color"] = "White"
        # nstyle["hz_line_color"] = "White"
        return node
                    
        print ("here")
    # nodeColorForLevels(t)
    t.render("tree.png", tree_style=ts)
    # t.show(tree_style=ts)
    print ("here")

# drawTree()
