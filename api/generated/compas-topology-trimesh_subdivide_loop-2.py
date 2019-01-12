from compas.datastructures import Mesh
from compas.topology import trimesh_subdivide_loop
from compas.topology import delaunay_from_points
from compas.geometry import pointcloud_xy
from compas.plotters import MeshPlotter

points = pointcloud_xy(10, (0, 100))
faces = delaunay_from_points(points)
mesh = Mesh.from_vertices_and_faces(points, faces)

subd = trimesh_subdivide_loop(mesh, k=3)

plotter = MeshPlotter(subd)
plotter.draw_vertices(radius=0.1)
plotter.draw_faces()
plotter.show()