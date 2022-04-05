from __future__ import annotations
from typing import Dict, List, Tuple

from math import log2
from modules.bool_circ import *


class binary_mx:
    @classmethod
    def construct_op(self, bits: str) -> BoolCirc:
        length = len(bits)
        if (length != 0) and ((length & (length - 1)) == 0):
            n0 = Node(0, "", {1: 1}, {})
            n1 = Node(1, "|", {}, {0: 1})
            op = OpenDigraph([], [0], [n0, n1])
            n = int(log2(length))
            for i in range(n):
                copy_id = op.add_node()
                op.add_input_node(copy_id)

            for i, bit in enumerate(bits):
                if bit == "1":
                    and_id = op.add_node(label="&", children={1: 1})
                    bin_i = bin(i)[2:]
                    for x, bit_i in enumerate("0" * (n - len(bin_i)) + bin_i):
                        copy_id = 2 * (x + 1)
                        if bit_i == "1":
                            op.add_node(
                                label="~",
                                parents={copy_id: 1},
                                children={and_id: 1},
                            )
                        else:
                            op.add_edge(copy_id, and_id)
            return op
