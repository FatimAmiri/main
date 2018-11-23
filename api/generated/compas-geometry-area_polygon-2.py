from compas.plotters import Plotter

plotter = Plotters()

polygon = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.5, 0.0, 0.0],
    [0.0, 1.0, 0.0]
]

area_polygon(polygon)

# 0.5

plotter.draw_polygons([{'points': polygon}])
plotter.show()