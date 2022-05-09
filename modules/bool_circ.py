from __future__ import annotations

import random
import string


from modules.open_digraph import *
from modules.bool_circ_mx.binary_mx import binary_mx
from modules.bool_circ_mx.evaluation_mx import evaluation_mx


class BoolCirc(OpenDigraph, binary_mx, evaluation_mx):
    def __init__(self, g: OpenDigraph) -> BoolCirc:
        """Constructor.

        Parameters
        ----------
        g: OpenDigraph
            Graphe à transformer en matrice booléenne circulaire.
        """
        if isinstance(g, OpenDigraph):
            if g.is_well_formed:  # Returns None if the graph is well formed
                raise Exception(
                    f"Invalid argument: the argument isn't a well formed boolean circuit"
                )
                super().__init__(g.inputs, g.outputs, g.nodes.values())
            else:
                super().__init__(g.inputs, g.outputs, g.nodes.values())
        else:
            raise Exception(f"Invalid argument: argument must be an OpenDigraph")

    @property
    def is_well_formed(self) -> None:
        """Returns True if the digraph is well formed.

        Raises:
        ------
        Exception:
            If the digraph is not well formed with the description of the problem.
        """
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

            if label == "0" or label == "1":
                if node.in_degree != 0 or node.out_degree != 1:
                    raise Exception(
                        f"primitive node {node_id} must must have an in degree of exactly 0 and out degree of exactly 1"
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
        """Returns a random boolean circuit of n nodes between 0 and bound with a given number of inputs and outputs.

        Parameters:
        -----------
        n: int
            The number of nodes of the circuit.
        bound: int
            The maximum value of the nodes.

        Optional parameters:
        ---------------------
        inputs: int
            The number of inputs of the circuit.
        outputs: int
            The number of outputs of the circuit.

        Returns:
        --------
        circ : BoolCirc
            A random boolean circuit.

        """
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
                    for child_id in children:
                        circ.remove_parallel_edges((node.get_id, child_id))

        return BoolCirc(circ)

    @classmethod
    def adder_0(cls) -> BoolCirc:
        a = Node(9, "", {}, {0: 1})
        b = Node(10, "", {}, {1: 1})
        c = Node(11, "", {}, {4: 1})

        n0 = Node(0, "", {9: 1}, {2: 1, 5: 1})
        n1 = Node(1, "", {10: 1}, {2: 1, 5: 1})
        n2 = Node(2, "^", {0: 1, 1: 1}, {3: 1})
        n3 = Node(3, "", {2: 1}, {6: 1, 7: 1})
        n4 = Node(4, "", {11: 1}, {6: 1, 7: 1})
        n5 = Node(5, "&", {0: 1, 1: 1}, {8: 1})
        n6 = Node(6, "&", {3: 1, 4: 1}, {8: 1})
        n7 = Node(7, "^", {3: 1, 4: 1}, {13: 1})
        n8 = Node(8, "|", {5: 1, 6: 1}, {12: 1})

        co = Node(12, "", {8: 1}, {})
        r = Node(13, "", {7: 1}, {})

        return BoolCirc(
            OpenDigraph(
                [9, 10, 11],
                [12, 13],
                [a, b, c, n0, n1, n2, n3, n4, n5, n6, n7, n8, co, r],
            )
        )

    @classmethod
    def adder(cls, n: int) -> BoolCirc:
        if n == 0:
            return cls.adder_0().copy
        else:
            c1 = cls.adder(n - 1)
            c2 = cls.adder(n - 1)

            carry_out = None
            for node_id in c1.get_output_ids:
                out_node = c1[node_id]
                if c1[out_node.get_parent_ids[0]].get_label == "|":
                    carry_out = out_node

            carry_in = None
            for node_id in c2.get_input_ids:
                in_node = c2[node_id]
                cp_node = c2[in_node.get_children_ids[0]]
                for child_id in cp_node.get_children_ids:
                    child_node = c2[child_id]
                    if child_node.get_children_ids[0] in c2.outputs:
                        carry_in = in_node

            c2.shift_indices(c1.max_id - c2.min_id + 1)
            for node in c2.get_nodes:
                c1.nodes[node.id] = node

            c1.add_edge(carry_out.get_parent_ids[0], carry_in.get_children_ids[0])
            c1.remove_node_by_id(carry_out.get_id, carry_in.get_id)

            c1.inputs += c2.inputs
            c1.inputs.remove(carry_in.get_id)
            c1.outputs += c2.outputs

            return c1

    @classmethod
    def half_adder(cls, n: int) -> BoolCirc:
        circ = cls.adder(n)
        circ.nodes[11].set_label("0")
        circ.inputs.remove(11)
        return circ

    @classmethod
    def encoder(cls) -> BoolCirc:
        return BoolCirc(OpenDigraph.from_dot_file("encoder.dot"))

    @classmethod
    def decoder(cls) -> BoolCirc:
        return BoolCirc(OpenDigraph.from_dot_file("decoder.dot"))


def parse_parenthesis(*args: string) -> BoolCirc:
    """Returns a boolean circuit from a string.

    Parameters
    ----------
    *args : string
        The string to parse.
    Returns
    -------
    BoolCirc : BoolCirc
        The boolean circuit.

    """
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
