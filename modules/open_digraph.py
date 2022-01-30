from __future__ import annotations
from typing import Dict, List


class Node:
    def __init__(
        self,
        identity: int,
        label: str,
        parents: Dict[int, int],
        children: Dict[int, int],
    ) -> Node:
        """
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        """

        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children

    def __str__(self) -> str:
        return (
            "Node("
            + str(self.id)
            + ", "
            + self.label
            + ", "
            + str(self.parents)
            + ", "
            + str(self.children)
            + ")"
        )

    def __repr__(self) -> str:
        return str(self)

    def copy(self) -> Node:
        """Returns a copy of the node"""
        return Node(self.id, self.label, self.parents, self.children)

    def get_id(self) -> int:
        """Returns the id of the node"""
        return self.id

    def get_label(self) -> str:
        """Returns the label of the node"""
        return self.label

    def get_parent_ids(self) -> List[int]:
        """Returns a list of the ids of all the parents of the node"""
        return list(self.parents.keys())

    def get_children_ids(self) -> List[int]:
        """Returns a list of the ids of all the children of the node"""
        return list(self.children.keys())

    def set_id(self, new_id: int) -> None:
        """Sets the id of the node to new_id"""
        self.id = new_id

    def set_label(self, new_label: str) -> None:
        """Sets the label of the node to new_label"""
        self.label = new_label

    def set_parent_ids(self, new_parents: Dict[int, int]) -> None:
        """Sets the parents of the node to new_parents"""
        self.parents = new_parents

    def set_children_ids(self, new_children: Dict[int, int]) -> None:
        """Sets the children of the node to new_children"""
        self.children = new_children

    def add_child_id(self, new_child_id: int, multi: int = 1) -> None:
        """Adds a new child to the node of id new_child_id and multiplicty multi (default is 1)"""
        self.children[new_child_id] = multi

    def add_parent_id(self, new_parent_id: int, multi: int = 1) -> None:
        """Adds a new parent to the node of id new_parent_id and multiplicty multi (default is 1)"""
        self.parents[new_parent_id] = multi

    def remove_parent_once(self, parent_id: int) -> None:
        """Reduces by 1 the multiplicty of the node's parent of id parent_id or removes it if the multiplicity was 1"""
        if self.parents[parent_id] > 1:
            self.parents[parent_id] -= 1
        else:
            del self.parents[parent_id]

    def remove_child_once(self, child_id: int) -> None:
        """Reduces by 1 the multiplicty of the node's child of id child_id or removes it if the multiplicity was 1"""
        if self.children[child_id] > 2:
            self.children[child_id] -= 1
        else:
            del self.children[child_id]

    def remove_parent_id(self, parent_id: int) -> None:
        """Removes the parent of id parent_id from the node's parents"""
        del self.parents[parent_id]

    def remove_child_id(self, child_id: int) -> None:
        """Removes the child of id child_id from the node's children"""
        del self.children[child_id]


