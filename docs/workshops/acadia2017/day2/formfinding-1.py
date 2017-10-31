import random

import compas
from compas.datastructures import Network
from compas.visualization import NetworkPlotter
from compas.geometry import network_relax
from compas.utilities import i_to_rgb

network = Network.from_obj(compas.get('lines.obj'))

dva = {
    'is_fixed': False,
    'px': 0.0,
    'py': 0.0,
    'pz': 0.0,
}
dea = {
    'q': 1.0,
    'f': 0.0,
    'l': 0.0
}

network.update_default_vertex_attributes(dva)
network.update_default_edge_attributes(dea)

for key, attr in network.vertices(True):
    attr['is_fixed'] = network.is_vertex_leaf(key)

for index, (u, v, attr) in enumerate(network.edges(True)):
    attr['q'] = 1.0 * random.randint(1, 7)

plotter = NetworkPlotter(network, figsize=(10, 7))

lines = []
for u, v in network.edges():
    lines.append({
        'start' : network.vertex_coordinates(u, 'xy'),
        'end'   : network.vertex_coordinates(v, 'xy'),
        'color' : '#cccccc',
        'width' : 0.5
    })

plotter.draw_lines(lines)

network_relax(network, kmax=50)

fmax = max(network.get_edges_attribute('f'))

plotter.draw_vertices(
    facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})}
)

plotter.draw_edges(
    color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in network.edges(True)},
    width={(u, v): 10 * attr['f'] / fmax for u, v, attr in network.edges(True)}
)

plotter.show()