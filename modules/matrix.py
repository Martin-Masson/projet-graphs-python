from re import M
from typing import List
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
    
