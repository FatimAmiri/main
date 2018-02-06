# WORK IN PROGRESS, CURRENTLY DOESNT WORK

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Network
from compas.numerical import algorithms
from compas.utilities import XFunc
from compas_rhino.helpers.artists.networkartist import NetworkArtist

import rhinoscriptsyntax as rs


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


# Make Network from lines

guids = rs.ObjectsByLayer('Default')
lines = [[rs.CurveStartPoint(guid), rs.CurveEndPoint(guid)] for guid in guids]
network = Network.from_lines(lines)
leaves = network.leaves()

# Assign attributes

m = network.number_of_edges()
network.add_vertex(key=(m + 1), x=0, y=-100)
network.update_default_edge_attributes({
    'w': m + 1,
    'E': 10.**7,
    'nu': 0.,
    'A': 1.,
    'Ix': 2.25 * 0.5**4,
    'Iy': 1. / 12,
    'Iz': 1. / 12,
})

bcs = {i: False for i in ['dofx', 'dofy', 'dofz', 'dofalpha', 'dofbeta', 'dofgamma']}

network.set_vertices_attributes(keys=[leaves[0], m + 1], attr_dict=bcs)
network.set_vertex_attribute(key=leaves[1], name='pz', value=600)

# Run XFunc

basedir = algorithms.__file__.split('__init__.py')[0]
xfunc = XFunc('dr6dof', basedir=basedir)
xfunc.funcname = 'dr_6dof.dr_6dof_numba'
X, x, x0 = xfunc(network=network, dt=1.0, xi=1., tol=0.001, steps=50, geomstiff=0)
print(x)

# Update Network

#k_i = network.key_index()
#for key in network.vertices():
#    i = k_i[key]
#    network.set_vertex_attributes(key, {'x': X[i][0], 'y': X[i][1], 'z': X[i][2]})

# Draw Network

artist = NetworkArtist(network=network, layer='Plot')
artist.clear_layer()
artist.draw_vertices()
artist.draw_vertexlabels()
artist.draw_edges()
