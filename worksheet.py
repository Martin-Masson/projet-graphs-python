from cgi import test
from lib2to3.pgen2.token import OP
from modules.node import Node
from modules.open_digraph import OpenDigraph

i0 = Node(10, "", {}, {0: 1})
i1 = Node(11, "", {}, {2: 1})

n0 = Node(0, "", {10: 1}, {3: 1})
n1 = Node(1, "", {}, {4: 1, 5: 1, 8: 1})
n2 = Node(2, "", {11: 1}, {4: 1})
n3 = Node(3, "", {0: 1}, {5: 1, 6: 1, 7: 1})
n4 = Node(4, "", {1: 1, 2: 1}, {6: 1})
n5 = Node(5, "", {1: 1, 3: 1}, {7: 1})
n6 = Node(6, "", {3: 1, 4: 1}, {8: 1, 9: 1})
n7 = Node(7, "", {3: 1, 5: 1}, {12: 1})
n8 = Node(8, "", {1: 1, 6: 1}, {})
n9 = Node(9, "", {6: 1}, {})

o0 = Node(12, "", {7: 1}, {})

test_graph = OpenDigraph(
    [10, 11], [12], [i0, i1, n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, o0]
)

random_circ = OpenDigraph.random(10, 1, inputs=1, outputs=1)
test_graph.display(verbose=True)

