import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)  # allows us to fetch files from the project root
import unittest

from modules.open_digraph import *


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
        self.assertEqual(od0.inputs, [0, 1])
        self.assertEqual(od0.outputs, [5, 6])
        self.assertEqual(od0.nodes, {0: i0, 1: i1, 2: n0, 3: n1, 4: n2, 5: o0, 6: o1})
        self.assertIsInstance(od0, OpenDigraph)


class test_open_digraph(unittest.TestCase):
    def setUp(self):
        self.v0 = Node(0, "v0", {}, {1: 1})
        self.v1 = Node(1, "v1", {0: 1}, {})

        self.od0 = OpenDigraph([0], [1], [self.v0, self.v1])

        self.i0 = Node(0, "i0", {}, {2: 1})
        self.i1 = Node(1, "i1", {}, {2: 1})
        self.n0 = Node(2, "a", {0: 1, 1: 1, 4: 1}, {3: 1, 4: 1})
        self.n1 = Node(3, "b", {2: 1}, {4: 2, 5: 1})
        self.n2 = Node(4, "c", {2: 1, 3: 2}, {2: 1, 6: 1})
        self.o0 = Node(5, "o0", {3: 1}, {})
        self.o1 = Node(6, "o1", {4: 1}, {})

        self.od1 = OpenDigraph(
            [0, 1],
            [5, 6],
            [self.i0, self.i1, self.n0, self.n1, self.n2, self.o0, self.o1],
        )

        self.od2 = OpenDigraph([3, 4], [0, 1], [self.i0, self.i1, self.n1, self.n2])

    def test_str(self):
        self.assertEqual(
            str(self.od0),
            "n0 = Node(0, v0, {}, {1: 1})\nn1 = Node(1, v1, {0: 1}, {})\n",
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.od0),
            "n0 = Node(0, v0, {}, {1: 1})\nn1 = Node(1, v1, {0: 1}, {})\n",
        )

    def test_empty(self):
        e = OpenDigraph.empty()
        self.assertEqual(e.inputs, [])
        self.assertEqual(e.outputs, [])
        self.assertEqual(e.nodes, {})
        self.assertIsInstance(e, OpenDigraph)

    def test_copy(self):
        self.assertIsNot(self.od0.copy, self.od0)

    def test_get_input_ids(self):
        self.assertEqual(self.od1.get_input_ids, [0, 1])

    def test_get_output_ids(self):
        self.assertEqual(self.od1.get_output_ids, [5, 6])

    def test_get_id_node_map(self):
        d = {
            0: self.i0,
            1: self.i1,
            2: self.n0,
            3: self.n1,
            4: self.n2,
            5: self.o0,
            6: self.o1,
        }
        self.assertEqual(self.od1.get_id_node_map, d)

    def test_get_nodes(self):
        l = [self.i0, self.i1, self.n0, self.n1, self.n2, self.o0, self.o1]
        self.assertEqual(self.od1.get_nodes, l)

    def test_get_node_ids(self):
        self.assertEqual(self.od1.get_node_ids, [0, 1, 2, 3, 4, 5, 6])

    def test_get_node_by_id(self):
        self.assertEqual(self.od1.get_node_by_id(4), self.n2)

    def test_get_nodes_by_ids(self):
        self.assertEqual(self.od1.get_nodes_by_ids([]), [])
        self.assertEqual(
            self.od1.get_nodes_by_ids([0, 4, 6]), [self.i0, self.n2, self.o1]
        )

    def test_set_input_ids(self):
        self.od1.set_input_ids([])
        self.assertEqual(self.od1.get_input_ids, [])

        self.od1.set_input_ids([0, 1, 2, 3])
        self.assertEqual(self.od1.get_input_ids, [0, 1, 2, 3])

    def test_set_output_ids(self):
        self.od1.set_output_ids([])
        self.assertEqual(self.od1.get_output_ids, [])

        self.od1.set_output_ids([7, 8, 9])
        self.assertEqual(self.od1.get_output_ids, [7, 8, 9])

    def test_add_input_id(self):
        self.od0.add_input_id(2)
        self.assertEqual(self.od0.get_input_ids, [0, 2])

        self.od1.add_input_id(2)
        self.assertEqual(self.od1.get_input_ids, [0, 1, 2])

    def test_add_output_id(self):
        self.od0.add_output_id(7)
        self.assertEqual(self.od0.get_output_ids, [1, 7])

        self.od1.add_output_id(7)
        self.assertEqual(self.od1.get_output_ids, [5, 6, 7])

    def test_new_id(self):
        self.assertNotIn(self.od1.new_id, self.od1.get_node_ids)

    def test_random_op(self):
        self.assertTrue(self.od1.random_op in self.od1.nodes)
    
    def test_random_input(self):
        self.assertTrue(self.od1.random_input in self.od1.inputs)
    
    def test_random_output(self):
        self.assertTrue(self.od1.random_output in self.od1.outputs)

    def test_add_edge(self):
        self.od1.add_edge(2, 3)
        self.assertEqual(self.od1.get_node_by_id(2).children, {3: 2, 4: 1})
        self.assertEqual(self.od1.get_node_by_id(3).parents, {2: 2})
        self.assertIsNone(self.od1.is_well_formed)

    def test_add_node(self):
        self.od0.add_node()
        k0 = self.od0.get_nodes[-1]
        self.assertEqual(self.od0.get_nodes, [self.v0, self.v1, k0])
        self.assertIsNone(self.od0.is_well_formed)

        self.od1.add_node()
        k1 = self.od1.get_nodes[-1]
        self.assertEqual(
            self.od1.get_nodes,
            [self.i0, self.i1, self.n0, self.n1, self.n2, self.o0, self.o1, k1],
        )
        self.assertIsNone(self.od1.is_well_formed)

    def test_remove_edges(self):
        self.od1.remove_edges((3, 4))
        self.assertEqual(self.od1.get_node_by_id(3).children, {4: 1, 5: 1})
        self.assertEqual(self.od1.get_node_by_id(4).parents, {2: 1, 3: 1})

        self.od1.remove_edges((2, 3))
        self.assertEqual(self.od1.get_node_by_id(2).children, {4: 1})
        self.assertEqual(self.od1.get_node_by_id(3).parents, {})
        self.assertIsNone(self.od1.is_well_formed)

    def test_remove_parallel_edges(self):
        self.od1.remove_parallel_edges((3, 4))
        self.assertEqual(self.od1.get_node_by_id(3).children, {5: 1})
        self.assertEqual(self.od1.get_node_by_id(4).parents, {2: 1})

    def test_remove_node_by_id(self):
        self.od1.remove_node_by_id(2)
        self.assertEqual(self.od1.get_nodes, [self.n1, self.n2, self.o0, self.o1])
        self.assertEqual(self.od1.get_input_ids, [])
        self.assertEqual(self.n1.parents, {})
        self.assertEqual(self.n2.parents, {3: 2})
        self.assertEqual(self.n2.children, {6: 1})

    # def test_is_well_formed(self):
    #     self.assertIsNone(self.od0.is_well_formed)
    #     self.assertIsNone(self.od1.is_well_formed)
    #     self.assertRaises(Exception, self.od2.is_well_formed)

    def test_add_input_node(self):
        self.od1.add_input_node(2)
        self.assertEqual(self.od1.get_node_by_id(2).parents, {0: 1, 1: 1, 4: 1, 7: 1})
        self.assertIsNone(self.od1.is_well_formed)

    def test_add_output_node(self):
        self.od1.add_output_node(4)
        self.assertEqual(self.od1.get_node_by_id(4).children, {2: 1, 6: 1, 7: 1})
        self.assertIsNone(self.od1.is_well_formed)

    # def test_fusion(self):
    #     self.od1.fusion(2,4)
    #     self.assertEqual(self.od1.get_node_by_id(2).children, {3: 1, 4: 1, 2: 1, 6: 1})

if __name__ == "__main__":  # the following code is called only when
    unittest.main()  # precisely this file is run
