import compas

from compas.datastructures import Network
from compas.datastructures import network_smooth_centroid
from compas.plotters import NetworkPlotter

network = Network.from_obj(compas.get('grid_irregular.obj'))
fixed = [key for key in network.vertices() if network.vertex_degree(key) == 1]

network_smooth_centroid(network, fixed=fixed)

plotter = NetworkPlotter(network)

plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
plotter.draw_edges()

plotter.show()