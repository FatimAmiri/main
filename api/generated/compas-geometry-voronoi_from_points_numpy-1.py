from compas.datastructures import Mesh
from compas_plotters import MeshPlotter
from compas.geometry import closest_point_on_line_xy
from compas.geometry import voronoi_from_points_numpy

mesh = Mesh()

mesh.add_vertex(x=0, y=0)
mesh.add_vertex(x=1.5, y=0)
mesh.add_vertex(x=1, y=1)
mesh.add_vertex(x=0, y=2)

mesh.add_face([0, 1, 2, 3])

sites = mesh.vertices_attributes('xy')
voronoi = voronoi_from_points_numpy(sites)

points = []
for xy in voronoi.vertices:
    points.append({
        'pos'       : xy,
        'radius'    : 0.02,
        'facecolor' : '#ff0000',
        'edgecolor' : '#ffffff',
    })

lines = []
arrows = []
for (a, b), (c, d) in zip(voronoi.ridge_vertices, voronoi.ridge_points):
    if a > -1 and b > -1:
        lines.append({
            'start' : voronoi.vertices[a],
            'end'   : voronoi.vertices[b],
            'width' : 1.0,
            'color' : '#ff0000',
        })
    elif a == -1:
        sp = voronoi.vertices[b]
        ep = closest_point_on_line_xy(sp, (voronoi.points[c], voronoi.points[d]))
        arrows.append({
            'start' : sp,
            'end'   : ep,
            'width' : 1.0,
            'color' : '#00ff00',
            'arrow' : 'end'
        })
    else:
        sp = voronoi.vertices[a]
        ep = closest_point_on_line_xy(sp, (voronoi.points[c], voronoi.points[d]))
        arrows.append({
            'start' : sp,
            'end'   : ep,
            'width' : 1.0,
            'color' : '#00ff00',
            'arrow' : 'end'
        })

plotter = MeshPlotter(mesh)
plotter.draw_points(points)
plotter.draw_lines(lines)
plotter.draw_arrows(arrows)
plotter.draw_vertices(radius=0.02)
plotter.draw_faces()
plotter.show()