class OpenDigraph:  # for open directed graph
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

    def __str__(self) -> str:
        output = ""
        for node in list(self.nodes.values()):
            output += "n" + str(node.id) + " = " + str(node) + "\n"
        return output

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def empty(self) -> OpenDigraph:
        """Returns an empty open digraph"""
        return OpenDigraph([], [], [])

    def copy(self) -> OpenDigraph:
        """Returns a copy of the open digraph"""
        return OpenDigraph(self.inputs, self.outputs, list(self.nodes.values()))

    def get_input_ids(self) -> List[int]:
        """Returns the inputs of the open digraph"""
        return self.inputs

    def get_output_ids(self) -> List[int]:
        """Returns the outputs of the open digraph"""
        return self.outputs

    def get_id_node_map(self) -> Dict[int, Node]:
        """Returns the nodes of the open digraph"""
        return self.nodes

    def get_nodes(self) -> List[Node]:
        """Returns a list of all the nodes in the open digraph"""
        return list(self.nodes.values())

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

    def new_id(self) -> int:
        """Returns a new id unused by any node of the open digraph"""
        return len(self.nodes)

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
        parents: Dict[int, int] = {},
        children: Dict[int, int] = {},
    ) -> None:
        """Adds a new node to the open digraph

        Optionnal Parameters
        ----------
        label : str (default "")
            The label of the new node
        parents : Dict[int, int] (default {})
            The parents of the new node
        children : Dict[int, int] (default {})
            The children of the new node
        """
        node_id = self.new_id()
        new_node = Node(node_id, label, parents, children)
        self.nodes[node_id] = new_node
        for parent, child in zip(list(parents.keys()), list(children.keys())):
            self.add_edge(parent, node_id)
            self.add_edge(node_id, child)

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

            for parent in tgt_node.parents:
                # Removing the node from the parent node's children
                self.get_node_by_id(parent).remove_child_id(tgt_id)

                # If the parent is an input removes it from the open digraph and its id from the inputs
                # to keep it well formed otherwise the input node would be left with no child
                if parent in self.inputs:
                    self.nodes.pop(parent)
                    self.inputs.remove(parent)

            for child in tgt_node.children:
                # Removing the node from the child node's parents
                self.get_node_by_id(child).remove_parent_id(tgt_id)

                # If the child is an output removes it from the open digraph and its id from the outputs
                # to keep it well formed otherwise the output node would be left with no parent
                if child in self.outputs:
                    self.nodes.pop(child)
                    self.inputs.remove(child)

            # If the target node is an input removes its id from the inputs
            if tgt_id in self.inputs:
                self.inputs.remove(tgt_id)

            # If the target node is an ouput removes its id from the outputs
            if tgt_id in self.outputs:
                self.outputs.remove(tgt_id)

            # Removes the node from the open digraph
            self.nodes.pop(tgt_id)

    def is_well_formed(self) -> None:
        """Verifies is the open digraph is well formed and returns None is so and

        Raises
        ------
        Exception
            Raises an exception if the open digraph isn't well formed with a description of the problem
        """
        # Checking if all intput nodes are in the graph, have no parents and have a single child of multiplicity 1
        for node_id in self.inputs:
            input_node = self.get_node_by_id(node_id)
            if not (input_node in self.get_nodes()):
                raise Exception(f"Input node {input_node} isn't in the graph")
            if input_node.parents:
                raise Exception(f"Input node {input_node} has parents")
            if list(input_node.children.values()) != [1]:
                raise Exception(
                    f"Intput node {input_node} has more than 1 children or its multiplicity is greater than 1"
                )

        # Checking if all output nodes are in the graph, have no children and have a single parent of multiplicity 1
        for node_id in self.outputs:
            output_node = self.get_node_by_id(node_id)
            if not (output_node in self.get_nodes()):
                raise Exception(f"Output node {input_node} isn't in the graph")
            if output_node.children:
                raise Exception(f"Output node {input_node} has children")
            if list(output_node.parents.values()) != [1]:
                raise Exception(
                    f"Output node {input_node} has more than 1 parent or its multiplicity is greater than 1"
                )

        # Checking if all the keys in nodes are paired with a node of id equal to the key
        for node_id in self.nodes:
            if self.nodes[node_id].id != node_id:
                raise Exception(f"A key of <id,node> in nodes is invalid")

        for node in self.get_nodes():
            # Checking if all the children of all the nodes have that same node as a parent with their respective multiplicity
            for parent_id, multi in node.parents.items():
                children = self.get_node_by_id(parent_id).children
                if not (node.id in children) or not (multi == children[node.id]):
                    raise Exception(
                        f"node {parent_id} isn't a parent of node {node_id} or their multiplicity are different"
                    )

            # Checking if all the parents of all the nodes have that same node as a child with their respective multiplicity
            for child_id, multi in node.children.items():
                parents = self.get_node_by_id(child_id).parents
                if not (node.id in parents) or not (multi == parents[node.id]):
                    raise Exception(
                        f"node {child_id} isn't a child of node {node_id} or their multiplicity are different"
                    )

    def add_input_node(self, child_id: int) -> None:
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
        node_id = self.new_id()
        new_node = Node(node_id, "", {}, {child_id: 1})
        self.nodes[node_id] = new_node
        self.add_input_id(node_id)
        self.add_edge(node_id, child_id)

    def add_output_node(self, parent_id: int) -> None:
        """Adds a new output node to the open digraph

        Parameters
        ----------
        parent_id : int
            The id if the node which the new output node will pointed at by

        Raises
        ------
        Exception
            Raises an exception if the target parent node is already an output or isn't in the open digraph"""
        if parent_id in self.outputs:
            raise Exception(f"the target node of id {parent_id} is already an output")
        if not (parent_id in self.nodes):
            raise Exception(f"the target node of id {parent_id} isn't in the graph")
        node_id = self.new_id()
        new_node = Node(node_id, "", {parent_id: 1}, {})
        self.nodes[node_id] = new_node
        self.add_output_id(node_id)
        self.add_edge(parent_id, node_id)
