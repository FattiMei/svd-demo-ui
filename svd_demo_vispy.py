import sys
import numpy as np
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from vispy import scene
from vispy.app import use_app
from vispy.scene import STTransform

import common


# adapted from 'https://vispy.org/gallery/scene/realtime_data/ex01_embedded_vispy.html'
class Controls(QtWidgets.QWidget):
    def __init__(self, initial_value: int, max_singular_values: int, callback_on_slider_change, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout()

        self.slider_label = QtWidgets.QLabel()
        layout.addWidget(self.slider_label)

        self.slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(max_singular_values)
        self.slider.setSingleStep(1)

        layout.addWidget(self.slider)
        layout.addStretch(1)

        self.slider.valueChanged.connect(self.update_label)
        self.slider.valueChanged.connect(callback_on_slider_change)
        self.slider.setValue(initial_value)
        self.setLayout(layout)

    def update_label(self):
        value = self.slider.value()
        self.slider_label.setText(f'Singular values ({value:2})')


# this class should implement only the rendering logic
class CanvasWrapper:
    def __init__(self, matrix: np.ndarray, explained_variance: np.ndarray):
        canvas = scene.SceneCanvas()
        grid = canvas.central_widget.add_grid()

        vb1 = grid.add_view(0, 0, bgcolor='#c0c0c0')
        vb2 = grid.add_view(0, 1, bgcolor='#c0c0c0')
        vb3 = grid.add_view(0, 2, bgcolor='#c0c0c0')
        vb = (vb1, vb2, vb3)

        # panzoom cameras for every viewbox
        for box in vb:
            box.camera = 'panzoom'
            box.camera.aspect = 1.0

        original_image = scene.visuals.Image(matrix, parent=vb1.scene, cmap='gray')
        original_image.transform = STTransform(translate=(0, 0, 0.5))
        vb1.camera.flip = (0,1,0)
        vb1.camera.set_range()

        compressed_image = scene.visuals.Image(np.zeros_like(matrix), parent=vb2.scene, cmap='gray')
        compressed_image.transform = STTransform(translate=(0, 0, 0.5))
        vb2.camera.flip = (0,1,0)
        vb2.camera.set_range()

        # the original implementation wasn't plotting properly due to the first range being too large
        # is this a bug? Needs a simple replica
        #
        #   pos = np.stack((np.arange(explained_variance.size), explained_variance)).T
        #
        pos = np.stack((np.linspace(0,1,num=explained_variance.size), explained_variance)).T
        variance_line = scene.visuals.Line(pos, parent=vb3.scene, color='blue')
        vb3.camera.set_range(
            y=(0,1)
        )

        # save only the relevant aspects
        self.canvas = canvas
        self.compressed_image = compressed_image
        self.variance_line = variance_line

    def set_compressed_image(self, new_image: np.ndarray):
        self.compressed_image.set_data(new_image)
        self.canvas.update()


# this class should encapsulate the domain logic
class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        args = common.parse_args(version='vispy')
        filename = 'resources/cameraman.jpg' if args.image is None else args.image
        name, matrix = common.load_image_from_filename(filename, precision=args.precision)
        self.U, self.Sigma, self.Vh, explained_variance = common.compute_svd_quantities(matrix)
        
        k = 3
        max_singular_values = min(args.max_singular_values, self.Sigma.size)

        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()

        self._canvas_wrapper = CanvasWrapper(matrix, explained_variance)
        self._controls = Controls(initial_value=3, max_singular_values=max_singular_values, callback_on_slider_change=self.recompute_compressed_image)

        main_layout.addWidget(self._controls)
        main_layout.addWidget(self._canvas_wrapper.canvas.native)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # there is a level on indirection:
    #   at this level we know the svd decomposition and we know how to produce compressed images
    #   at the canvas level we know how to diplay them
    def recompute_compressed_image(self, k: int):
        self._canvas_wrapper.set_compressed_image(
            common.truncate_to_k_singular_values(self.U, self.Sigma, self.Vh, k)
        )


if __name__ == '__main__':
    app = use_app("pyqt5")
    app.create()

    win = MyMainWindow()
    win.show()
    app.run()
