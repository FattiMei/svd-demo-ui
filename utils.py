import PIL
import argparse
import numpy as np


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

    args = parser.parse_args()
    args.precision = np.float32 if args.fp32 else np.float64

    return args


def load_image_from_filename(filename: str, precision) -> tuple[str, np.ndarray]:
    print(f'[INFO]: loading {filename}')
    name = filename.split('/')[-1]
    image = PIL.Image.open(filename)
    grayscale = image.convert(mode='L')

    return name, np.array(grayscale, dtype=precision)
