import inspect
from modules.open_digraph import *

n0 = Node(0, 'a', {}, {2:1})
n1 = Node(1, 'b', {}, {2:1})
n2 = Node(2, 'c', {0:1, 1:1}, {})
od0 = OpenDigraph([0, 1], [2], [n0, n1, n2])
print(od0)
