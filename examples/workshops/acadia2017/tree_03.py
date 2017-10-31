from compas.geometry import subtract_vectors
from compas.geometry import normalize_vector
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector
from compas.geometry import network_smooth_centroid

from compas.datastructures.network import Network
from compas_rhino import network_draw_edges

import rhinoscriptsyntax as rs

# callback function get called in every interation step
def callback(network, k, args):
    # unpack arguments
    step, key_y, pt_base, dis_max = args
    
    # print iterations and draw network
    if k % step == 0:
        rs.Prompt("Iteration: {0}".format(k))
        network_draw_edges(network)
    
    # constrain y-coordinate to 0.0
    network.vertex[key_y]['y'] = 0.
    
    # constrain vertex movement in relation to pt_base
    pt = network.vertex_coordinates(key_y)
    vec = subtract_vectors(pt, pt_base)
    if length_vector(vec) > dis_max:
        vec = scale_vector(normalize_vector(vec),dis_max)
        x, y, z = add_vectors(pt_base, vec)
        network.vertex[key_y]['x'] = x
        network.vertex[key_y]['y'] = y 
        network.vertex[key_y]['z'] = z 
    

# select a network of lines
objs = rs.GetObjects("lines", 4)


# create network from lines in Rhino
lines = [(rs.CurveStartPoint(obj), rs.CurveEndPoint(obj)) for obj in objs]
network = Network.from_lines(lines)


# create list of keys for fixed vertices
fixed = [key for key in network.vertices() if network.vertex_degree(key) == 1]

# get vertex key for a vertex on the x-z-plane
for key in network.vertices():
    pts = network.vertex_coordinates(key)
    if -0.1 <= pts[1] <= 0.1:
        key_y = key
        break
        
# remove x-z-plane vertex key from fixed
fixed.remove(key_y)


# define callback variables
step = 1
pt_base = network.vertex_coordinates(key_y)
dis_max = 5.

# set callback arguments
callback_args = [step, key_y, pt_base, dis_max]

# smooth network
network_smooth_centroid(network, fixed=fixed, kmax=100, damping=0.1, callback=callback, callback_args=callback_args)

# draw relaxed network
network_draw_edges(network)
