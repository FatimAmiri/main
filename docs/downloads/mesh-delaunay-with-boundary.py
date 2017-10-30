"""Delaunay triangulation with boundary"""

from compas.datastructures import Mesh

import compas_rhino


__author__    = ['Tom Van Mele', 'Matthias Rippmann']
__copyright__ = 'Copyright 2017, BRG - ETH Zurich',
__license__   = 'MIT'
__email__     = 'van.mele@arch.ethz.ch'


# select the points
# select the boundary
# select the hole(s)

guids = compas_rhino.select_points("Select points.")
points = compas_rhino.get_point_coordinates(guids)

guid = compas_rhino.select_polyline("Select boundary.")
boundary = compas_rhino.get_polyline_coordinates(guid)

guids = compas_rhino.select_polylines("Select holes.")
holes = [compas_rhino.get_polyline_coordinates(guid) for guid in guids]


# make a delaunay triangulation
# within the boundary
# and around the holes

mesh = Mesh.from_points(points, boundary=boundary, holes=holes)


# draw the result

compas_rhino.mesh_draw(mesh)
