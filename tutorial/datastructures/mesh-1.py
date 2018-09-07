import compas

from compas.datastructures import Mesh
from compas.plotters import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices(
    facecolor={key: '#ff0000' for key in mesh.vertices_on_boundary()},
    radius={key: 0.3 for key in mesh.vertices_on_boundary()},
    text={key: str(key) for key in mesh.vertices_on_boundary()}
)
plotter.draw_edges(
    color={key: '#00ff00' for key in mesh.edges_on_boundary()},
    width={key: 3 for key in mesh.edges_on_boundary()}
)
plotter.draw_faces(
    text={key: str(key) for key in mesh.faces_on_boundary()}
)

plotter.show()