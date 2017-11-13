from numpy import random

import matplotlib.pyplot as plt

from compas.geometry import rotation_matrix
from compas.geometry import transform_numpy

from compas.plotters import Axes3D
from compas.plotters import Cloud3D
from compas.plotters import Bounds
from compas.plotters import create_axes_3d

from compas.numerical import pca_numpy

data = random.rand(300, 3)
data[:, 0] *= 10.0
data[:, 1] *= 1.0
data[:, 2] *= 4.0

a = 3.14159 * 30.0 / 180
Ry = rotation_matrix(a, [0, 1.0, 0.0], rtype='array')

a = -3.14159 * 45.0 / 180
Rz = rotation_matrix(a, [0, 0, 1.0], rtype='array')

R = Rz.dot(Ry)

data = transform_numpy(data, R)

average, vectors, values = pca_numpy(data)

axes = create_axes_3d()

Bounds(data).plot(axes)
Cloud3D(data).plot(axes)
Axes3D(average, vectors).plot(axes)

plt.show()