import compas
from compas.datastructures import Network
from compas.plotters import NetworkPlotter
from compas.numerical import drx_numpy
from compas.utilities import i_to_rgb

from numpy import linspace

L0 = 1
L = 1.5
n = 40
EI = 0.2
pins = [0, 5, 20, n - 5]

# Network

vertices = [[i, i, 0] for i in list(linspace(0, L0, n))]
edges = [[i, i + 1] for i in range(n - 1)]

network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
network.update_default_vertex_attributes({'is_fixed': False, 'P': [1, -2, 0], 'EIx': EI, 'EIy': EI})
network.update_default_edge_attributes({'E': 50, 'A': 1, 'l0': L / n})
network.set_vertices_attributes(pins, {'B': [0, 0, 0], 'is_fixed': True})
network.beams = {'beam': {'nodes': list(range(n))}}

# Plotter

plotter = NetworkPlotter(network)

lines = []
for u, v in network.edges():
    lines.append({
        'start': network.vertex_coordinates(u, 'xy'),
        'end'  : network.vertex_coordinates(v, 'xy'),
        'color': '#cccccc',
        'width': 1.0})

plotter.draw_lines(lines)

# Solver

drx_numpy(network=network, tol=0.01, refresh=10, factor=30, update=True)

# Result

plotter.draw_vertices(radius=0.005, facecolor={key: '#ff0000' for key in pins})
plotter.draw_edges()

plotter.show()