from compas.geometry import reflect_line_triangle
from compas.geometry import distance_point_point
from compas.geometry import subtract_vectors
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import normalize_vector

import rhinoscriptsyntax as rs

# Select Objects
#-------------------------
tris_id = rs.GetObjects("Select Triangles", 4) # cage of triangles (check direction!)
line = rs.GetObject("Select Start Line", 4) # initial vector (direction and magnitude)

ab = list(rs.CurveStartPoint(line)), list(rs.CurveEndPoint(line))
velo = distance_point_point(ab[0], ab[1]) * 0.2

# triangles as list of points a, b, c
tris = []
for tri_id in tris_id:
    tris.append(rs.PolylineVertices(tri_id)[:-1])

# ray starting at ab, bouncing back the walls of the cage for max_d times
max_d = 100
poly_pts = [ab[0]]
for i in range(max_d):
    for tri in tris:
        reflected_line = reflect_line_triangle(ab, tri)
        if reflected_line:
            ab = reflected_line
            poly_pts.append(ab[0])
            break

# trace complete reflection path
rs.AddPolyline(poly_pts)
rs.AddPoints(poly_pts)