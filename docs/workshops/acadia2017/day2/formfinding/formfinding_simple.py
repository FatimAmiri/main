""""""

import compas

from compas.datastructures import Mesh
from compas.visualization import MeshPlotter
from compas.numerical import fd
from compas.utilities import i_to_rgb


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


def main():
    """"""
    mesh = Mesh.from_obj(compas.get('faces.obj'))
    plotter = MeshPlotter(mesh)

    # plot original state

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end'  : mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 0.5 
        })

    plotter.draw_lines(lines)

    # preprocess

    k_i  = mesh.key_index()
    i_k  = mesh.index_key()
    uv_i = mesh.uv_index()
    i_uv = mesh.index_uv()

    xyz   = [mesh.vertex_coordinates(k) for k in mesh.vertices()]
    fixed = [k_i[k] for k in mesh.vertices() if mesh.vertex_degree(k) == 2]
    loads = [[0.0, 0.0, 0.0] for _ in range(mesh.number_of_vertices())]

    edges = [[k_i[u], k_i[v]] for u, v in mesh.edges()]
    q     = [1.0] * mesh.number_of_edges()
    
    # compute equilibrium

    xyz, q, f, l, r = fd(xyz, edges, fixed, q, loads, rtype='list')

    # update

    for key, attr in mesh.vertices(True):
        x, y, z = xyz[k_i[key]]
        attr['x'] = x
        attr['y'] = y
        attr['z'] = z

    # visualize

    fmax = max(f)

    plotter.draw_vertices(
        radius={key: 0.05 if k_i[key] not in fixed else 0.1 for key in mesh.vertices()},
        facecolor={i_k[i]: '#000000' for i in fixed}
    )

    plotter.draw_faces()

    plotter.draw_edges(
        text={uv: '{0:.1f}'.format(f[uv_i[uv]]) for uv in mesh.edges()},
        color={uv: i_to_rgb(f[uv_i[uv]] / fmax) for uv in mesh.edges()},
        width={uv: 10 * f[uv_i[uv]] / fmax for uv in mesh.edges()},
    )

    plotter.show()


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    
    main()
