# svd-demo-ui
Experiment at runtime image compression with the SVD algorithm


## Program description
The requested program takes as input an image, transforms it into a black and white image and then shows the following window
![plot](./screenshots/matplotlib.png)

where:
  * the left view is the original one
  * the center view is obtained from the [svd decomposition](https://en.wikipedia.org/wiki/Singular_value_decomposition) of the input, taking only the first $k$ singular values
  * the right view is the plot of explained variance as a function of $k$
  * the bottom view is the slider that controls how $k$ changes

If the user doesn't upload any image, a default one will be chosen.


## Rationale
> TL;DR Find a replacement of matplotlib for ugly but usable (=fast) interactive plots

I proposed this experiment to explore how we could interact with scientific plots and simulations. The scientific workflow benefits from interactivity for:
  * data exploration
  * building intuition
  * seeing in real time the effects of parameters for the target simulation

when searching for solutions to satisfy this requirement one must consider:
  * **quality of the plot**: as we are spoiled by `matplotlib` beautiful plots, competing solutions may have a more spartan outlook
  * **ease of use**: how easy is to assemble views and UI elements to match the user expectations
  * **low-noise rendering library**

the last point stresses the importance of making the simulation code the most relevant part of the program. The opposite of that is to bury the domain logic in deeply nested class hierarchies or in hundres of lines of UI spaghettic code. More details on searching a good UI solution [at my zettlekasten entry](./ui.md).


## Proposed solutions
Working with python, an high level language suitable for scientific computing, I propose three demos:
  * [`svd_demo_reference`](./svd_demo_reference) implements the specification with `matplotlib` and it's considered the gold standard for looks and usability
  * [`svd_demo_vispy`](./svd_demo_vispy) uses the promising [Vispy](https://vispy.org) library that uses OpenGL acceleration for plots and [PyGt5](https://pypi.org/project/PyQt5/) for UI elements
  * [`svd_demo_pygame`](./svd_demo_pygame) uses the [pygame](https://pygame.org) and implements a simple UI from scratch, without plotting capabilities for now

A minimal C program is also presented as an excuse to use [my smooth-gui library](https://github.com/FattiMei/smooth-gui). This should measure the overhead of the python applications.


## Screenshots
