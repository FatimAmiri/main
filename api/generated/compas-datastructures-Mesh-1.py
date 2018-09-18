import compas
from compas.datastructures import Mesh

mesh = Mesh.from_obj(compas.get('faces.obj'))

mesh.plot(
    vertextext={key: key for key in network.vertices()},
    vertexcolor={key: '#ff0000' for key in mesh.vertices_where({'vertex_degree': 2})}
    vertexsize=0.2
)