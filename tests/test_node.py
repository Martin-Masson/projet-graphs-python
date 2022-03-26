import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)  # allows us to fetch files from the project root
import unittest

from modules.node import *


class test_init(unittest.TestCase):
    def test_init_node(self):
        n0 = Node(0, "i", {}, {1: 1})

        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.label, "i")
        self.assertEqual(n0.parents, {})
        self.assertEqual(n0.children, {1: 1})
        self.assertIsInstance(n0, Node)


class test_node(unittest.TestCase):
    def setUp(self):
        self.n0 = Node(2, "a", {0: 1, 1: 1, 4: 1}, {3: 1, 4: 1})

    def test_str(self):
        self.assertEqual(str(self.n0), "Node(2, a, {0: 1, 1: 1, 4: 1}, {3: 1, 4: 1})")

    def test_repr(self):
        self.assertEqual(repr(self.n0), "Node(2, a, {0: 1, 1: 1, 4: 1}, {3: 1, 4: 1})")

    def test_copy(self):
        self.assertIsNot(self.n0.copy, self.n0)

    def test_get_id(self):
        self.assertEqual(self.n0.get_id, 2)

    def test_get_label(self):
        self.assertEqual(self.n0.get_label, "a")

    def test_get_parent_ids(self):
        self.assertEqual(self.n0.get_parent_ids, [0, 1, 4])

    def test_get_children_ids(self):
        self.assertEqual(self.n0.get_children_ids, [3, 4])

    def test_set_id(self):
        self.n0.set_id(3)
        self.assertEqual(self.n0.get_id, 3)

    def test_set_label(self):
        self.n0.set_label("b")
        self.assertEqual(self.n0.get_label, "b")

    def test_set_parent_ids(self):
        self.n0.set_parent_ids({1: 1, 2: 1, 3: 1})
        self.assertEqual(self.n0.get_parent_ids, [1, 2, 3])

    def test_set_children_ids(self):
        self.n0.set_children_ids({7: 1, 8: 1, 9: 1})
        self.assertEqual(self.n0.get_children_ids, [7, 8, 9])

    def test_add_child_id(self):
        self.n0.add_child_id(5)
        self.assertEqual(self.n0.get_children_ids, [3, 4, 5])

    def test_add_parent_id(self):
        self.n0.add_parent_id(5)
        self.assertEqual(self.n0.get_parent_ids, [0, 1, 4, 5])

    def test_remove_parent_once(self):
        self.n0.remove_parent_once(4)
        self.assertEqual(self.n0.get_parent_ids, [0, 1])

    def test_remove_child_once(self):
        self.n0.remove_child_once(4)
        self.assertEqual(self.n0.get_children_ids, [3])

    def test_remove_parent_id(self):
        self.n0.add_parent_id(4)
        self.n0.remove_parent_id(4)
        self.assertEqual(self.n0.get_parent_ids, [0, 1])

    def test_remove_child_id(self):
        self.n0.add_child_id(4)
        self.n0.remove_child_id(4)
        self.assertEqual(self.n0.get_children_ids, [3])


if __name__ == "__main__":  # the following code is called only when
    unittest.main()  # precisely this file is run
