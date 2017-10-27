import compas
from compas.datastructures import Mesh
from compas.visualization import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices()
plotter.draw_faces()
plotter.draw_edges()

plotter.draw_vertices(
    text='key',
    facecolor=(0.9, 0.9, 0.9),
)
plotter.draw_faces(
    text='key',
    facecolor=(0.7, 0.7, 0.7),
)
plotter.draw_edges(
    text='key'
)

plotter.show()