from __future__ import annotations
from typing import Dict, List, Tuple
from copy import deepcopy
import itertools
import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)

from modules.node import *
from modules.exception import *
from modules.open_digraph_mx.matrix_mx import *
from modules.open_digraph_mx.display_mx import *
from modules.open_digraph_mx.bool_circ_mx import *
from modules.open_digraph_mx.depth_mx import *

Matrix = List[List[int]]


class OpenDigraph(
    matrix_mx, display_mx, bool_circ_mx, depth_mx
):  # for open directed graph
    def __init__(
        self, inputs: List[int], outputs: List[int], nodes: List[Node]
    ) -> OpenDigraph:
        """
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        """

        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id: node for node in nodes}

    def __getitem__(self, node_id) -> Node:
        return self.nodes[node_id]

    def __str__(self) -> str:
        output = ""
        for node in list(self.nodes.values()):
            output += "n" + str(node.id) + " = " + str(node) + "\n"
        return output

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def empty(cls) -> OpenDigraph:
        """Returns an empty open digraph"""
        return cls([], [], [])

    @classmethod
    def random(
        cls, n: int, bound: int, inputs: int = 0, outputs: int = 0, form: str = "free"
    ) -> OpenDigraph:
        """
        Doc
        Bien préciser ici les options possibles pour form !
        """
        if form == "free":
            digraph = cls.graph_from_adjacency_matrix(random_matrix(n, bound))
        elif form == "DAG":
            digraph = cls.graph_from_adjacency_matrix(
                random_matrix(n, bound, null_diag=True, triangular=True)
            )
        elif form == "oriented":
            digraph = cls.graph_from_adjacency_matrix(
                random_matrix(n, bound, oriented=True)
            )
        elif form == "loop-free":
            digraph = cls.graph_from_adjacency_matrix(
                random_matrix(n, bound, null_diag=True)
            )
        elif form == "undirected":
            digraph = cls.graph_from_adjacency_matrix(
                random_matrix(n, bound, symetric=True)
            )
        elif form == "loop-free undirected":
            digraph = cls.graph_from_adjacency_matrix(
                random_matrix(n, bound, null_diag=True, symetric=True)
            )

        length = len(digraph.nodes) - 1

        for input in range(inputs):
            digraph.add_input_node(random.randint(0, length))
        for output in range(outputs):
            digraph.add_output_node(random.randint(0, length))
        return digraph

    @classmethod
    def graph_from_adjacency_matrix(cls, matrix: Matrix) -> OpenDigraph:
        digraph = OpenDigraph.empty()
        n = len(matrix)
        for i in range(n):
            digraph.add_node()
        for i, j in itertools.product(range(n), range(n)):
            multi = matrix[i][j]
            if multi != 0:
                for k in range(multi):
                    digraph.add_edge(i, j)
        return digraph

    @classmethod
    def from_dot_file(self, path: str) -> OpenDigraph:
        lines = []
        with open(path, "rt") as file:
            for line in file:
                lines.append(line)

    @property
    def is_empty(self) -> bool:
        return self.nodes == {}

    @property
    def copy(self) -> OpenDigraph:
        """Returns a copy of the open digraph"""
        return deepcopy(self)

    @property
    def get_input_ids(self) -> List[int]:
        """Returns the inputs of the open digraph"""
        return self.inputs

    @property
    def get_output_ids(self) -> List[int]:
        """Returns the outputs of the open digraph"""
        return self.outputs

    @property
    def get_id_node_map(self) -> Dict[int, Node]:
        """Returns the nodes of the open digraph"""
        return self.nodes

    @property
    def get_nodes(self) -> List[Node]:
        """Returns a list of all the nodes in the open digraph"""
        return list(self.nodes.values())

    @property
    def get_node_ids(self) -> List[int]:
        """Returns a list of all the nodes id in the open digraph"""
        return list(self.nodes.keys())

    def get_node_by_id(self, node_id: int) -> Node:
        """Returns the node of id node_id in the open digraph"""
        return self.nodes[node_id]

    def get_nodes_by_ids(self, ids: List[int]) -> List[Node]:
        """Returns a list of the nodes of given ids in the open digraph"""
        output = []
        for id in ids:
            output.append(self.get_node_by_id(id))
        return output

    def set_input_ids(self, new_inputs_ids: List[int]) -> None:
        """Sets the open digraph input ids to new_inputs_ids"""
        self.inputs = new_inputs_ids

    def set_output_ids(self, new_outputs_ids: List[int]) -> None:
        """Sets the open digraph output ids to new_outputs_ids"""
        self.outputs = new_outputs_ids

    def add_input_id(self, new_input_id: int) -> None:
        """Adds new_input_id to the open digraph's input ids"""
        self.inputs.append(new_input_id)

    def add_output_id(self, new_output_id: int) -> None:
        """Adds new_output_id to the open digraph's output ids"""
        self.outputs.append(new_output_id)

    @property
    def new_id(self) -> int:
        """Returns a new id unused by any node of the open digraph"""
        if self.is_empty:
            return 0
        else:
            return max(self.nodes) + 1

    def add_edge(self, src: int, tgt: int) -> None:
        """Adds a edge from node of id src to node of id tgt"""
        tgt_node = self.get_node_by_id(tgt)
        src_node = self.get_node_by_id(src)
        if src in tgt_node.parents and tgt in src_node.children:
            tgt_node.parents[src] += 1
            src_node.children[tgt] += 1
        else:
            tgt_node.parents[src] = 1
            src_node.children[tgt] = 1

    def add_node(
        self,
        label: str = "",
        parents: Dict[int, int] = None,
        children: Dict[int, int] = None,
    ) -> int:
        """Adds a new node to the open digraph

        Optionnal Parameters
        ----------
        label : str (default "")
            The label of the new node
        parents : Dict[int, int] (default {})
            The parents of the new node
        children : Dict[int, int] (default {})
            The children of the new node

        Returns
        ----------
        node_id : int
            The id of the new node
        """
        parents = {} if parents is None else parents
        children = {} if children is None else children
        node_id = self.new_id
        new_node = Node(node_id, label, parents, children)
        self.nodes[node_id] = new_node
        for parent in list(parents.keys()):
            for child in list(children.keys()):
                for multi in list(parents.values()):
                    self.add_edge(parent, node_id)
                for multi in list(children.values()):
                    self.add_edge(node_id, child)
        return node_id

    # *args are tuples (src, tgt)
    def remove_edges(self, *args: Tuple[int, int]) -> None:
        """Removes and edge between two target nodes

        Parameters
        ----------
        *args
            Arguments should be tuples (src, tgt) where src is the id of the source node of the edge
            and tgt is the id of the target node where the edge points
        """
        for arg in args:
            src = arg[0]
            tgt = arg[1]
            src_node = self.get_node_by_id(src)
            tgt_node = self.get_node_by_id(tgt)
            if tgt_node.parents[src] > 1 and src_node.children[tgt] > 1:
                tgt_node.parents[src] -= 1
                src_node.children[tgt] -= 1
            else:
                del tgt_node.parents[src]
                del src_node.children[tgt]

    def remove_parallel_edges(self, *args: Tuple[int, int]) -> None:
        """Removes all edges between two target nodes

        Parameters
        ----------
        *args
            Arguments should be tuples (src, tgt) where src is the id of the source node of the edge
            and tgt is the id of the target node where the edge points
        """
        for arg in args:
            src = arg[0]
            tgt = arg[1]
            src_node = self.get_node_by_id(src)
            tgt_node = self.get_node_by_id(tgt)
            del src_node.children[tgt]
            del tgt_node.parents[src]

    def remove_node_by_id(self, *args: int) -> None:
        """Removes nodes from the open digraph

        Parameters
        ----------
        *args
            Arguments should be int, the ids of the target nodes
        """
        for arg in args:
            tgt_id = arg
            tgt_node = self.get_node_by_id(tgt_id)

            for parent_id in tgt_node.get_parent_ids:
                self.remove_parallel_edges((parent_id, tgt_id))

                # If the parent is an input removes it from the open digraph and its id from the inputs
                # to keep it well formed otherwise the input node would be left with no child
                if parent_id in self.inputs:
                    self.nodes.pop(parent_id)
                    self.inputs.remove(parent_id)

            for child_id in tgt_node.get_children_ids:
                self.remove_parallel_edges((tgt_id, child_id))

                # If the child is an output removes it from the open digraph and its id from the outputs
                # to keep it well formed otherwise the output node would be left with no parent
                if child_id in self.outputs:
                    self.nodes.pop(child_id)
                    self.inputs.remove(child_id)

            if tgt_id in self.inputs:
                self.inputs.remove(tgt_id)

            if tgt_id in self.outputs:
                self.outputs.remove(tgt_id)

            self.nodes.pop(tgt_id)

    @property
    def is_well_formed(self) -> None:
        """Verifies is the open digraph is well formed and returns None is so and

        Raises
        ------
        Exception
            Raises an exception if the open digraph isn't well formed with a description of the problem
        """
        # Checks if all intput nodes are in the graph, have no parents and have a single child of multiplicity 1
        for node_id in self.inputs:
            input_node = self.get_node_by_id(node_id)
            if not (input_node in self.get_nodes):
                raise Exception(f"Input node {input_node} isn't in the graph")
            if input_node.parents:
                raise Exception(f"Input node {input_node} has parents")
            if list(input_node.children.values()) != [1]:
                raise Exception(
                    f"Intput node {input_node} has more than 1 children or its multiplicity is greater than 1"
                )

        # Checks if all output nodes are in the graph, have no children and have a single parent of multiplicity 1
        for node_id in self.outputs:
            output_node = self.get_node_by_id(node_id)
            if not (output_node in self.get_nodes):
                raise Exception(f"Output node {input_node} isn't in the graph")
            if output_node.children:
                raise Exception(f"Output node {input_node} has children")
            if list(output_node.parents.values()) != [1]:
                raise Exception(
                    f"Output node {input_node} has more than 1 parent or its multiplicity is greater than 1"
                )

        # Checks if all the keys in nodes are paired with a node of id equal to the key
        for node_id in self.nodes:
            if self.nodes[node_id].id != node_id:
                raise Exception(f"A key of <id,node> in nodes is invalid")

        for node in self.get_nodes:
            # Checks if all the children of all the nodes have that same node as a parent with their respective multiplicity
            for parent_id, multi in node.parents.items():
                children = self.get_node_by_id(parent_id).children
                if not (node.id in children) or not (multi == children[node.id]):
                    raise Exception(
                        f"Node {parent_id} isn't a parent of node {node_id} or their multiplicity are different"
                    )

            # Checks if all the parents of all the nodes have that same node as a child with their respective multiplicity
            for child_id, multi in node.children.items():
                parents = self.get_node_by_id(child_id).parents
                if not (node.id in parents) or not (multi == parents[node.id]):
                    raise Exception(
                        f"Node {child_id} isn't a child of node {node_id} or their multiplicity are different"
                    )

    def add_input_node(self, child_id: int) -> int:
        # CHANGER LA DOC on return un id maintenant
        """Adds a new input node to the open digraph

        Parameters
        ----------
        child_id : int
            The id if the node which the new input node will point towards

        Raises
        ------
        Exception
            Raises an exception if the target child node is already an input or isn't in the open digraph
        """
        if child_id in self.inputs:
            raise Exception(f"the target node of id {child_id} is already an input")
        if not (child_id in self.nodes):
            raise Exception(f"the target node of id {child_id} isn't in the graph")
        node_id = self.new_id
        new_node = Node(node_id, "", {}, {child_id: 1})
        self.nodes[node_id] = new_node
        self.add_input_id(node_id)
        self.add_edge(node_id, child_id)
        return node_id

    def add_output_node(self, parent_id: int) -> int:
        # PAREIL CHANGER LA DOC
        """Adds a new output node to the open digraph

        Parameters
        ----------
        parent_id : int
            The id if the node which the new output node will pointed at by

        Raises
        ------
        Exception
            Raises an exception if the target parent node is already an output or isn't in the open digraph
        """
        if parent_id in self.outputs:
            raise Exception(f"the target node of id {parent_id} is already an output")
        if not (parent_id in self.nodes):
            raise Exception(f"the target node of id {parent_id} isn't in the graph")
        node_id = self.new_id
        new_node = Node(node_id, "", {parent_id: 1}, {})
        self.nodes[node_id] = new_node
        self.add_output_id(node_id)
        self.add_edge(parent_id, node_id)
        return node_id

    def fusion(self, src: int, tgt: int, new_label: str = None) -> None:
        for parent_id in self[tgt].get_parent_ids:
            self.add_edge(parent_id, src)
        for children_id in self[tgt].get_children_ids:
            self.add_edge(src, children_id)
        if new_label != None:
            self[src].set_label(new_label)
        self.remove_node_by_id(tgt)
