import sys
import numpy as np

import common
import PyQt5
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from vispy import scene
from vispy.app import use_app
from vispy.scene import STTransform


# adapted from 'https://vispy.org/gallery/scene/realtime_data/ex01_embedded_vispy.html'
class Controls(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout()

        self.slider_label = QtWidgets.QLabel(f'Singular values ( 1)')
        layout.addWidget(self.slider_label)

        self.slider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(30)
        self.slider.setSingleStep(1)

        layout.addWidget(self.slider)
        layout.addStretch(1)

        self.slider.valueChanged.connect(self.update_label)
        self.setLayout(layout)

    def update_label(self):
        value = self.slider.value()
        self.slider_label.setText(f'Singular values ({value:2})')


class CanvasWrapper:
    def __init__(self):
        args = common.parse_args(version='matplotlib')
        filename = 'resources/cameraman.jpg' if args.image is None else args.image
        name, matrix = common.load_image_from_filename(filename, precision=args.precision)
        U, Sigma, Vh, explained_variance = common.compute_svd_quantities(matrix)

        canvas = scene.SceneCanvas()

        vb1 = scene.widgets.ViewBox(parent=canvas.scene)
        vb2 = scene.widgets.ViewBox(parent=canvas.scene)
        vb3 = scene.widgets.ViewBox(parent=canvas.scene)
        vb = (vb1, vb2, vb3)

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

        # save only the relevant aspects
        self.args = args
        self.canvas = canvas
        self.compressed_image = compressed_image

        self.U = U
        self.Sigma = Sigma
        self.Vh = Vh

    def set_compressed_image(self, k: int):
        compressed_image = common.truncate_to_k_singular_values(
            self.U, self.Sigma, self.Vh, k
        )

        self.compressed_image.set_data(compressed_image)
        self.canvas.update()


class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout()

        self._controls = Controls()
        main_layout.addWidget(self._controls)
        self._canvas_wrapper = CanvasWrapper()
        main_layout.addWidget(self._canvas_wrapper.canvas.native)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self._connect_controls()

    def _connect_controls(self):
        self._controls.slider.valueChanged.connect(self._canvas_wrapper.set_compressed_image)


if __name__ == '__main__':
    app = use_app("pyqt5")
    app.create()

    win = MyMainWindow()
    win.show()
    app.run()
