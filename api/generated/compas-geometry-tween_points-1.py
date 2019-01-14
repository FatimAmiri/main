from compas.geometry import tween_points
from compas.plotters import Plotter

points1 = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 0.0, 0.0], [3.0, 0.0, 0.0]]
points2 = [[0.0, 0.0, 0.0], [1.0, 3.0, 0.0], [2.0, 1.0, 0.0], [3.0, 0.0, 0.0]]

tweens = tween_points(points1, points2, 5)

polylines = [{'points': points1, 'width': 1.0}]

for points in tweens:
    polylines.append({'points': points, 'width': 0.5})

polylines.append({'points': points2, 'width': 1.0})

plotter = Plotter()
plotter.draw_polylines(polylines)
plotter.show()