import numpy as np
import matplotlib.pyplot as plt
from typing import Any, Callable

class Ising2D:
    def __init__(self, N: int, M: int, kT: float):
        self.N = N
        self.M = M
        self.kT = kT
        self.lattice = self.init_lattice()

    def init_lattice(self) -> np.ndarray[Any, np.dtype[np.int_]]:
        """
        Return a nxm array with random spin configuration.
        A = [ 00 01 02 ... 0m]
            [ 10 12 13 ... 1m]
            [ :  :  :  ... : ]
            [ n0 n1 n3 ... nm]
        """
        return np.random.choice([1, -1], [self.N, self.M]).astype('byte')

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
    def calculate_dE(cls, A: np.ndarray, i, j) -> int:
        neighbors = cls.get_neighbors(A, i, j)
        return A[i, j] * 2 * np.sum(neighbors)

    @classmethod
    def metropolis(cls, A: np.ndarray, kT: float, nstep : int=100_000, nyield=10):
        N = A.shape[0]
        M = A.shape[1]
        if not nstep or nstep < 10:
            # Cap number of step at 100_000
            nstep = np.min([10 * N * M, 100_000])
        # Cap number of return array at 10
        if nyield > 50:
            nyield = 50
        # Shouldn't have more return array than number of step
        if nyield >= nstep:
            nyield = nstep

        # How many step in between each yield
        yield_per = np.ceil(nstep / nyield)
        for step in range(nstep):
            for _ in range(N*M):
                i = np.random.randint(0, N)
                j = np.random.randint(0, M)
                dE = cls.calculate_dE(A, i, j)
                # Flip spin based on some probability
                if (dE < 0) or (np.random.random() < np.exp(-dE/kT)):
                    A[i, j] *= -1

            if step % yield_per == 0:
                yield A, step

        # Return final result
        yield A, -1

    @classmethod
    def plot_lattice(cls, A, title, serialized_func: Callable):
        if not title:
            title = f"Plot of array shaped {A.shape}"
        figure = plt.figure()
        plt.imshow(A)
        plt.title(title)
        serialized_plot = serialized_func(figure)
        plt.close(figure)
        return serialized_plot
