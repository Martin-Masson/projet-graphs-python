from __future__ import annotations
from lib2to3.pgen2.token import OP
from msilib.schema import Component
from tkinter import N
from typing import Dict, List, Tuple
import itertools
import sys
import os

root = os.path.normpath(os.path.join(__file__, "./../.."))
sys.path.append(root)
from modules.matrix import *

Matrix = List[List[int]]

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

    def in_degree(self) -> int:
        degree = 0
        for parent_id in self.parents:
            degree += self.parents[parent_id]
        return degree
        
    def out_degree(self) -> int:
        degree = 0
        for child_id in self.children:
            degree += self.children[child_id]
        return degree
    
    def degree(self) -> int:
        return self.out_degree() + self.in_degree()
    

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
    def empty(cls) -> OpenDigraph:
        """Returns an empty open digraph"""
        return cls([], [], [])

    @classmethod
    def random(cls, n: int, bound: int, inputs: int = 0, outputs: int = 0, form: str = "free") -> OpenDigraph:
        """
        Doc
        Bien préciser ici les options possibles pour form !
        """
        if form == "free":
            digraph = cls.graph_from_adjacency_matrix(random_matrix(n, bound))
        elif form == "DAG":
            digraph = cls.graph_from_adjacency_matrix(random_matrix(n, bound, triangular=True))
        elif form == "oriented":
            digraph = cls.graph_from_adjacency_matrix(random_matrix(n, bound, oriented=True))
        elif form == "loop-free":
            digraph = cls.graph_from_adjacency_matrix(random_matrix(n, bound, null_diag=True))
        elif form == "undirected":
            digraph = cls.graph_from_adjacency_matrix(random_matrix(n, bound, symetric=True))
        elif form == "loop-free undirected":
            digraph = cls.graph_from_adjacency_matrix(random_matrix(n, bound, null_diag=True, symetric=True))
        
        for input in range(inputs):
            digraph.add_input_node(random.randint(0, len(digraph.nodes) - 1))
        for output in range(outputs):
            digraph.add_output_node(random.randint(0, len(digraph.nodes) - 1))

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

        print(lines)

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
        if self.nodes == {}:
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
        parents = {} if parents is None else None
        children= {} if children is None else None
        node_id = self.new_id()
        new_node = Node(node_id, label, parents, children)
        self.nodes[node_id] = new_node
        for parent in list(parents.keys()):
            for child in list(children.keys()):
                for multi in list(parents.values()):
                    self.add_edge(parent, node_id)
                for multi in list(children.values()):
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

            for parent_id in tgt_node.get_parent_ids():
                self.remove_parallel_edges((parent_id, tgt_id))

                # If the parent is an input removes it from the open digraph and its id from the inputs
                # to keep it well formed otherwise the input node would be left with no child
                if parent_id in self.inputs:
                    self.nodes.pop(parent_id)
                    self.inputs.remove(parent_id)

            for child_id in tgt_node.get_children_ids():
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
            if not (input_node in self.get_nodes()):
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
            if not (output_node in self.get_nodes()):
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

        for node in self.get_nodes():
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
            Raises an exception if the target parent node is already an output or isn't in the open digraph
        """
        if parent_id in self.outputs:
            raise Exception(f"the target node of id {parent_id} is already an output")
        if not (parent_id in self.nodes):
            raise Exception(f"the target node of id {parent_id} isn't in the graph")
        node_id = self.new_id()
        new_node = Node(node_id, "", {parent_id: 1}, {})
        self.nodes[node_id] = new_node
        self.add_output_id(node_id)
        self.add_edge(parent_id, node_id)

    def enumerate_digraph(self) -> Dict[int, int]:
        """Returns a dic that matches each node id to a unique integer between 0 and the number of nodes
        
        Returns
        ------
        A FINIR
        """
        node_ids = self.get_node_ids()
        return {node_id: n for node_id, n in zip(node_ids, range(len(node_ids)))}

    def adjency_matrix(self) -> Matrix:

        n = len(self.nodes)
        matrix = []
        for i in range(n):
            matrix.append([0]*n)
        dic = self.enumerate_digraph()
        
        for node_id in dic:
            node = self.get_node_by_id(node_id)
            children = node.children
            for child_id in children:
                matrix[dic[node_id]][dic[child_id]] = children[child_id]
        return matrix

    def save_sa_dot_file(self, path: str, verbose: bool = False) -> None:
        with open(path, "w") as file:
            file.write("digraph G {\n")

            for node_id in self.nodes:
                node = self.get_node_by_id(node_id)
                label = node.get_label()

                if node_id in self.inputs:
                    file.write(f"    v{node_id} [color=blue];\n")
                if node_id in self.outputs:
                    file.write(f"    v{node_id} [color=red];\n")

                if verbose:
                    file.write(f"    v{node_id} [label=\"{label} id={node_id}\"];\n")
                else:
                    file.write(f"    v{node_id} [label=\"{label}\"];\n")
                
                for child_id in node.children:
                    for multiplicity in range(node.children[child_id]):
                        file.write(f"    v{node_id} -> v{child_id};\n")

            file.write("}")

    def display(self, verbose: bool = False) -> None:
        self.save_sa_dot_file("digraph.dot", verbose=verbose)
        os.system("dot -Tpdf digraph.dot -o digraph.pdf")

    def sub_is_cyclic(self, *args: List[int]) -> bool:
        if self.nodes == {}:
            return False
        
        leaves = []
        for node_id in self.nodes:
            node = self.get_node_by_id(node_id)
            if node.out_degree() == 0:
                leaves.append(node)
            
        if not leaves:
            return True

        for leaf in leaves.copy():
            parents = self.get_nodes_by_ids(leaf.get_parent_ids())
            for parent in parents:
                if len(parent.children) == 1:
                    leaves.append(parent)
            leaves.remove(leaf)
            self.remove_node_by_id(leaf.get_id())
        
        return self.sub_is_cyclic(leaves)

        
    def is_cyclic(self) -> bool:
        

        digraph = self.copy()
        for input in self.inputs:
            digraph.remove_node_by_id(input)
        for output in self.outputs:
            digraph.remove_node_by_id(output)
        
        return digraph.sub_is_cyclic()

    def min_id(self) -> int:
        return min(self.nodes)

    def max_id(self) -> int:
        return max(self.nodes)

    def shift_indices(self, n: int) -> None:
        for id in self.nodes:
            node = self.get_node_by_id(id)
            node.set_id(id + n)
            node.set_parent_ids({id + n: multi for id, multi in node.parents.items()})
            node.set_children_ids({id + n: multi for id, multi in node.children.items()})          
        
        for i in range(len(self.inputs)):
            self.inputs[i] += n
            
        for j in range(len(self.outputs)):
            self.outputs[j] += n
        
        self.nodes = {node.id: node for node in self.nodes.values()}

    def iparallel(self, *args: OpenDigraph) -> None:
        "A TESTER"
        for g in args:
            g.shift_indices(self.max_id() - g.min_id() + 1)
            self.inputs.extend(g.inputs)
            self.outputs.extend(g.outputs)
            for node in g.get_nodes():
                self.nodes[node.id] = node

    def parallel(self, g: OpenDigraph) -> OpenDigraph:
        "A TESTER"
        output = self.copy()
        output.iparallel(g)
        return output

    def icompose(self, g: OpenDigraph) -> None:
        g.shift_indices(self.max_id() - g.min_id() + 1)
        if len(self.outputs) != len(g.inputs):
            raise Exception(f"Length of outputs of self are different from inputs of g")

        for node in g.get_nodes():
            self.nodes[node.id] = node
            
        for i in range(len(self.outputs)):
            node_o = self.get_node_by_id(self.outputs[i])
            node_i = self.get_node_by_id(g.inputs[i])
            self.add_edge(node_o.get_parent_ids()[0], node_i.get_children_ids()[0])
            self.remove_node_by_id(node_o.id, node_i.id)

        self.outputs = g.outputs

    def compose(self, g: OpenDigraph) -> OpenDigraph:
        output = self.copy()
        output.icompose(g)
        return output
    

    def dfs(self,visited, node, component):
        if node not in visited:
            visited.add(node)
            component.append(node.id)
            voisins = node.get_parent_ids() + node.get_children_ids()
            for voisin in voisins:
                self.dfs(visited,self.get_node_by_id(voisin),component)
    
    
    def connected_components_v2(self):
        visited = set()
        output = {}
        components = []
        for id in self.inputs:
            node = self.get_node_by_id(id)
            l = []
            self.dfs(visited, node, l)
            components.append(l)
        components = list(filter(lambda a: a != [], components))
        nb_component = len(components)
        k = 0
        for component in components:
            component.sort()
            for id in component:
                output[id] = k
            k += 1
        return nb_component,output
    
    '''
    def connected_components_v1(self):
        mat = self.adjency_matrix()
        output = {}
        components = []
        for input_id in self.inputs:
            current_id = input_id
            # on boucle sur les id
            # si l'id est pas dans aucun des component, on l'ajoute
            # dans un nouveau component ajouté à components
            #   on recommence sur son enfant
            # si l'id est dans components, on break et on passe au
            # prochain id
                       
            for component in components:
                if current_id in component:
                    break
            components.append([current_id])
            
            components[i].append([input_id])

    def dijkstra( src, direction=None) :
        '''
