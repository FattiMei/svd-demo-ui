date: dom 2 mar 2025
tags: [[ui]], [[swe]]

My current interests are in the visualization of experiment results, plots and simulations with a real time interaction. Such computations are often parametric and it is desirable to see the effect those parameter have on the results.
## Previous attempts
* [svd compression](https://github.com/FattiMei/svd-demo-ui)
* [2d-lbm-opengl](https://github.com/FattiMei/2d-lbm-opengl)

## Conflicting requirements
The UI elements require an **high level graphics interface**:
* rectangles
* circles
* mouse and key events
but the implementation requires **low level API concepts**:
* vertexes and textures
* shaders (vertex, fragment, geometry, compute)
* GPU code

The interaction with the GPU is not "native" in the sense that a shader is not part of the programming language itself. This results in coupling problems and runtime errors.

## Proposed solutions
The top-down approach consists in using high level libraries and frameworks:
* [pygame](https://pygame.org)
* [SDL2](https://www.libsdl.org/)
* [raylib](https://raylib.com)
* [ImGUI](https://github.com/ocornut/imgui)
* ipywidgets

A good library paired with the flexibility of the python language, here are other python libraries more focused on scientific visualization:
* [vispy](https://vispy.org/gallery/scene/index.html)
* [pyqtgraph](https://pyqtgraph.readthedocs.io/en/latest/getting_started/plotting.html): `python -m pyqtgraph.examples`

### Making shaders part of the language
A *typed shader system* makes shaders available as native objects of the host language. This is similar to what `nvcc` has done to integrate CUDA kernels in C++ source files (a glorified preprocessor, if I may say so). Further context is [available here](https://chatgpt.com/share/67c4051b-1b18-800b-b499-d668b79d7856).

### Using the GPU for computing
Vispy makes use of OpenGL acceleration for plots. It's mission statement is to "harness(ing) The GPU For Fast, High Level Visualization". The real deal is whether or not the library is compatible with GPU computing in the sense that **can work with plot data already present in the GPU memory**. The problem arises from the interface between GPU memory objects (possibly owned by other third-party libraries) and rendering objects.

#### OpenGL - OpenGL interop
OpenGL data primitives are:
* vertex buffers
* textures
* *shader buffers* (only > 4.3)
and they are already native to the rendering process. However there are limitations in the memory access of the shaders that limit the range of application:
* **vertex shaders**: can only pass modified vertexes to the fragment shader or overwrite its vertexes with [`glTransformFeedbackVaryings`](https://www.khronos.org/opengl/wiki/Transform_Feedback). [Example of "quantum" particle simulation](file:///home/matteo/research)
* **fragment shaders**: can render on a texture
* **compute shaders**: can work with arbitrary data (they are the most powerful)

#### OpenCL/PyTorch/Jax - OpenGL interop
This is still a work in progress. One has to be critical about the role of GPU computation. Adopt this technique for the right reasons as we experimentally found that the bottleneck in visualization scripts is often `matplotlib`.
