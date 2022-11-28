import numpy as np
from typing import Any

from .ising2D import Ising2D

class Triangle2D(Ising2D):
    def __init__(self, N: int, kT: float):
        self.N = N
        self.kT = kT
        self.lattice = self._init_lattice(N)

    def _init_lattice(self, N) -> np.ndarray[Any, np.dtype[np.int_]]:
        return np.tril(super()._init_lattice(N, N))

    @classmethod
    def get_neighbors(cls, A, i, j):
        j = j % (i+1)
        N = A.shape[0]
        # center
        if 1 < i < N - 1 and 0 < j < i:
            return np.array([A[i - 1][j - 1],
                            A[i - 1][j],
                            A[i][j - 1],
                            A[i][j + 1],
                            A[i + 1][j],
                            A[i + 1][j + 1]])

        # left side central
        elif 0 < i < N - 1 and j == 0:
            return np.array([A[i - 1][0],
                             A[i][1],
                             A[i + 1][0],
                             A[i + 1][1],
                             A[i][i],
                             A[i - 1][i - 1]])

        # right side central
        elif 0 < i < N - 1 and j == i:
            return np.array([A[i - 1][i - 1],
                             A[i - 1][0],
                             A[i][i - 1],
                             A[i][0],
                             A[i + 1][i],
                             A[i + 1][i + 1]])

        # bottom side central
        elif i == N - 1 and 0 < j < i:
            return np.array([A[i - 1][j - 1],
                             A[i - 1][j],
                             A[i][j - 1],
                             A[i][j + 1],
                             A[0][0],
                             A[0][0]])

        # very top
        elif i == 0:
            return np.array([A[1][0],
                             A[1][1],
                             A[N - 1][0],
                             A[N - 1][N - 1],
                             A[N - 1][1],
                             A[N - 1][N - 2]])
        # bottom left
        elif i == N - 1 and j == 0:
            return np.array([A[i - 1][0],
                             A[i - 1][i - 1],
                             A[i][1],
                             A[i][i],
                             A[0][0],
                             A[0][0]])

        # bottom right
        elif i == N - 1 and (j == i):
            return np.array([A[i - 1][0],
                             A[i - 1][i - 1],
                             A[i][0],
                             A[i][i - 1],
                             A[0][0],
                             A[0][0]])

    @classmethod
    def get_lattice_size(cls, N, M):
        return round((N*M) / 2)
