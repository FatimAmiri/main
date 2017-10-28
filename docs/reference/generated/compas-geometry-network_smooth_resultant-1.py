import compas

from compas.datastructures import Network
from compas.visualization import NetworkPlotter
from compas.geometry import network_smooth_resultant

network = Network.from_obj(compas.get('grid_irregular.obj'))
fixed = [key for key in network.vertices() if network.vertex_degree(key) == 1]

lines = []
for u, v in network.edges():
    lines.append({
        'start' : network.vertex_coordinates(u, 'xy'),
        'end'   : network.vertex_coordinates(v, 'xy'),
        'color' : '#cccccc',
        'width' : 1.0
    })

network_smooth_resultant(network, fixed=fixed)

plotter = NetworkPlotter(network)

plotter.draw_lines(lines)

plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
plotter.draw_edges()

plotter.show()