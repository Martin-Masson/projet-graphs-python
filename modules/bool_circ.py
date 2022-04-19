from __future__ import annotations

import random

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

    @classmethod
    def random(cls, n: int, bound: int, inputs: int = 0, outputs: int = 0) -> BoolCirc:
        circ = OpenDigraph.random(n, bound, form="DAG")
        for node in circ.get_nodes:
            if not (node.has_parents):
                circ.add_input_node(node.get_id)
            if not (node.has_children):
                circ.add_output_node(node.get_id)

        if inputs != 0 and outputs != 0:
            while inputs > len(circ.inputs):
                circ.add_input_node(circ.random_op)
            while inputs < len(circ.inputs):
                input_1 = circ[circ.random_input]
                other = circ.inputs.copy()
                other.remove(input_1.get_id)
                input_2 = circ[random.choice(other)]
                input_1_child = circ[input_1.get_children_ids[0]]
                new_id = circ.add_node(
                    parents={input_1.id: 1},
                    children=input_1.children | input_2.children,
                )
                circ.remove_parallel_edges((input_1.get_id, input_1_child.get_id))
                circ.remove_node_by_id(input_2.get_id)

            while outputs > len(circ.outputs):
                circ.add_output_node(circ.random_op)
            while outputs < len(circ.outputs):
                output_1 = circ[circ.random_output]
                other = circ.outputs.copy()
                other.remove(output_1.get_id)
                output_2 = circ[random.choice(other)]
                output_1_parent = circ[output_1.get_parent_ids[0]]
                new_id = circ.add_node(
                    parents=output_1.parents | output_2.parents,
                    children={output_1.id: 1},
                )
                circ.remove_parallel_edges((output_1_parent.get_id, output_1.get_id))
                circ.remove_node_by_id(output_2.get_id)

        for node in circ.get_nodes:
            if node.in_degree == 1 and node.out_degree == 1:
                node.set_label("~")

            if node.in_degree > 1:
                node.set_label(random.choice(["&", "|", "^"]))
                if node.out_degree > 1:
                    children = node.children.copy()
                    new_id = circ.add_node(parents={node.get_id: 1}, children=children)
                    for child_id in children.copy():
                        circ.remove_parallel_edges((node.get_id, child_id))

        return circ


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
        if not (node.has_parents):
            input_id = output_graph.add_input_node(node.get_id)
            output_graph[input_id].set_label(node.get_label)
            node.set_label("")

    return output_graph
