import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

def start_array(n, m):
    """
    Return a nxm array with random spin configuration.
    A = [ 00 01 02 ... 0m]
        [ 10 12 13 ... 1m]
        [ :  :  :  ... : ]
        [ n0 n1 n3 ... nm]
    """
    return np.random.choice([1,-1], [n,m])

def get_neighbors(A: npt.NDArray[np.int_], i: int, j: int):
    """
    Given array A and element A[i, j] on a 2D array,
    return its neighbors in the adjacent 4 grid, obeying
    torus-like boundary condition.

    Neighbor order: left, right, up, down.
    """
    n = A.shape[0]
    m = A.shape[1]
    return np.array((
        A[i, (j-1) % m], A[i, (j+1) % m],
        A[(i-1) % n, j], A[(i+1) % n, j]
    ))

def get_dE(A: npt.NDArray[np.int_], i, j):
    neighbors = get_neighbors(A, i, j)
    return A[i, j] * 2 * np.sum(neighbors)

def is_flippable(energy: int, T: float):
    """Check if lattice site is flippable with current energy."""
    return (energy < 0) or (np.random.random() <= np.exp(-energy/T))

def get_ising_array():
    """
    Run the Ising model on current lattice.
    """
    N = M = 10
    yield_every = 10
    step = 10*N*M
    A = start_array(N, M)
    kT = 2.0
    for st in range(step):
        for _ in range(N*M):
            i = np.random.randint(0, N)
            j = np.random.randint(0, M)
            dE = get_dE(A, i, j)
            if is_flippable(dE, kT):
                A[i, j] *= -1
        if st % yield_every == 0:
            yield A

def main():
    for array in get_ising_array():
        print(array)
    # Generate placeholder file
    A = np.ones([20, 20])
    plt.imshow(A)
    plt.title('20x20 placeholder lattice')
    plt.savefig('static/assets/placeholder.png', format='png', transparent=True)

if __name__ == "__main__":
    main()
