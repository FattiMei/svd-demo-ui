import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from time import perf_counter
from matplotlib.widgets import Slider

matplotlib.use("Qt5Agg")


def truncate_to_k_singular_values(U, Sigma, Vh, k):
    return (U[:,:k] * Sigma[:k]) @ Vh[:k, :]


def truncate_to_k_singular_values_optimized(merged, Vh, k):
    return merged[:,:k] @ Vh[:k, :]


# TODO: can I tell if I'm running from ipython?
# TODO: add memory footprint
# TODO: add pooling for improving computation times


if __name__ == '__main__':
    is_interactive = sys.argv[0].split('/')[-1] == 'ipython'

    if len(sys.argv) == 1 or is_interactive:
        print('[INFO]: no image provided, loading default image')
        name = 'resources/einstein.jpg'
    else:
        name = sys.argv[1]

    print(f'[INFO]: loading {name}')
    image = Image.open(name)
    name = name.split('/')[-1]
    grayscale = image.convert(mode='L')
    matrix = np.array(grayscale, dtype=np.float32)

    print('[INFO]: performing SVD decomposition')
    start_time = perf_counter()
    U, Sigma, Vh = np.linalg.svd(matrix, full_matrices=False)
    end_time = perf_counter()
    print(f'[INFO]: computation time: {end_time - start_time:.2f}')

    # siccome viene spesso ripetuto il calcolo di U * Sigma,
    # decido di precalcolarlo una volta per tutte
    merged = U * Sigma

    singular_values_squared = Sigma**2
    explained_variance = np.cumsum(singular_values_squared)
    explained_variance /= explained_variance[-1]

    k = 3

    # ------------------------ interactive section -----------------------------
    fig = plt.figure(figsize=(10,5))
    gs = fig.add_gridspec(2, 3, height_ratios=[1,0.1])

    ax = [
        fig.add_subplot(gs[0,0]),
        fig.add_subplot(gs[0,1]),
        fig.add_subplot(gs[0,2]),
    ]

    ax[0].set_title(f'{name} (original)')
    ax[0].set_axis_off()
    ax[0].imshow(matrix, cmap='gray')

    ax[1].set_title(f'{k} singular values')
    ax[1].set_axis_off()
    compressed = ax[1].imshow(
        truncate_to_k_singular_values_optimized(merged, Vh, k),
        cmap='gray'
    )

    ax[2].set_title('Explained variance')
    ax[2].set_xlabel('k')
    ax[2].plot(explained_variance)
    point = ax[2].plot([k], [explained_variance[k]], color='red', marker='o', markersize=5)

    sv_slider = Slider(
        ax=fig.add_subplot(gs[1,:]),
        label='',
        valmin=1,
        valmax=min(30,len(Sigma)),
        valinit=k,
        valstep=1
    )

    def update(val):
        global k
        k = val

        ax[1].set_title(f'{k} singular values')
        compressed.set_data(truncate_to_k_singular_values_optimized(merged, Vh, k))

        point[0].set_xdata([k])
        point[0].set_ydata([explained_variance[k]])


    sv_slider.on_changed(update)
    plt.tight_layout()
    plt.show()
