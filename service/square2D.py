import numpy as np
from typing import Any

from .ising2D import Ising2D

class Square2D(Ising2D):
    def __init__(self, N: int, M: int, kT: float):
        self.N = N
        self.M = M
        self.kT = kT
        self.lattice = self._init_lattice(N, M)

    @classmethod
    def get_neighbors(cls, A: np.ndarray, i: int, j: int) -> np.ndarray[Any, np.dtype[np.int_]]:
        """
        Given array A and element A[i, j] on a 2D array,
        return its neighbors in the adjacent 4 grid, obeying
        torus-like boundary condition.

        Neighbor order: left, right, up, down.
        """
        N = A.shape[0]
        M = A.shape[1]
        return np.array((
            A[i, (j-1) % M],
            A[i, (j+1) % M],
            A[(i-1) % N, j],
            A[(i+1) % N, j]
        ))

    @classmethod
    def get_lattice_size(cls, N, M):
        return N*M
