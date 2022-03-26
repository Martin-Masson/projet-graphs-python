from __future__ import annotations

from modules.open_digraph import *


class BoolCirc(OpenDigraph):
    def __init__(self, g: OpenDigraph) -> BoolCirc:
        if isinstance(g, OpenDigraph):
            if not (g.is_well_formed):
                """
                raise Exception(
                    f"Invalid argument: the argument isn't a well formed boolean circuit"
                )
                """
                super().__init__(g.inputs, g.outputs, g.nodes)
            else:
                super().__init__(g.inputs, g.outputs, g.nodes)
        else:
            raise Exception(f"Invalid argument: argument must be an OpenDigraph")

    @property
    def is_well_formed(self) -> None:
        # Checks if the graph is acyclic
        if self.is_cyclic:
            raise Exception(f"The graph is cyclic")

        # Checks if ann nodes respect their degree requirement
        valid_labels = ["0", "1", "", "&", "|", "^", "~"]
        for node_id in self.nodes:
            node = self.get_node_by_id(node_id)
            label = node.get_label
            if not (label in valid_labels):
                raise Exception(
                    f"The label of node {node_id} is invalid. Valid labels are {valid_labels}"
                )

            if label == "":
                if node.in_degree != 1:
                    raise Exception(
                        f"COPY node {node_id} must have an in degree of exactly 1"
                    )

            if label == "&":
                if node.out_degree != 1:
                    raise Exception(
                        f"AND node {node_id} must have an out degree of exactly 1"
                    )

            if label == "|":
                if node.out_degree != 1:
                    raise Exception(
                        f"OR node {node_id} must have an out degree of exactly 1"
                    )

            if label == "^":
                if node.out_degree != 1:
                    raise Exception(
                        f"XOR node {node_id} must have an out degree of exactly 1"
                    )

            if label == "~":
                if node.in_degree != 1 or node.out_degree != 1:
                    raise Exception(
                        f"NOT node {node_id} must have an in degree and out degree of exactly 1"
                    )


def parse_parenthesis(s: string) -> BoolCirc:
    o0 = Node(1, "", {0: 1}, {})
    n0 = Node(0, "", {}, {1: 1})
    g = OpenDigraph([], [1], [o0, n0])
    current_id = 0
    s2 = ""
    for char in s:
        if char == "(":
            current_node = g[current_id]
            if s2 != "":
                current_node.set_label(s2)
            new_id = g.add_node(g.new_id)
            g.add_edge(new_id, current_id)
            current_id = new_id
            s2 = ""
        elif char == ")":
            current_node = g[current_id]
            if s2 != "":
                current_node.set_label(s2)
            current_id = g[current_node.get_children_ids[0]].id
            s2 = ""
        else:
            s2 += char
    return g
