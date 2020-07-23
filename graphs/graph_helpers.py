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

def visualize_single_channel(title, image):
    """Visualize a 2D array using matplotlib.
    All inputs values should be normalized 0.0-1.0.

    Args:
        title (str): Name of image we're visualizing.
        image (np.ndarray): Image we're visualizing. Shape should be `(rows, cols)`.
    """
    assert type(title) == str, "Title not a string!"
    assert len(image.shape) == 2, "Image array not 2D!"

    # Visualize image
    # We manually set the black value with `vmin`, and the white value with `vmax`
    plt.imshow(image, vmin=0.0, vmax=1.0, cmap="gray")

    # Give our plot a title -- this is purely cosmetic!
    plt.title(f"{title}, shape={image.shape}")

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
            p = [l // m, l % m]
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
