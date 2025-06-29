import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from time import perf_counter
from matplotlib.widgets import Slider

import common


if __name__ == '__main__':
    args = common.parse_args(version='matplotlib')
    print(args)

    filename = 'resources/cameraman.jpg' if args.image is None else args.image
    name, matrix = common.load_image_from_filename(filename, precision=args.precision)

    U, Sigma, Vh, explained_variance = common.compute_svd_quantities(matrix)

    k = 3
    max_singular_values = min(args.max_singular_values, Sigma.size)

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
        common.truncate_to_k_singular_values(U, Sigma, Vh, k),
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
        valmax=max_singular_values,
        valinit=k,
        valstep=1
    )

    def update(val):
        global k
        k = val

        ax[1].set_title(f'{k} singular values')
        compressed.set_data(common.truncate_to_k_singular_values(U, Sigma, Vh, k))

        point[0].set_xdata([k])
        point[0].set_ydata([explained_variance[k]])


    sv_slider.on_changed(update)
    plt.tight_layout()
    plt.show()
