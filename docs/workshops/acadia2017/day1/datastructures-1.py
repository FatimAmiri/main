import compas
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter

mesh = Mesh.from_obj(compas.get('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.draw_vertices()
plotter.draw_faces()
plotter.draw_edges()

plotter.draw_vertices(
    text='key',
    radius=0.15
)
plotter.draw_faces(
    text='key',
)
plotter.draw_edges(
    text='key'
)

plotter.show()