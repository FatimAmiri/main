import math

import rhinoscriptsyntax as rs

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import scale_vector
from compas.geometry import rotate_points

# Select Rhino Object
obj = rs.GetObject("Select line", 4)

# create line list with start and end point coordinates
line = [rs.CurveStartPoint(obj), rs.CurveEndPoint(obj)]

rad = math.radians(10)
fac = 0.98

for i in range(400):
    # create and scale previous line vector
    vec = subtract_vectors(line[1], line[0])
    vec = scale_vector(vec, fac)
    # replace line with new scaled line
    line = [line[1], add_vectors(line[1], vec)]
    # rotate end point of line
    line = rotate_points(line, (0.,0.,1.), rad, line[0])
    # add line to Rhino
    rs.AddLine(line[0], line[1])