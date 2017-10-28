"""Smooth a mesh.

"""

from compas.datastructures import Mesh
from compas.geometry import smooth_area

import compas_rhino


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# select a Rhino mesh
# and make it into a mesh datastructure

guid = compas_rhino.select_mesh()
mesh = compas_rhino.mesh_from_guid(Mesh, guid)


# extract the data needed by the smoothing algorithm
# identify the boundary as fixed

vertices  = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
faces     = {key: mesh.face_vertices(key) for key in mesh.faces()}
adjacency = {key: mesh.vertex_faces(key) for key in mesh.vertices()}
fixed     = mesh.vertices_on_boundary()


# run the smoothing algorithm
# update the mesh
# display the result in Rhino

smooth_area(vertices, faces, adjacency, fixed=fixed, kmax=100)

for key, attr in mesh.vertices(True):
    attr['x'] = vertices[key][0]
    attr['y'] = vertices[key][1]
    attr['z'] = vertices[key][2]

compas_rhino.mesh_draw(mesh)
