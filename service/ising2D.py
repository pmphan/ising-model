import numpy as np
import matplotlib.pyplot as plt

from typing import Any, Callable
from abc import ABC, abstractmethod

class Ising2D(ABC):

    def _init_lattice(self, N, M) -> np.ndarray[Any, np.dtype[np.int_]]:
        """
        Return a nxm array with random spin configuration.
        A = [ 00 01 02 ... 0m]
            [ 10 12 13 ... 1m]
            [ :  :  :  ... : ]
            [ n0 n1 n3 ... nm]
        """
        return np.random.choice([1, -1], [N, M]).astype('byte')

    @classmethod
    @abstractmethod
    def get_neighbors(cls, A, i, j):
        return np.array([])

    @classmethod
    @abstractmethod
    def get_lattice_size(cls, N: int, M: int):
        return N * M


    @classmethod
    def calculate_dE(cls, A: np.ndarray, i, j) -> int:
        neighbors = cls.get_neighbors(A, i, j)
        return A[i, j] * 2 * np.sum(neighbors)

    @classmethod
    def metropolis(cls, A: np.ndarray, kT: float, nstep : int=100_000, nyield=10):
        """
        Apply Metropolis method on configuration A with kT for nstep sweeps.
        """
        N = A.shape[0]
        M = A.shape[1]
        size = cls.get_lattice_size(N, M)
        if not nstep or nstep < 10:
            # Cap number of step at 100_000
            nstep = np.min([10 * size, 100_000])
        # Cap number of return array at 100
        if nyield > 100:
            nyield = 100
        # Shouldn't have more return array than number of step
        if nyield >= nstep:
            nyield = nstep
        # How many step in between each yield
        yield_per = np.ceil(nstep / nyield)
        for step in range(nstep):
            for _ in range(size):
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
        """
        Plot array A with title and return serialized image serialized
        with serialized_func.
        """
        if not title:
            title = f"Plot of array shaped {A.shape}"
        figure = plt.figure()
        plt.imshow(A)
        plt.title(title)
        serialized_plot = serialized_func(figure)
        plt.close(figure)
        return serialized_plot
