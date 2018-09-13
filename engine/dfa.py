from engine import nfamake
from graphviz import Digraph
import copy


# 通过点来构造子集
def groupnodefromnode(value, node, way='ε'):
    nodeset = list()
    if (node == 0) and way == 'ε':
        nodeset.append(node)
    for link in value.links:
        if (link[2] == way) and (link[1] not in nodeset) and (link[0] == node):
            nodeset.append(link[1])
    queue = copy.deepcopy(nodeset)
    while queue:
        item = queue.pop()
        for link in value.links:
            if (link[2] == 'ε') and (link[1] not in nodeset) and (link[0] == item):
                nodeset.append(link[1])
                queue.append(link[1])
    return nodeset


# 通过集合构建子集
def groupnodefromset(value, nodeset, way='ε'):
    newnodeset = list()
    for i in nodeset:
        temp = groupnodefromnode(value, i, way)
        for t in temp:
            if t not in newnodeset:
                newnodeset.append(t)
    queue = copy.deepcopy(newnodeset)
    while queue:
        item = queue.pop()
        for link in value.links:
            if (link[2] == 'ε') and (link[1] not in newnodeset) and (link[0] == item):
                newnodeset.append(link[1])
                queue.append(link[1])
    return newnodeset


class dfapic:
    def __init__(self):
        self.start = 0
        self.finish = list()
        self.node = list()
        self.links = list()

    #def makesimple(self):

    def dfatonfa(self, value):
        nodeset = list()
        flags = list()
        self.node.append(0)
        tempnode = groupnodefromnode(value, value.start)
        nodeset.append(tempnode)
        flags.append(True)
        for i in value.chars:
            tempnode = groupnodefromset(value, nodeset[0], i)
            if (tempnode not in nodeset) and tempnode:
                nodeset.append(tempnode)
                flags.append(False)
                self.node.append(nodeset.index(tempnode))
                self.links.append([0, self.node[-1], i])
        while False in flags:
            item = flags.index(False)
            for i in value.chars:
                tempnode = groupnodefromset(value, nodeset[item], i)
                if (tempnode not in nodeset) and tempnode:
                    nodeset.append(tempnode)
                    flags.append(False)
                    self.node.append(nodeset.index(tempnode))
                    self.links.append([item, self.node[-1], i])
                if tempnode:
                    templink = [item, nodeset.index(tempnode), i]
                    if templink not in self.links:
                        self.links.append(templink)
            flags[item] = True

        for item in self.node:
            if value.end in nodeset[item]:
                self.finish.append(item)

    def polt(self):
        dot = Digraph()
        for n in self.node:
            if n not in self.finish:
                dot.node(str(n), str(n))
            else:
                dot.node(str(n), 'f:' + str(n))
        for l in self.links:
            dot.edge(str(l[0]), str(l[1]), l[2])
        dot.view()
