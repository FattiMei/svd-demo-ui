import sys
import numpy as np
from PIL import Image
from time import perf_counter

import common
import pygame


def make_grayscale_surface(arr: np.ndarray) -> pygame.surface.Surface:
    return pygame.surfarray.make_surface(
        np.stack([arr]*3, axis=-1).swapaxes(0,1)
    )


def generate_layout(window_shape: tuple[int, int], image_shape: tuple[int, int], margin_frac: float = 0.05, slider_frac: float = 0.1):
    # image_shape[0] is the number of rows in the np.ndarray
    # here we use it as the pixel dimensions of the image, so we need to swap
    image_shape = (image_shape[1], image_shape[0])

    margin = np.floor(margin_frac * np.array(window_shape))

    slider_width = window_shape[0] - 2*margin[0]
    slider_height = int(slider_frac * window_shape[1])
    slider_rect = pygame.rect.Rect(margin[0], window_shape[1] - margin[1] - slider_height, slider_width, slider_height)

    bbox_width = (window_shape[0] - 3*margin[0]) / 2
    bbox_height = window_shape[1] - 3*margin[1] - slider_height

    # rettangolo inscritto in un altro rettangolo
    bbox_aspect_ratio = bbox_height / bbox_width
    image_aspect_ratio = image_shape[1] / image_shape[0]

    bbox_hor_offset = margin[0]
    bbox_ver_offset = margin[1]


    if bbox_aspect_ratio < image_aspect_ratio:
        # l'altezza della immagine è il fattore limitante (a parità di lunghezza l'immagine è più larga della bbox)
        new_width = bbox_height / image_aspect_ratio

        bbox_hor_offset = margin[0] + (bbox_width - new_width)/2
        bbox_ver_offset = margin[1]
        bbox_width = new_width
    else:
        # la larghezza della immagine è il fattore limitante
        new_height = bbox_width * image_aspect_ratio

        bbox_hor_offset = margin[0]
        bbox_ver_offset = margin[1] + (bbox_height - new_height)/2
        bbox_height = new_height

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
    args = common.parse_args(version='pygame')

    filename = 'resources/cameraman.jpg' if args.image is None else args.image
    name, matrix = common.load_image_from_filename(filename, precision=args.precision)

    U, Sigma, Vh, explained_variance = common.compute_svd_quantities(matrix)

    k = 3
    max_singular_values = min(args.max_singular_values, Sigma.size)

    print('[INFO]: converting image to pygame Surface')
    original_image_texture = make_grayscale_surface(matrix)

    compute_compressed_matrix = lambda k: np.clip(common.truncate_to_k_singular_values(U, Sigma, Vh, k), 0, 255)

    min_k = 1
    max_k = max_singular_values
    compressed_image = compute_compressed_matrix(k)
    compressed_image_texture = make_grayscale_surface(compressed_image)

    # ------------------------ interactive section -----------------------------
    window_size = (600, 600)

    pygame.init()
    screen = pygame.display.set_mode(window_size, pygame.DOUBLEBUF | pygame.RESIZABLE)
    clock  = pygame.time.Clock()

    running = True
    state = k
    mouse_state = 'up'
    percent = (state - min_k) / (max_k - min_k)

    while running:
        clicked = False

        window_size = screen.get_size()
        slider_rect, left_bbox_rect, right_bbox_rect = generate_layout(window_size, matrix.shape)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_state == 'up':
                    clicked = True

                mouse_state = 'down'

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_state = 'up'

        mouse_pos = pygame.mouse.get_pos()

        if clicked:
            if slider_rect.collidepoint(mouse_pos):
                percent = (mouse_pos[0] - slider_rect.x) / slider_rect.w
                new_state = min_k + int(percent * (max_k - min_k))

                if new_state != state:
                    state = new_state
                    compressed_image = compute_compressed_matrix(state)
                    compressed_image_texture = make_grayscale_surface(compressed_image)

        scaled_image_texture = pygame.transform.smoothscale(original_image_texture, (left_bbox_rect.w, left_bbox_rect.h))
        scaled_compressed_image_texture = pygame.transform.smoothscale(compressed_image_texture, (right_bbox_rect.w, right_bbox_rect.h))

        screen.fill((255, 255, 255))
        screen.blit(scaled_image_texture, (left_bbox_rect.x, left_bbox_rect.y))
        screen.blit(scaled_compressed_image_texture, (right_bbox_rect.x, right_bbox_rect.y))

        pygame.draw.rect(screen, color=(0,100,100), rect=slider_rect)
        pygame.draw.rect(screen, color=(0,200,200), rect=pygame.rect.Rect(slider_rect.x, slider_rect.y, percent*slider_rect.w, slider_rect.h))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
