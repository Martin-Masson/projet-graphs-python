from __future__ import annotations
from copy import deepcopy
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

    @property
    def copy(self) -> Node:
        """Returns a copy of the node"""
        return deepcopy(self)

    @property
    def get_id(self) -> int:
        """Returns the id of the node"""
        return self.id

    @property
    def get_label(self) -> str:
        """Returns the label of the node"""
        return self.label

    @property
    def get_parent_ids(self) -> List[int]:
        """Returns a list of the ids of all the parents of the node"""
        return list(self.parents.keys())

    @property
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

    @property
    def in_degree(self) -> int:
        degree = 0
        for parent_id in self.parents:
            degree += self.parents[parent_id]
        return degree

    @property
    def out_degree(self) -> int:
        degree = 0
        for child_id in self.children:
            degree += self.children[child_id]
        return degree

    @property
    def degree(self) -> int:
        return self.out_degree + self.in_degree
