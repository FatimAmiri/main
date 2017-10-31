# segments of reflection path ab, bc, cd, ...
lines = [(poly_pts[i], poly_pts[i + 1]) for i in range(len(poly_pts) - 1)]

# list of descending velocities
fac = 0.97
velos = [velo]
while velos[-1] > 0.05:
    velos.append(velos[-1] * fac)

# animate bouncing ball
i = 0
scale = 0
for velo in velos:
    scale += velo
    a, b = lines[i]
    ab_len = distance_point_point(a, b)
    vec = subtract_vectors(b, a)
    if scale > ab_len:
        scale = scale - ab_len
        i += 1
        a, b = lines[i]
        vec = subtract_vectors(b, a)

    pt = add_vectors(a, scale_vector(normalize_vector(vec), scale))

    # visualizing ball
    pt_id = rs.AddTextDot("8", pt)
    rs.Sleep(50)
    rs.DeleteObject(pt_id)