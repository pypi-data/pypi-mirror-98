"""An optimized implementation of Suffix-Tree.
https://github.com/kasramvd/SuffixTree
Algo description best: https://stackoverflow.com/questions/9452701/ukkonens-suffix-tree-algorithm-in-plain-english
"""

# For more infor about the comments you can read http://web.stanford.edu/~mjkay/gusfield.pdf
from operator import attrgetter

leafEnd = -1


class Node:
    def __init__(self, leaf):
        # self.__identifier = identifier
        self.children = {}
        # for leaf nodes, it stores the index of suffix for
        # the path  from root to leaf"""
        self.leaf = leaf
        self.suffixIndex = None
        self.start = None
        self.end = None
        self.suffixLink = None

    def __eq__(self, node):
        atg = attrgetter('start', 'end', 'suffixIndex')
        return atg(self) == atg(node)

    def __ne__(self, node):
        atg = attrgetter('start', 'end', 'suffixIndex')
        return atg(self) != atg(node)

    def __getattribute__(self, name):
        if name == 'end':
            if self.leaf:
                return leafEnd
        return super(Node, self).__getattribute__(name)


class Occupation:
    def __init__(self):
        self.total = 0
        self.counter = 0

    def increment(self, inc):
        self.total += inc
        self.counter += 1


class SuffixTree:
    def __init__(self, data):
        self._string = data
        self.lastNewNode = None
        self.activeNode = None
        self.activeEdge = -1
        self.activeLength = 0
        self.remainingSuffixCount = 0
        self.rootEnd = None
        self.splitEnd = None
        self.size = -1  # Length of input string
        self.root = None
        self.internalNodes = 0

    def edge_length(self, node):
        return node.end - node.start + 1

    def walk_down(self, current_node):
        length = self.edge_length(current_node)
        if (self.activeLength >= length):
            self.activeEdge += length
            self.activeLength -= length
            self.activeNode = current_node
            return True
        return False

    def new_node(self, start, end=None, leaf=False):
        node = Node(leaf)
        node.suffixLink = self.root
        node.start = start
        node.end = end
        node.suffixIndex = -1
        if not leaf and start >= 0:
            self.internalNodes += 1
        return node

    def extend_suffix_tree(self, pos):
        global leafEnd
        leafEnd = pos
        self.remainingSuffixCount += 1
        self.lastNewNode = None
        while (self.remainingSuffixCount > 0):
            if (self.activeLength == 0):
                self.activeEdge = pos
            if (self.activeNode.children.get(self._string[self.activeEdge]) is None):
                self.activeNode.children[self._string[self.activeEdge]] = self.new_node(pos, leaf=True)
                if (self.lastNewNode is not None):
                    self.lastNewNode.suffixLink = self.activeNode
                    self.lastNewNode = None
            else:
                _next = self.activeNode.children.get(self._string[self.activeEdge])
                if self.walk_down(_next):
                    continue
                if (self._string[_next.start + self.activeLength] == self._string[pos]):
                    if ((self.lastNewNode is not None) and (self.activeNode != self.root)):
                        self.lastNewNode.suffixLink = self.activeNode
                        self.lastNewNode = None
                    self.activeLength += 1
                    break
                self.splitEnd = _next.start + self.activeLength - 1
                split = self.new_node(_next.start, self.splitEnd)
                self.activeNode.children[self._string[self.activeEdge]] = split
                split.children[self._string[pos]] = self.new_node(pos, leaf=True)
                _next.start += self.activeLength
                split.children[self._string[_next.start]] = _next
                if (self.lastNewNode is not None):
                    self.lastNewNode.suffixLink = split
                self.lastNewNode = split
            self.remainingSuffixCount -= 1
            if ((self.activeNode == self.root) and (self.activeLength > 0)):  # APCFER2C1
                self.activeLength -= 1
                self.activeEdge = pos - self.remainingSuffixCount + 1
            elif (self.activeNode != self.root):  # APCFER2C2
                self.activeNode = self.activeNode.suffixLink

    def walk_dfs(self, current):
        start, end = current.start, current.end
        yield self._string[start: end + 1]

        for node in current.children.values():
            if node:
                yield from self.walk_dfs(node)

    def _count_active_windows(self, current, window, occupation):
        start, end = current.start, current.end
        if current.start >= 0:
            sorted_child_indexes = sorted(map(lambda node: node.start, current.children.values()))
            n = len(self._string)
            ocuppy = count_more_than_2_by_indexes(sorted_child_indexes, window, n) / (n - window + 1)
            occupation.increment(ocuppy)
        for node in current.children.values():
            if node and not node.leaf and node.start >= 0:
                self._count_active_windows(node, window, occupation)

    def count_active_windows(self, window):
        occupy = Occupation()
        self._count_active_windows(self.root, window, occupy)
        log(f"Occupy increased {occupy.counter} times")
        return occupy.total / occupy.counter

    def build_suffix_tree(self):
        self.size = len(self._string)
        self.rootEnd = -1
        self.root = self.new_node(-1, self.rootEnd)
        self.activeNode = self.root  # First activeNode will be root
        internal_nodes_history = []
        for i in range(self.size):
            self.extend_suffix_tree(i)
            internal_nodes_history.append(self.internalNodes)
        return internal_nodes_history

    def __str__(self):
        return "\n".join(map(str, self.edges.values()))

    def print_dfs(self):
        for sub in self.walk_dfs(self.root):
            print(sub)

import matplotlib.pyplot as plt

def show_history(s, show=True, showImmidiaely=False, title=""):
    st = SuffixTree(s)
    history = st.build_suffix_tree()
    if show:
        plt.title(title)
        p = plt.plot(history)
    if showImmidiaely:
        plt.show()
    return history


def show_repetition_parameter(text, title="", show=False):
    text = text+"$"
    history = show_history(text, show=False)
    v = [history[w] / (w + 1) for w in range(0, len(history) - 1)]
    if show:
        plt.title(title)
        plt.plot([history[w] / (w+1) for w in range(0, len(history)-1)])
        plt.show()
    return v

import argparse
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get Golcher Plot')
    parser.add_argument('--file', type=str,
                        help='path to text file')

    parser.add_argument('--out', type=str,
                        help='csv file to store V(t) data')
    parser.add_argument('--show', action='store_true',
                        help='plot V(t)')

    args = parser.parse_args()
    with open(args.file, 'r', encoding="utf8") as f:
        text = f.read().lower()
        print(text)
        show_history(text, show=False)
        history = show_repetition_parameter(text, show=args.show)
        if args.out is not None:
            np.savetxt(args.out, history, delimiter=",")

