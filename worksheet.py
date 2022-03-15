import inspect
from tabnanny import verbose
from modules.open_digraph import *

i0 = Node(0, "i0", {}, {3: 1})
i1 = Node(1, "i1", {}, {3: 1})
i2 = Node(2, "i2", {}, {4: 1})
n0 = Node(3, "&", {0: 1, 1: 1}, {4: 1})
n1 = Node(4, "|", {3: 1, 2: 1}, {5: 1})
o0 = Node(5, "o0", {4: 1}, {})

od1 = OpenDigraph([0, 1, 2], [5], [i0, i1, i2, n0, n1, o0])

i3 = Node(0, "i3", {}, {1: 1})
n0 = Node(1, "", {0: 1}, {2: 1})
o2 = Node(2, "o2", {1: 1}, {})

od2 = OpenDigraph([0], [2], [i3, n0, o2])

od1.iparallel(od2)

od1.display(verbose=True)

print_matrix(od1.adjency_matrix())
