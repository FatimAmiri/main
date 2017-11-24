import compas

from compas.datastructures import Mesh
from compas.plotters import MeshPlotter

from compas.geometry import centroid_points

mesh = Mesh.from_obj(compas.get_data('faces.obj'))

for fkey in list(mesh.faces()):
    vertices = mesh.face_vertices(fkey)
    mesh.split_face(fkey, vertices[0], vertices[2])

mesh.swap_edge_tri(14, 16)
mesh.swap_edge_tri(31, 22)

mesh.collapse_edge_tri(30, 17)
mesh.collapse_edge_tri(30, 31)
mesh.collapse_edge_tri(30, 22)

points = mesh.get_vertices_attributes('xyz', keys=mesh.vertex_neighbours(30))
x, y, z = centroid_points(points)
attr = {'x': x, 'y': y, 'z': z}

mesh.set_vertex_attributes(30, attr)

plotter = MeshPlotter(mesh)

plotter.draw_vertices(text={key: key for key in mesh.vertices()}, radius=0.2)
plotter.draw_faces(text={fkey: fkey for fkey in mesh.faces()})

plotter.show()