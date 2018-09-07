# leaves as breakpoints

import compas
from compas.topology import FaceNetwork
from compas.topology import network_find_faces
from compas.plotters import FaceNetworkPlotter

network = FaceNetwork.from_obj(compas.get('grid_irregular.obj'))

network_find_faces(network, breakpoints=network.leaves())

plotter = FaceNetworkPlotter(network)

plotter.draw_vertices(
    radius=0.075,
    facecolor={key: '#cccccc' for key in network.leaves()}
)
plotter.draw_edges(
    color={(u, v): '#cccccc' for u, v in network.edges()}
)
plotter.draw_faces(
    facecolor={fkey: '#eeeeee' for fkey in network.faces()},
    text={fkey: fkey for fkey in network.faces()}
)

plotter.show()