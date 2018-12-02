from compas.datastructures import Mesh
from compas.topology import trimesh_subdivide_loop
from compas.plotters import MeshPlotter

points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 1.0, 0.0]]
faces = [[0, 1, 2]]
mesh = Mesh.from_vertices_and_faces(points, faces)

subd = trimesh_subdivide_loop(mesh, k=5)

plotter = MeshPlotter(subd)
plotter.draw_vertices(radius=0.002)
plotter.draw_faces()
plotter.show()