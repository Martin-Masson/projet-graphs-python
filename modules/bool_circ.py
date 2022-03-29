from __future__ import annotations

from modules.open_digraph import *
from modules.bool_circ_mx.binary_mx import *


class BoolCirc(OpenDigraph, binary_mx):
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


def parse_parenthesis(*args: string) -> BoolCirc:
    operator = ["", "&", "|", "^", "~"]
    output_graph = OpenDigraph.empty()

    for s in args:
        o0 = Node(1, "", {0: 1}, {})
        n0 = Node(0, "", {}, {1: 1})
        g = OpenDigraph([], [1], [o0, n0])
        current_id = 0
        s2 = ""
        for char in s:
            if char == "(":
                current_node = g[current_id]
                if s2 != "":
                    labels = {node.label: node.id for node in g.get_nodes}
                    if not (s2 in operator) and s2 in labels:
                        g.fusion(current_id, labels[s2])
                    current_node.set_label(s2)
                new_id = g.add_node(g.new_id)
                g.add_edge(new_id, current_id)
                current_id = new_id
                s2 = ""
            elif char == ")":
                current_node = g[current_id]
                if s2 != "":
                    labels = {node.label: node.id for node in g.get_nodes}
                    if not (s2 in operator) and s2 in labels:
                        g.fusion(current_id, labels[s2])
                    current_node.set_label(s2)
                current_id = g[current_node.get_children_ids[0]].id
                s2 = ""
            else:
                s2 += char

        if s == args[0]:
            output_graph = g
        else:
            output_labels = {node.label: node.id for node in output_graph.get_nodes}
            n = output_graph.new_id

            output_graph.iparallel([g])

            component_nodes = []
            for node in output_graph.get_nodes:
                if node.id >= n:
                    component_nodes.append(node)

            for node in component_nodes:
                label = node.get_label
                if not (label in operator) and label in output_labels:
                    output_graph.fusion(node.get_id, output_labels[label])

    for node in output_graph.get_nodes:
        if node.parents == {}:
            input_id = output_graph.add_input_node(node.get_id)
            output_graph[input_id].set_label(node.get_label)
            node.set_label("")

    return output_graph
