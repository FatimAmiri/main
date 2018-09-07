import compas
from compas.datastructures import Network

network = Network.from_obj(compas.get('lines.obj'))

network.plot(
    vertextext={key: key for key in network.vertices()},
    vertexsize=0.2
)