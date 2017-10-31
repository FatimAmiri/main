from compas.datastructures import Mesh
from compas.datastructures import trimesh_remesh
from compas.datastructures import delaunay_from_points
from compas.datastructures import voronoi_from_delaunay

from compas.geometry import pointcloud_xy

from compas.visualization import MeshPlotter

points   = pointcloud_xy(10, (0, 10))
delaunay = delaunay_from_points(Mesh, points)

trimesh_remesh(delaunay, 1.0, allow_boundary_split=True)

points   = [delaunay.vertex_coordinates(key) for key in delaunay.vertices()]
delaunay = delaunay_from_points(Mesh, points)
voronoi  = voronoi_from_delaunay(delaunay)

lines = []
for u, v in voronoi.edges():
    lines.append({
        'start': voronoi.vertex_coordinates(u, 'xy'),
        'end'  : voronoi.vertex_coordinates(v, 'xy'),
        'width': 1.0
    })

plotter = MeshPlotter(delaunay, figsize=(10, 6))

plotter.draw_lines(lines)

plotter.draw_vertices(
    radius=0.075,
    facecolor={key: '#0092d2' for key in delaunay.vertices() if key not in delaunay.vertices_on_boundary()})

plotter.draw_edges(color='#cccccc')

plotter.show()