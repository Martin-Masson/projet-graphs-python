import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)  # allows us to fetch files from the project root
import unittest

from modules.bool_circ import *

class test_init(unittest.TestCase):
    def test_init_open_digraph(self):
        i0 = Node(0, "i0", {}, {2: 1})
        i1 = Node(1, "i1", {}, {2: 1})
        n0 = Node(2, "a", {0: 1, 1: 1, 4: 1}, {3: 1, 4: 1})
        n1 = Node(3, "b", {2: 1}, {4: 2, 5: 1})
        n2 = Node(4, "c", {2: 1, 3: 2}, {2: 1, 6: 1})
        o0 = Node(5, "o0", {3: 1}, {})
        o1 = Node(6, "o1", {4: 1}, {})

        od0 = OpenDigraph([0, 1], [5, 6], [i0, i1, n0, n1, n2, o0, o1])
        # boolcir = BoolCirc(od0)


class test_open_digraph(unittest.TestCase):
    def setUp(self):
        self.v1 = parse_parenthesis("((x0)&((x1)&(x2)))|((x1)&(~(x2)))")
        self.v2 = BoolCirc.random(2, 2, 1, 1)
    
    def test_random(self):
        self.assertEqual(len(self.v2.nodes) - len(self.v2.inputs) - len(self.v2.outputs) in [2,4], True)
        self.assertEqual(len(BoolCirc.random(2, 2, 1, 1).inputs), 1)
        self.assertEqual(len(BoolCirc.random(2, 2, 1, 1).outputs), 1)


    def test_parse_parenthesis(self):
        self.assertEqual(self.v1.inputs, parse_parenthesis("((x0)&((x1)&(x2)))|((x1)&(~(x2)))").inputs)
        self.assertEqual(self.v1.outputs, parse_parenthesis("((x0)&((x1)&(x2)))|((x1)&(~(x2)))").outputs)
        self.assertEqual(str(self.v1.nodes), str(parse_parenthesis("((x0)&((x1)&(x2)))|((x1)&(~(x2)))").nodes))

if __name__ == "__main__":  # the following code is called only when
    unittest.main()  # precisely this file is run