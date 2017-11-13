import compas
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter
from compas.topology import depth_first_tree
from compas.utilities import pairwise

mesh = Mesh.from_obj(compas.get('faces.obj'))

edges = list(mesh.edges())

root = mesh.get_any_vertex()

ordering, predecessors, paths = depth_first_tree(mesh.adjacency, root)

edgecolor = {}
edgewidth = {}

for u, v in pairwise(paths[0]):
    if not mesh.has_edge(u, v):
        u, v = v, u
    edgecolor[(u, v)] = '#ff0000'
    edgewidth[(u, v)] = 3.0

for path in paths[1:]:
    parent = predecessors[path[0]]
    for u, v in pairwise([parent] + path):
        if not mesh.has_edge(u, v):
            u, v = v, u
        edgecolor[(u, v)] = '#00ff00'
        edgewidth[(u, v)] = 3.0

plotter = MeshPlotter(mesh, figsize=(10, 7))

plotter.draw_vertices(text='key', facecolor={root: '#ff0000'}, radius=0.2)
plotter.draw_edges(color=edgecolor, width=edgewidth)

plotter.show()