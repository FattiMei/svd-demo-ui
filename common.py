import sys
import PIL
import argparse
import numpy as np

from time import perf_counter


def is_interactive() -> bool:
    import __main__ as main
    return not hasattr(main, '__file__')


def parse_args(version: str):
    parser = argparse.ArgumentParser(
        prog=f'svd-demo-ui (version {version})',
        description="Performs image compression using the SVD algorithm, let's the user decide how many singular values in the final image",
        epilog='Click on the slider and see the effect!'
    )
    group = parser.add_mutually_exclusive_group()

    parser.add_argument('--image', help='Image file to be processed')
    parser.add_argument('--max-singular-values', type=int, help='Maximum number of singular values for compression')

    group.add_argument('--fp32', help='Performs the computation in float32', action='store_true')
    group.add_argument('--fp64', help='Performs the computation in float64 (default)', action='store_true')

    # when the program gets launched from ipython, there is collision
    # between the ipython command line arguments and the args related
    # to this application. Duct tape solution: we remove them.
    if is_interactive():
        sys.argv = ['']

    args = parser.parse_args()
    args.precision = np.float32 if args.fp32 else np.float64

    return args


def load_image_from_filename(filename: str, precision) -> tuple[str, np.ndarray]:
    print(f'[INFO]: loading {filename}')
    name = filename.split('/')[-1]
    image = PIL.Image.open(filename)
    grayscale = image.convert(mode='L')

    return name, np.array(grayscale, dtype=precision)


def compute_svd_quantities(matrix: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    print('[INFO]: performing SVD decomposition')

    start_time = perf_counter()
    U, Sigma, Vh = np.linalg.svd(matrix, full_matrices=False)
    end_time = perf_counter()

    print(f'[INFO]: computation time: {end_time - start_time:.2f}')

    explained_variance = np.cumsum(Sigma**2)
    explained_variance /= explained_variance[-1]

    return U, Sigma, Vh, explained_variance


def truncate_to_k_singular_values(U, Sigma, Vh, k):
    return (U[:,:k] * Sigma[:k]) @ Vh[:k, :]
