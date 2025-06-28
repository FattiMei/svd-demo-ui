import PIL
import numpy as np


def load_image_from_argv(argv: list[str], default: str = None, dtype = np.float32) -> tuple[str, np.ndarray]:
    is_interactive = argv[0].split('/')[-1] == 'ipython'

    if len(argv) == 1 or is_interactive:
        print('[INFO]: no image provided, loading default image')

        if default is None:
            raise ValueError('Supply a default image path')

        name = default

    else:
        name = argv[1]

    return load_image_from_filename(name, dtype)


def load_image_from_filename(filename: str, dtype) -> tuple[str, np.ndarray]:
    print(f'[INFO]: loading {filename}')
    name = filename.split('/')[-1]
    image = PIL.Image.open(filename)
    grayscale = image.convert(mode='L')

    return name, np.array(grayscale, dtype=dtype)
