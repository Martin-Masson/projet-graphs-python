import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)  # allows us to fetch files from the project root
import unittest
from modules.open_digraph_mx.matrix_mx import *


class test_open_digraph(unittest.TestCase):
    
    def test_random_matrix(self):
        m = random_matrix(5, 5, null_diag=True)
        for i in range(5):
            for j in range(5):
                if i == j:
                    self.assertEqual(m[i][j], 0)
        m = random_matrix(5, 5, symetric=True)
        for i in range(5):
            for j in range(5):
                self.assertEqual(m[i, j], m[j, i])
        m = random_matrix(5, 5, oriented=True)
        for i in range(5):
            for j in range(5):
                if m[i][j] != 0:
                    self.assertEqual(m[j, i], 0)
        m = random_matrix(5, 5, triangular=True)
        for i in range(5):
            for j in range(5):
                if i > j:
                    self.assertEqual(m[i, j], 0)

if __name__ == "__main__":  # the following code is called only when
    unittest.main()  # precisely this file is run