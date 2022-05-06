from __future__ import annotations
from typing import Dict, List, Tuple

from modules.open_digraph import *


class evaluation_mx:
    @classmethod
    def circ_from_int(cls, n: int, bin_size: int = 8) -> BoolCirc:
        output = OpenDigraph.empty()
        b = bin(n)[2:]
        while len(b) < bin_size:
            b = "0" + b
        for digit in b:
            copy_id = output.add_node()
            output.add_input_node(copy_id, label=digit)
        return output

    def copy_rule(self, primitive_id: int, op_id: int) -> None:
        bit = self[primitive_id].get_label
        op = self[op_id]
        self.remove_node_by_id(primitive_id)
        for child_id in op.get_children_ids:
            self.add_node(label=bit, children={child_id: 1})
        self.remove_node_by_id(op_id)

    def not_rule(self, primitive_id: int, op_id: int) -> None:
        bit = self[primitive_id].get_label
        op = self[op_id]
        self.remove_node_by_id(primitive_id)
        if bit == "0":
            op.set_label("1")
        else:
            op.set_label("0")

    def and_rule(self, primitive_id: int, op_id: int) -> None:
        bit = self[primitive_id].get_label
        op = self[op_id]
        self.remove_node_by_id(primitive_id)
        if bit == "0":
            for parent_id in op.get_parent_ids:
                self.add_node(parents={parent_id: 1})
                self.remove_parallel_edges((parent_id, op_id))
            op.set_label("0")

    def or_rule(self, primitive_id: int, op_id: int) -> None:
        bit = self[primitive_id].get_label
        op = self[op_id]
        self.remove_node_by_id(primitive_id)
        if bit == "1":
            for parent_id in op.get_parent_ids:
                self.add_node(parents={parent_id: 1})
                self.remove_parallel_edges((parent_id, op_id))
            op.set_label("1")

    def xor_rule(self, primitive_id: int, op_id: int) -> None:
        bit = self[primitive_id].get_label
        op = self[op_id]
        self.remove_node_by_id(primitive_id)
        if bit == "1":
            old_parents = op.parents.copy()
            for parent_id in op.get_parent_ids:
                self.remove_parallel_edges((parent_id, op_id))
            self.add_node(label="^", parents=old_parents, children={op_id: 1})
            op.set_label("~")

    def neutral_rule(self, op_id: int) -> None:
        op = self[op_id]
        op_label = op.get_label
        if op_label == "|" or op_label == "^":
            op.set_label("0")
        if op_label == "&":
            op.set_label("1")

    def simplify(self, primitive_id: int, op_id: int, label: str) -> None:
        if label == "":
            self.copy_rule(primitive_id, op_id)
        if label == "~":
            self.not_rule(primitive_id, op_id)
        if label == "&":
            self.and_rule(primitive_id, op_id)
        if label == "|":
            self.or_rule(primitive_id, op_id)
        if label == "^":
            self.xor_rule(primitive_id, op_id)
        if label == "n":
            self.neutral_rule(op_id)

    def evaluate(self) -> None:
        # 1) on simplifie les inputs pour pouvoir utiliser le tri
        # topologique
        for input_id in self.get_input_ids:
            bit = self[input_id]
            op = self[bit.get_children_ids[0]]
            self.simplify(input_id, op.get_id, op.get_label)

        layers = self.tri_topologique

        # 2) on simplifie toutes les nodes de la couche la plus
        # haute jusqu'à n'avoir plus qu'une seule couche
        while len(layers) > 1:
            top_layer = layers[0]
            for node_id in top_layer:
                node = self[node_id]
                node_label = node.get_label
                if node_label != 0 or node_label != 1:
                    self.simplify(None, node_id, "n")
                else:
                    child = self[node.get_children_ids[0]]
                    self.simplify(node_id, child_id, child.get_label)
            layers = self.tri_topologique
