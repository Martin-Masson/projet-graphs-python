import sys
import os
root = os.path.normpath(os.path.join(__file__, './../..'))
sys.path.append(root)# allows us to fetch files from the project root
import unittest
from modules.open_digraph import *

class InitTest(unittest.TestCase):
    def test_init_node(self):
        n0 = node(0, 'i', {}, {1: 1})
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, 'i')
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1: 1})
        self.assertIsInstance(n0, node)


if __name__ == '__main__':  # the following code is called only when
    unittest.main()  # precisely this file is run


class NodeTest(unittest.testcase):
    def setUp(self):
        self.n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
    def test_get_id(self):
        self.assertEqual(self.n0.get_id(), 0)
    def test_get_label(self):
        self.assertEqual(self.n0.get_label(), 'a')
    def test_get_parents(self):
        self.assertEqual(self.n0.get_parents(),{3:1, 4:1})
    def test_get_children(self):
        self.assertEqual(self.n0.get_children,{1:1, 2:1})


class open_digraphTest(unittest.testcase):
    n0 = node(0, 'a', {3:1, 4:1}, {1:1, 2:1})
    n1 = node(1, 'b', {0:1}, {2:2, 5:1})
    n2 = node(2, 'c', {0:1, 1:2}, {6:1})
    i0 = node(3, 'i0', {}, {0:1})
    i1 = node(4, 'i1', {}, {0:1})
    o0 = node(5, 'o0', {1:1}, {})
    o1 = node(6, 'o1', {2:1}, {})
    def setUp(self):
        self.dia = open_digraph([3,4], [5,6], [n0,n1,n2,i0,i1,o0,o1])
    def test_get_input(self):
        self.assertEqual(self.dia.get_inputs(), [3,4])
    def get_outputs(self):
        self.assertEqual(self.dia.get_outputs(), [5,6])
    def test_get_nodes(self):
        self.assertEqual(self.dia.get_nodes(),[n0,n1,n2,i0,i1,o0,o1])