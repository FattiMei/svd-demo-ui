import sys
import numpy as np
from PIL import Image
from time import perf_counter

import pygame
from OpenGL.GL import *
from pygame.locals import *


def truncate_to_k_singular_values(U, Sigma, Vh, k):
    return (U[:,:k] * Sigma[:k]) @ Vh[:k, :]


def truncate_to_k_singular_values_optimized(merged, Vh, k):
    return merged[:,:k] @ Vh[:k, :]


def resize_image(shape: tuple[int, int], max_dim: int):
    c = max_dim / max(shape)
    return tuple(np.floor(c * np.array(shape)))


def generate_layout(window_shape: tuple[int, int], image_shape: tuple[int, int], margin_frac: float = 0.05, slider_height: int = 50):
    margin = np.floor(margin_frac * np.array(window_shape))

    slider_width = window_shape[0] - 2*margin[0]
    slider_rect = pygame.rect.Rect(margin[0], window_shape[1] - margin[1] - slider_height, slider_width, slider_height)

    bbox_width = (window_shape[0] - 3*margin[0]) / 2
    bbox_height = window_shape[1] - 3*margin[1] - slider_height

    # this is an horizontal image
    if image_shape[0] >= image_shape[1]:
        new_height = (bbox_width / image_shape[0]) * image_shape[1]

        bbox_hor_offset = margin[0]
        bbox_ver_offset = margin[1] + (bbox_height - new_height)/2
        bbox_height = new_height

    else:
        new_width = (bbox_height / image_shape[1]) * image_shape[0]

        bbox_hor_offset = margin[0] + (new_width - bbox_width)/2
        bbox_ver_offset = margin[1]
        bbox_width = new_width

    left_bbox_rect = pygame.rect.Rect(
        bbox_hor_offset,
        bbox_ver_offset,
        bbox_width,
        bbox_height
    )

    right_bbox_rect = pygame.rect.Rect(
        window_size[0] - left_bbox_rect.x - left_bbox_rect.w,
        left_bbox_rect.y,
        left_bbox_rect.w,
        left_bbox_rect.h
    )

    return slider_rect, left_bbox_rect, right_bbox_rect


if __name__ == '__main__':
    is_interactive = sys.argv[0].split('/')[-1] == 'ipython'

    if len(sys.argv) == 1 or is_interactive:
        print('[INFO]: no image provided, loading default image')
        name = 'resources/cameraman.jpg'
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
    compute_compressed_matrix = lambda k: truncate_to_k_singular_values_optimized(merged, Vh, k)

    singular_values_squared = Sigma**2
    explained_variance = np.cumsum(singular_values_squared)
    explained_variance /= explained_variance[-1]

    k = 3

    # ------------------------ interactive section -----------------------------
    window_size = (600, 600)

    pygame.init()
    screen = pygame.display.set_mode(window_size, DOUBLEBUF | RESIZABLE)
    clock  = pygame.time.Clock()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        window_size = screen.get_size()
        slider_rect, left_bbox_rect, right_bbox_rect = generate_layout(window_size, matrix.shape)

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, color=(0,255,255), rect=slider_rect)
        pygame.draw.rect(screen, color=(0,255,255), rect=left_bbox_rect)
        pygame.draw.rect(screen, color=(0,255,255), rect=right_bbox_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
