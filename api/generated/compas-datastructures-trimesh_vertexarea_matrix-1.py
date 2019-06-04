import compas

from compas.datastructures import Mesh
from compas.datastructures import mesh_quads_to_triangles
from compas.datastructures import trimesh_vertexarea_matrix
from compas_plotters import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh_quads_to_triangles(mesh)
A = trimesh_vertexarea_matrix(mesh)
area = A.diagonal().tolist()

plotter = MeshPlotter(mesh, tight=True)

plotter.draw_vertices(
    text={key: "{:.1f}".format(area[i]) for i, key in enumerate(mesh.vertices())},
    radius=0.2
)
plotter.draw_edges()
plotter.draw_faces()
plotter.show()