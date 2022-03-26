import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)  # allows us to fetch files from the project root
import unittest
from modules.open_digraph import *
from modules.open_digraph_mx.depth_mx import *


class test_depth_mx(unittest.TestCase):
    def setUp(self):
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

        self.test_graph = OpenDigraph(
            [10, 11], [12], [i0, i1, n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, o0]
        )

    def test_dijkstra(self):
        dist, prev = self.test_graph.dijkstra(6)
        self.assertEqual(dist[6], 0)
        self.assertEqual(dist[3], 1)
        self.assertEqual(dist[7], 2)
        self.assertEqual(dist[12], 3)

        self.assertEqual(prev[3], 6)
        self.assertEqual(prev[7], 3)
        self.assertEqual(prev[12], 7)

    def test_shortest_path(self):
        self.assertEqual(self.test_graph.shortest_path(0, 7), [0, 3, 7])
        self.assertEqual(self.test_graph.shortest_path(2, 8), [2, 4, 6, 8])
        self.assertEqual(self.test_graph.shortest_path(1, 8), [1, 8])

    def test_common_ancestors(self):
        self.assertEqual(
            self.test_graph.common_ancestors(5, 8),
            {
                0: (2, 3),
                1: (1, 1),
                3: (1, 2),
                10: (3, 4),
            },
        )
        self.assertEqual(
            self.test_graph.common_ancestors(8, 9),
            {
                0: (3, 3),
                1: (1, 3),
                2: (3, 3),
                3: (2, 2),
                4: (2, 2),
                6: (1, 1),
                10: (4, 4),
                11: (4, 4),
            },
        )

    def test_tri_topologique(self):
        self.assertEqual(
            self.test_graph.tri_topologique, [[0, 1, 2], [3, 4], [5, 6], [7, 8, 9]]
        )

    def test_node_depth(self):
        self.assertEqual(self.test_graph.node_depth(0), 0)
        self.assertEqual(self.test_graph.node_depth(3), 1)
        self.assertEqual(self.test_graph.node_depth(5), 2)
        self.assertEqual(self.test_graph.node_depth(9), 3)

    def test_depth(self):
        self.assertEqual(self.test_graph.depth, 4)

    def test_longest_path(self):
        path, dist_max = self.test_graph.longest_path(0, 7)
        self.assertEqual(path, [0, 3, 5, 7])
        self.assertEqual(dist_max, 3)

        path, dist_max = self.test_graph.longest_path(1, 8)
        self.assertEqual(path, [1, 4, 6, 8])
        self.assertEqual(dist_max, 3)


if __name__ == "__main__":  # the following code is called only when
    unittest.main()  # precisely this file is run
