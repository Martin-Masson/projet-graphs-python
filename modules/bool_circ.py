from __future__ import annotations
from typing import Dict, List, Tuple

from modules.open_digraph import *

class BoolCirc(OpenDigraph):
    def __init__(self, g: OpenDigraph) -> BoolCirc:
        if isinstance(OpenDigraph, g):
            if not(g.is_well_formed()):
                raise Exception(f"Invalid argument: the argument isn't a well formed boolean circuit")
            else:
                super().__init__(g.inputs, g.outputs, g.nodes)
        else:
            raise Exception(f"Invalid argument: argument must be an OpenDigraph")
    
    def is_well_formed(self) -> None:
        # Checks if the graph is acyclic
        if self.is_cyclic():
            raise Exception(f"The graph is cyclic")

        # Checks if ann nodes respect their degree requirement
        valid_labels = ["0", "1", "", "&", "|", "^", "~"]
        for node_id in self.nodes:
            node = self.get_node_by_id(node_id)
            label = node.get_label()
            if not(label in valid_labels):
                raise Exception(f"The label of node {node_id} is invalid. Valid labels are {valid_labels}")
            
            if label == "":
                if node.in_degree() != 1:
                    raise Exception(f"COPY node {node_id} must have an in degree of exactly 1")
            
            if label == "&":
                if node.out_degree() != 1:
                    raise Exception(f"AND node {node_id} must have an out degree of exactly 1")
            
            if label == "|":
                if node.out_degree() != 1:
                    raise Exception(f"OR node {node_id} must have an out degree of exactly 1")

            if label == "^":
                if node.out_degree() != 1:
                    raise Exception(f"XOR node {node_id} must have an out degree of exactly 1")

            if label == "~":
                if node.in_degree() != 1 or node.out_degree() != 1:
                    raise Exception(f"NOT node {node_id} must have an in degree and out degree of exactly 1")
