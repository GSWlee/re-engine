from graphviz import Digraph


class nfapic:
    def __init__(self, value):
        self.start = 0
        self.end = 1
        self.node = [0, 1]
        self.links = [[0, 1, value]]

    def getnextcahr(self, value):
        index = self.node[len(self.node) - 1] + 1
        self.end = index
        self.node.append(index)
        self.links.append([index - 1, index, value])

    def caseone(self):
        # char==*
        for i in range(len(self.node)):
            self.node[i] += 1
        for l in self.links:
            l[0] += 1
            l[1] += 1
        self.node.insert(0, 0)
        self.node.append(self.node[-1] + 1)
        print(self.links)
        self.links.append([0, 1, 'ε'])
        self.links.append([self.node[-2], self.node[-1], 'ε'])
        self.links.append([self.node[0], self.node[-1], 'ε'])
        self.links.append([self.node[-2], self.node[1], 'ε'])

    def addnfa(self, value):
        # 两个nfa的连接
        tempnode = value.node
        templinks = value.links
        for i in range(len(tempnode)):
            tempnode[i] += self.node[-1]
        for l in templinks:
            l[0] += self.node[-1]
            l[1] += self.node[-1]
        self.node.extend(tempnode)
        self.links.extend(templinks)
        self.end = self.node[-1]

    def plot(self):
        dot = Digraph()
        for n in self.node:
            dot.node(str(n), str(n))
        for l in self.links:
            dot.edge(str(l[0]), str(l[1]), l[2])
        dot.view()
