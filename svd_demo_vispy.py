import sys
import numpy as np

import common
from vispy import app, scene
from vispy.scene import STTransform


# `%gui qt` in an interactive console


if __name__ == '__main__':
    args = common.parse_args(version='matplotlib')

    filename = 'resources/cameraman.jpg' if args.image is None else args.image
    name, matrix = common.load_image_from_filename(filename, precision=args.precision)

    U, Sigma, Vh, explained_variance = common.compute_svd_quantities(matrix)

    canvas = scene.SceneCanvas(keys='interactive', show=True)
    canvas.size = 800, 600
    canvas.show()

    vb1 = scene.widgets.ViewBox(parent=canvas.scene)
    vb2 = scene.widgets.ViewBox(parent=canvas.scene)
    vb3 = scene.widgets.ViewBox(parent=canvas.scene)
    vb = (vb1, vb2, vb3)

    # add grid as central widget, add viewboxes into grid
    grid = canvas.central_widget.add_grid()
    grid.padding = 0
    grid.add_widget(vb1, 0, 0)
    grid.add_widget(vb2, 0, 1)
    grid.add_widget(vb3, 0, 2)

    # panzoom cameras for every viewbox
    for box in vb:
        box.camera = 'panzoom'
        box.camera.aspect = 1.0

    original_image = scene.visuals.Image(matrix, parent=vb1.scene, cmap='gray')
    original_image.transform = STTransform(translate=(0, 0, 0.5))
    vb1.camera.flip = (0,1,0)
    vb1.camera.set_range()

    compressed_image = scene.visuals.Image(matrix, parent=vb2.scene, cmap='gray')
    compressed_image.transform = STTransform(translate=(0, 0, 0.5))
    vb2.camera.flip = (0,1,0)
    vb2.camera.set_range()

    pos = np.stack((np.arange(explained_variance.size), explained_variance)).T
    variance_line = scene.visuals.LinePlot(pos, parent=vb3.scene)
    vb3.camera.set_range()

    app.run()
