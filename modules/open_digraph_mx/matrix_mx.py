from typing import Dict, List
import itertools
import random

Matrix = List[List[int]]


def random_int_list(n: int, bound: int) -> List[int]:
    return [random.randint(0, bound) for i in range(n)]


def random_matrix(
    n: int,
    bound: int,
    null_diag: bool = False,
    symetric: bool = False,
    oriented: bool = False,
    triangular: bool = False,
) -> Matrix:
    matrix = []
    for i in range(n):
        matrix.append(random_int_list(n, bound))

    for i, j in itertools.product(range(n), range(n)):
        if null_diag:
            matrix[i][i] = 0
        if triangular:
            if i > j:
                matrix[i][j] = 0
        elif oriented:
            if matrix[i][j] != 0:
                matrix[j][i] = 0
        elif symetric:
            matrix[i][j] = matrix[j][i]

    return matrix


def print_matrix(mat: Matrix):
    print("", end="    ")
    for i in range(len(mat)):
        print(i, end="  ")
    print("")
    print("")
    for i, line in enumerate(mat):
        print(i, end="   ")
        for val in line:
            print(val, end="  ")
        print("")


class matrix_mx:
    @property
    def enumerate_digraph(self) -> Dict[int, int]:
        """Returns a dic that matches each node id to a unique integer between 0 and the number of nodes

        Returns
        ------
        A FINIR
        """
        node_ids = self.get_node_ids
        return {node_id: n for node_id, n in zip(node_ids, range(len(node_ids)))}

    @property
    def adjency_matrix(self) -> Matrix:
        n = len(self.nodes)
        matrix = []
        for i in range(n):
            matrix.append([0] * n)
        dic = self.enumerate_digraph

        for node_id in dic:
            node = self.get_node_by_id(node_id)
            children = node.children
            for child_id in children:
                matrix[dic[node_id]][dic[child_id]] = children[child_id]
        return matrix

    """
    def random_int_matrix
    """
