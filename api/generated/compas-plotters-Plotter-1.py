import compas

from compas.datastructures import Mesh
from compas.plotters import Plotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = Plotter(figsize=(10, 7))

points = []
for key in mesh.vertices():
    points.append({
        'pos'      : mesh.vertex_coordinates(key),
        'radius'   : 0.1,
        'facecolor': '#ffffff'
    })

lines = []
for u, v in mesh.edges():
    lines.append({
        'start': mesh.vertex_coordinates(u),
        'end'  : mesh.vertex_coordinates(v),
        'width': 1.0
    })

plotter.draw_points(points)
plotter.draw_lines(lines)
plotter.show()