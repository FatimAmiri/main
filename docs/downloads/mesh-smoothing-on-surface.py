"""Smooth a mesh on a NURBS surface.

- make a mesh datastructure form a given Rhino mesh
- define a target surface
- smooth the mesh
- use a callback to pull the mesh back onto the surface at every iteration
- visualize the process with a conduit

"""

from __future__ import print_function

from compas.datastructures import Mesh
from compas.geometry import smooth_area

import compas_rhino

from compas_rhino.conduits import LinesConduit
from compas_rhino.geometry import RhinoSurface


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# make a mesh datastructure from a Rhino mesh object
# and select a target surface

guid = compas_rhino.select_mesh()
mesh = compas_rhino.mesh_from_guid(Mesh, guid)

guid = compas_rhino.select_surface()
surf = RhinoSurface(guid)


# extract the input for the smoothing algorithm from the mesh
# and identify the boundary as fixed

vertices  = {key: mesh.vertex_coordinates(key) for key in mesh.vertices()}
faces     = {key: mesh.face_vertices(key) for key in mesh.faces()}
adjacency = {key: mesh.vertex_faces(key) for key in mesh.vertices()}
fixed     = set(mesh.vertices_on_boundary())


# make a conduit for visualization
# and a callback for updating the conduit
# and for pulling the free vertices back to the surface
# at every iteration

edges = list(mesh.edges())
lines = [[vertices[u], vertices[v]] for u, v in edges]

conduit = LinesConduit(lines, refreshrate=5)

def callback(vertices, k, args):
    for key in set(vertices) - fixed:
            x, y, z = surf.closest_point(vertices[key])
            vertices[key][0] = x
            vertices[key][1] = y
            vertices[key][2] = z

    conduit.lines = [[vertices[u], vertices[v]] for u, v in edges]
    conduit.redraw(k)


# with the conduit enabled
# run the smoothing algorithm
# update the mesh when smoothing is done
# and draw the result

with conduit.enabled():
    smooth_area(
        vertices,
        faces,
        adjacency,
        fixed=fixed,
        kmax=100,
        callback=callback)

for key, attr in mesh.vertices(True):
    attr['x'] = vertices[key][0]
    attr['y'] = vertices[key][1]
    attr['z'] = vertices[key][2]

compas_rhino.mesh_draw(mesh)
