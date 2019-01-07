import compas

from compas.topology import network_find_faces
from compas.datastructures import Network
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter

network = Network.from_obj(compas.get('lines.obj'))

mesh = Mesh()

for key, attr in network.vertices(True):
    mesh.add_vertex(key, x=attr['x'], y=attr['y'], z=attr['z'])

mesh.halfedge = network.halfedge

network_find_faces(mesh)

mesh.delete_face(0)

plotter = MeshPlotter(mesh)

plotter.draw_vertices()
plotter.draw_edges()
plotter.draw_faces()

plotter.show()