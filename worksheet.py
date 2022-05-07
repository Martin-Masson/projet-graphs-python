from cgi import test
from lib2to3.pgen2.token import OP
from modules.node import Node
from modules.open_digraph import OpenDigraph
from modules.bool_circ import *

a = Node(0, "1", {}, {3: 1})
b = Node(1, "0", {}, {4: 1})
c = Node(2, "1", {}, {7: 1})

n0 = Node(3, "", {0: 1}, {5: 1, 8: 1})
n1 = Node(4, "", {1: 1}, {5: 1, 8: 1})
n2 = Node(5, "^", {3: 1, 4: 1}, {6: 1})
n3 = Node(6, "", {5: 1}, {9: 1, 10: 1})
n4 = Node(7, "", {2: 1}, {9: 1, 10: 1})
n5 = Node(8, "&", {3: 1, 4: 1}, {11: 1})
n6 = Node(9, "&", {6: 1, 7: 1}, {11: 1})
n7 = Node(10, "^", {6: 1, 7: 1}, {13: 1})
n8 = Node(11, "|", {8: 1, 9: 1}, {12: 1})

co = Node(12, "", {11: 1}, {})
r = Node(13, "", {10: 1}, {})

adder_0 = BoolCirc(
    OpenDigraph(
        [0, 1, 2],
        [12, 13],
        [a, b, c, n0, n1, n2, n3, n4, n5, n6, n7, n8, co, r],
    )
)

# BoolCirc.adder(2).display(verbose=True)

OpenDigraph.from_dot_file("digraph.dot").display()
