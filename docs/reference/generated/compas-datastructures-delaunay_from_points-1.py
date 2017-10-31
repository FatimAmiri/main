from compas.geometry import pointcloud_xy
from compas.datastructures import Mesh
from compas.datastructures import delaunay_from_points

from compas.visualization import MeshPlotter

points   = pointcloud_xy(10, (0, 10))
delaunay = delaunay_from_points(Mesh, points)

plotter = MeshPlotter(delaunay)

plotter.draw_vertices(radius=0.1)
plotter.draw_faces()

plotter.show()