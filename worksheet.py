from cgi import test
from lib2to3.pgen2.token import OP
from modules.node import Node
from modules.open_digraph import OpenDigraph
from modules.bool_circ import *

a = Node(9, "1", {}, {0: 1})
b = Node(10, "0", {}, {1: 1})
c = Node(11, "1", {}, {4: 1})

n0 = Node(0, "", {9: 1}, {2: 1, 5: 1})
n1 = Node(1, "", {10: 1}, {2: 1, 5: 1})
n2 = Node(2, "^", {0: 1, 1: 1}, {3: 1})
n3 = Node(3, "", {2: 1}, {6: 1, 7: 1})
n4 = Node(4, "", {11: 1}, {6: 1, 7: 1})
n5 = Node(5, "&", {0: 1, 1: 1}, {8: 1})
n6 = Node(6, "&", {3: 1, 4: 1}, {8: 1})
n7 = Node(7, "^", {3: 1, 4: 1}, {13: 1})
n8 = Node(8, "|", {5: 1, 6: 1}, {12: 1})

co = Node(12, "", {8: 1}, {})
r = Node(13, "", {7: 1}, {})

adder_0 = BoolCirc(
    OpenDigraph(
        [9, 10, 11],
        [12, 13],
        [a, b, c, n0, n1, n2, n3, n4, n5, n6, n7, n8, co, r],
    )
)

# random_circ = OpenDigraph.random(10, 1, inputs=2, outputs=2)
adder_0.evaluate()

adder_0.display()
