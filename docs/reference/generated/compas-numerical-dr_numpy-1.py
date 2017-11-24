import compas
from compas.datastructures import Network
from compas.plotters import NetworkPlotter
from compas.numerical import dr_numpy

dva = {
    'is_fixed': False,
    'x': 0.0,
    'y': 0.0,
    'z': 0.0,
    'px': 0.0,
    'py': 0.0,
    'pz': 0.0,
    'rx': 0.0,
    'ry': 0.0,
    'rz': 0.0,
}

dea = {
    'qpre': 1.0,
    'fpre': 0.0,
    'lpre': 0.0,
    'linit': 0.0,
    'E': 0.0,
    'radius': 0.0,
}

network = Network.from_obj(compas.get('lines.obj'))
network.update_default_vertex_attributes(dva)
network.update_default_edge_attributes(dea)

for key, attr in network.vertices(True):
    attr['is_fixed'] = network.vertex_degree(key) == 1

for index, (u, v, attr) in enumerate(network.edges(True)):
    attr['qpre'] = index + 1

k_i = network.key_index()

vertices = network.get_vertices_attributes(('x', 'y', 'z'))
edges    = [(k_i[u], k_i[v]) for u, v in network.edges()]
fixed    = [k_i[key] for key in network.vertices_where({'is_fixed': True})]
loads    = network.get_vertices_attributes(('px', 'py', 'pz'))
qpre     = network.get_edges_attribute('qpre')
fpre     = network.get_edges_attribute('fpre')
lpre     = network.get_edges_attribute('lpre')
linit    = network.get_edges_attribute('linit')
E        = network.get_edges_attribute('E')
radius   = network.get_edges_attribute('radius')

lines = []
for u, v in network.edges():
    lines.append({
        'start': network.vertex_coordinates(u, 'xy'),
        'end'  : network.vertex_coordinates(v, 'xy'),
        'color': '#cccccc',
        'width': 1.0
    })

plotter = NetworkPlotter(network)
plotter.draw_lines(lines)

xyz, q, f, l, r = dr_numpy(vertices, edges, fixed, loads, qpre, fpre, lpre, linit, E, radius)

for key, attr in network.vertices(True):
    index = k_i[key]
    attr['x'] = xyz[index, 0]
    attr['y'] = xyz[index, 1]
    attr['z'] = xyz[index, 2]

plotter.draw_vertices(
    facecolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})})
plotter.draw_edges()
plotter.show()