import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)  # allows us to fetch files from the project root
import unittest

from modules.bool_circ_mx.binary_mx import *

class test_open_digraph(unittest.TestCase):

    def setUp(self):
        self.boolcirc = binary_mx.construct_op("1110001000111111")

    def test_construct_op(self):
        self.assertEqual(binary_mx.construct_op("1110001000111111").inputs ,self.boolcirc.inputs)
        self.assertEqual(binary_mx.construct_op("1110001000111111").outputs,self.boolcirc.outputs)
        self.assertEqual(str(binary_mx.construct_op("1110001000111111").nodes) ,str(self.boolcirc.nodes))

if __name__ == "__main__":  # the following code is called only when
    unittest.main()  # precisely this file is run