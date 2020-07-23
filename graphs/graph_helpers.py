import numpy as np
import matplotlib.pyplot as plt

def default_cmap(x):
    if x == 1:
        return [0, 255, 0]
    else:
        return [255, 0, 0]
    
def colored(A, cmap):
    im = np.zeros((A.shape[0], A.shape[1], 3), dtype=np.int)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            im[i, j] = cmap(A[i, j])
    return im

def visualize_adjacency(title, A):
    """Visualize an adjacency matrix using matplotlib.

    Args:
        title (str): Name of image we're visualizing.
        A (np.ndarray): Adjacency matrix we're visualizing.
    """
    assert type(title) == str, "Title not a string!"
    assert len(A.shape) == 2, "Image array not 2D!"
    
    plt.figure(figsize=(7, 7))

    # Visualize adjacency matrix
    # We manually set the black value with `vmin`, and the white value with `vmax`
    plt.imshow(A, vmin=0.0, vmax=1.0, cmap="gray")

    # Give our plot a title -- this is purely cosmetic!
    plt.title(f"{title}, shape={A.shape}")

    # Show image
    plt.show()

def visualize_map(title, M, A=None, start=None, end=None, cmap=default_cmap):
    """Visualize a 2D array using matplotlib.

    Args:
        title (str): Name of map we're visualizing.
        M (np.ndarray): Map we're visualizing. Shape should be `(rows, cols)`.
        A (np.ndarray): Adjacency matrix of graph.
    """
    assert type(title) == str, "Title not a string!"
    assert len(M.shape) == 2, "Map array not 2D!"
    
    plt.imshow(colored(M, cmap))
    if start is not None:
        plt.scatter(start[0], start[1], color="blue", label="start")
    if end is not None:
        plt.scatter(end[0], end[1], color="yellow", label="end")

        
    if A is not None:
        m, n = M.shape
        
        def ids(l):
            p = [l // n, l % n]
            return p

        def flip(t):
            return [t[1], t[0]]

        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                if A[i, j]:
                    # print(f"({i}, {j}) {ids(i)} -> {ids(j)}")
                    icoords = flip(ids(i))
                    jcoords = flip(ids(j))
                    x = [icoords[0], jcoords[0]]
                    y = [icoords[1], jcoords[1]]
                    plt.scatter(ids(i)[1], ids(i)[0], color="black")#, label=f"{i}")
                    plt.plot(x, y, color="black", alpha=0.5)#, label=f"{i} -> {j}")
                    
    if start or end:
        plt.legend()
        
    plt.title(title)
    plt.show()

def visualize_costs(title, M, costs, start=None, end=None):
    m, n = M.shape
    C = np.zeros_like(M)
    for i in range(m):
        for j in range(n):
            C[i, j] = costs[i * n + j]
    
    if start is not None:
        plt.scatter(start[1], start[0], color="blue", label="start")
    if end is not None:
        plt.scatter(end[1], end[0], color="yellow", label="end")
        
    plt.imshow(C)
    if start or end:
        plt.legend()
    plt.title(title)
    plt.show()
    
def plot_path(M, path):
    m, n = B.shape
    plt.imshow(colored(B, default_cmap))
    
    def ids(l):
        p = [l // m, l % m]
        return p
    
    def flip(t):
        return [t[1], t[0]]
    
    for i in range(len(p)-1):
        u, v = p[i], p[i+1]
        
        ucoords = flip(ids(u))
        vcoords = flip(ids(v))
        x = [ucoords[0], vcoords[0]]
        y = [ucoords[1], vcoords[1]]
        plt.plot(x, y, color="black", alpha=0.5)#, label=f"{i} -> {j}")