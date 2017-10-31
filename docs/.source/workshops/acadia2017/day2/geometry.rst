.. _acadia2017_day2_geometry:

********************************************************************************
Geometry
********************************************************************************

Introduction
======================================

The *compas* framework contains an extensive set of python geometry functions 
and algorithms without any external dependencies. Code using the geometry 
package can run in any Python or IronPython environment. Hence, any algorithm
or program using the geometry package can easily be integrated in different
applications (e.g.: Rhino, Blender, Maya, ...)

The full geometry reference can be found here:

* :mod:`compas.geometry`

.. note::

    Besides many basic geometry functions such as:

    * :mod:`compas.geometry.add_vectors`
    * :mod:`compas.geometry.subtract_vectors`
    * :mod:`compas.geometry.intersection_line_plane`
    * :mod:`compas.geometry.closest_point_on_polyline`
    * :mod:`compas.geometry.is_point_in_triangle`
    * ...

    The geometry package also includes geometry 
    algorithms such as:

    * :mod:`compas.geometry.planarize_faces`
    * :mod:`compas.geometry.smooth_centroid`
    * :mod:`compas.geometry.smooth_area`
    * :mod:`compas.geometry.discrete_coons_patch`
    * ...   


Object-Oriented Interface vs Functions
--------------------------------------

The geometry package features an object-oriented interface:

.. code-block:: python

    from __future__ import print_function

    from compas.geometry import Vector

    u = Vector(1.0, 0.0, 0.0)
    v = Vector(0.0, 1.0, 0.0)

    r = u + v

    print(r)
    print(r.length)


The same vector calculations can be computed using functions and 
lists (or tuples) as vectors:

.. code-block:: python

    from __future__ import print_function

    from compas.geometry import add_vectors
    from compas.geometry import length_vector

    u = (1.0, 0.0, 0.0)
    v = (0.0, 1.0, 0.0)

    r = add_vectors(u, v)

    print(r)
    print(length_vector(r))


Compute and Visualize a 3D Spiraling Polyline  
---------------------------------------------

The following example script uses basic vector methods to compute a spiraling polyline
based on stepwise rotation and scaling.  

.. figure:: /_images/flatter_spiral.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Spiral created by stepwise rotation and scaling

.. seealso::

    * :meth:`compas.geometry.add_vectors`
    * :meth:`compas.geometry.scale_vector`
    * :func:`compas.geometry.subtract_vectors`
    * :func:`compas.geometry.rotate_points`


.. note::

    The following examples are made to be visualised in Rhino. Please check if you 
    have the right IronPython version installed.

    Open the script editor in Rhino (Command: _EditPythonScript) and run:

     .. code-block:: python

        import sys
        print(sys.version_info)

    Make sure to have version 2.7.5 installed!

.. code-block:: python

    import math

    import rhinoscriptsyntax as rs

    from compas.geometry import add_vectors
    from compas.geometry import scale_vector
    from compas.geometry import subtract_vectors
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


Raytracing Inside a Box  
-----------------------

The following example script uses basic geometry functions to compute the reflection
path inside a box based on a given starting ray.  

.. figure:: /_images/ball.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Reflection path inside of a box

.. seealso::

    * :meth:`compas.geometry.reflect_line_triangle`
    * :meth:`compas.geometry.distance_point_point`
    * :meth:`compas.geometry.subtract_vectors`
    * :meth:`compas.geometry.add_vectors`
    * :meth:`compas.geometry.scale_vector`
    * :meth:`compas.geometry.normalize_vector`


Rhino file for this example:

* :download:`reflect.3dm </../../examples/workshops/acadia2017/reflect.3dm>`

.. code-block:: python

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


Add this script to the previous example to animate a ball bouncing of the walls
of the given box.

.. code-block:: python

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


**Exercise**: Allow the player to target a defined corner and stop the ball if
it is close to that corner. 

Hint code snippet:

.. code-block:: python

    # use
    # from compas.geometry import distance_point_point
     
    # ... 
    # visualizing ball
    pt_id = rs.AddTextDot("8", pt)

    # do something here
    # ------------------


Creating Geometric Algorithms for Architectural Applications
============================================================

Plugging together geometry functions in combinations with datastructures allow to 
develope tools for architectural design and optimization.


Simple Translational Surfaces for Gridshelss
--------------------------------------------

.. figure:: /_images/sbp.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Cabot Circus Bristol and Deutsches Historisches Museum (Photo: SBP)

Using translational surfaces for the design of gridshells allows to explore freeform
spaces that can be built from planar (glass) panels. Jörg Schlaich together with Hans 
Schober published several geometric design methods for various gridshells built in the 
last decades.

.. figure:: /_images/planar_sweeps.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Various translation surfaces


Rhino file for the following examples:

* :download:`trans_srf.3dm </../../examples/workshops/acadia2017/trans_srf.3dm>`

Sweep Translation Surface
^^^^^^^^^^^^^^^^^^^^^^^^^

The following example shows the generation of a simple tanslation surface based on a
given profile and rail curve. 


.. figure:: /_images/sweep.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Sweep translation surface

.. seealso::

    * :func:`compas.geometry.translate_points`


.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import subtract_vectors
    from compas.geometry import centroid_points
    from compas.geometry import translate_points

    # Get inputs
    crv_p = rs.GetObject("Select profile", 4)
    crv_r = rs.GetObject("Select rail",4)

    div_p = 20
    div_r = 40

    # divide profile and rail curve
    pts_p = rs.DivideCurve(crv_p, div_p)
    pts_r = rs.DivideCurve(crv_r, div_r)


    # ------------------------------
    # compas geometry function

    # reference point for profile curve
    pt_ref = centroid_points([pts_p[0], pts_p[-1]])

    # create profiles along the rail curve
    pts_sets = []
    for i in range(div_r + 1):
        vec_1 = subtract_vectors(pts_r[i], pt_ref)
        points = translate_points(pts_p, vec_1)
        pts_sets.append(points)

    # create polyline point sets for each face
    polys = []
    for i in xrange(len(pts_sets)-1):
        for j in xrange(len(pts_sets[i])-1):
            p1 = pts_sets[i][j] 
            p2 = pts_sets[i + 1][j] 
            p3 = pts_sets[i + 1][j + 1] 
            p4 = pts_sets[i][j + 1]
            polys.append([p1, p2, p3, p4, p1])

    # compas geometry function
    # ------------------------------

    # draw gridshell in Rhino
    rs.EnableRedraw(False)
    for poly in polys:
        rs.AddPolyline(poly)
    rs.EnableRedraw(True)


Aligned Translation Surface
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example shows the generation of a tanslation surface with profile
curves aligned with the rail curve.


.. figure:: /_images/project_plane.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Aligned translation surface


.. seealso::

    * :func:`compas.geometry.project_points_plane`


.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import subtract_vectors
    from compas.geometry import project_points_plane

    # Get inputs
    crv_p = rs.GetObject("Select profile", 4)
    crv_a = rs.GetObject("Select rail 1",4)

    div_p = 20
    div_r = 40

    # divide profile and rail curve
    pts_p = rs.DivideCurve(crv_p, div_p)
    pts_a = rs.DivideCurve(crv_a, div_r)


    # ------------------------------
    # compas geometry function

    # create planes along the rail curve
    planes = []
    for i in range(div_r):
        vec = subtract_vectors(pts_a[i + 1], pts_a[i])
        planes.append([pts_a[i], vec])

    # subsequentely project profile curve to all planes
    pts_uv = []
    pts = pts_p
    for i in range(div_r - 1):
        pts = project_points_plane(pts, planes[i])
        pts_uv.append(pts)

    # create polyline point sets for each face
    polys = []
    for u in xrange(len(pts_uv)-1):
        for v in xrange(len(pts_uv[u])-1):
            p1 = pts_uv[u][v] 
            p2 = pts_uv[u + 1][v] 
            p3 = pts_uv[u + 1][v + 1] 
            p4 = pts_uv[u][v + 1]
            polys.append([p1, p2, p3, p4, p1])

    # compas geometry function
    # ------------------------------

    # draw gridshell in Rhino
    rs.EnableRedraw(False)
    for poly in polys:
        rs.AddPolyline(poly)
    rs.EnableRedraw(True)


**Exercise**: Create a mesh object from the extruded geometry. Generate fins
(rs.AddSrfPt()) normal to the mesh along the edges. Use a (u, v) tuples as vertex keys.

Hint code snippet:

.. code-block:: python

    # use:
    from compas.datastructures import Mesh
    from compas_rhino import mesh_draw_faces
    trans_mesh = Mesh()

    # add vertices to mesh object
    for u in xrange(len(pts_uv)):
        for v in xrange(len(pts_uv[u])):
            x, y, z = pts_uv[u][v]
            
            # do something here:
            # trans_mesh.add_vertex(...)

    # add faces to mesh object
    for u in xrange(len(pts_uv)-1):
        for v in xrange(len(pts_uv[u])-1):
            
            # do something here
            # trans_mesh.add_face(...)

    mesh_draw_faces(trans_mesh)

    for u, v in trans_mesh.edges():
        # do something here


.. seealso::

    * :func:`compas_rhino.mesh_draw_faces`
    * :func:`compas.geometry.add_vectors`
    * :func:`compas.geometry.scale_vector`
    * :class:`compas.datastructures.Mesh`
    * mesh.vertex_normal()
    * mesh.vertex_coordinates()

Solution:

* :download:`trans_fins.py </../../examples/workshops/acadia2017/trans_fins.py>`


Conical Translation Surface
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following figure shows the generation of a tanslation surface with two profile
curves. The method geneartes planes along the two rail curves and subsequentely uses
intersections with conical extrusions to guarantee the planarity of resulting mesh.

.. figure:: /_images/conical_srf.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Translation surface with conical sections

The steps of the algorithm are:

* Divide profile curve
* Divide rail curves
* Create planes aligned to both rail curves
* Compute focus point based on a pair of tangents to the two rails
* Create cone between projected profile curve and focus point
* Intersect cone with next section plane
* repeat the last three points


.. seealso::

    * :func:`compas.geometry.add_vectors`
    * :func:`compas.geometry.centroid_points`
    * :func:`compas.geometry.intersection_line_plane`
    * :func:`compas.geometry.intersection_line_line`


.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import subtract_vectors
    from compas.geometry import add_vectors
    from compas.geometry import centroid_points
    from compas.geometry import intersection_line_plane
    from compas.geometry import intersection_line_line
    from compas.geometry import normalize_vector
        
    # Get inputs
    crv_p = rs.GetObject("Select profile", 4)
    crv_a = rs.GetObject("Select rail 1",4)
    crv_b = rs.GetObject("Select rail 2",4)

    div_p = 20
    div_r = 40

    # divide profile and rail curves
    pts_p = rs.DivideCurve(crv_p, div_p)
    pts_a = rs.DivideCurve(crv_a, div_r)
    pts_b = rs.DivideCurve(crv_b, div_r)

    # ------------------------------
    # compas geometry function

    # create planes along the rail curve
    planes = []
    for i in range(div_r):
        pt_mid = centroid_points([pts_a[i], pts_b[i]])
        vec_a = subtract_vectors(pts_a[i + 1], pts_a[i])
        vec_b = subtract_vectors(pts_b[i + 1], pts_b[i])
        vec_a = normalize_vector(vec_a)
        vec_b = normalize_vector(vec_b)
        vec = add_vectors(vec_a, vec_b)
        planes.append([pt_mid, vec])

    # create profiles
    pts_uv = []
    pts = pts_p
    for i in range(div_r - 1):
        ray_a = [pts_a[i], pts_a[i + 1]]
        ray_b = [pts_b[i], pts_b[i + 1]]
        pts_x = intersection_line_line(ray_a, ray_b)
        if None in pts_x:
            print("parallel!")
        pt_cent = centroid_points(pts_x)
        # computes intersection between a plane and all lines
        # from the profile curve points to the intersection point
        pts = [intersection_line_plane([pt, pt_cent], planes[i + 1]) for pt in pts]
        
        pts_uv.append(pts)

    # create polyline point sets for each face
    polys = []
    for u in xrange(len(pts_uv)-1):
        for v in xrange(len(pts_uv[u])-1):
            p1 = pts_uv[u][v] 
            p2 = pts_uv[u + 1][v] 
            p3 = pts_uv[u + 1][v + 1] 
            p4 = pts_uv[u][v + 1]
            polys.append([p1, p2, p3, p4, p1])

    # compas geometry function
    # ------------------------------

    # draw gridshell in Rhino
    rs.EnableRedraw(False)
    for poly in polys:
        rs.AddPolyline(poly)
    rs.EnableRedraw(True)


Grasshopper definition:

* :download:`trans_srf.gh </../../examples/workshops/acadia2017/trans_srf.gh>`

.. note::

    You need the GhPython for Grasshopper to run trans_srf.gh.
    * http://www.food4rhino.com/app/ghpython



Using Geometric Algorithms and Optimization Techniques
======================================================


Coons Patches
-------------

Create a 3D coons patch.

.. figure:: /_images/coons.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Gridshells from Coons meshes 

.. seealso::

    * :func:`compas.geometry.discrete_coons_patch`

    * https://en.wikipedia.org/wiki/Coons_patch


Rhino file for the following examples:

* :download:`coons.3dm </../../examples/workshops/acadia2017/coons.3dm>`


.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import add_vectors
    from compas.geometry import scale_vector

    from compas.datastructures.mesh import Mesh
    from compas.geometry import discrete_coons_patch

    from compas_rhino import mesh_draw_faces


    # Select objects in Rhino
    crv_ab = rs.GetObject("Select ab",4)
    crv_bc = rs.GetObject("Select bc",4)
    crv_dc = rs.GetObject("Select cd",4)
    crv_ad = rs.GetObject("Select ad",4)

    # Define devisions
    div_a = 15
    div_b = 15

    # height of fons
    height = 0.3

    # divide boundary curves of coons patch
    ab = rs.DivideCurve(crv_ab, div_a)
    bc = rs.DivideCurve(crv_bc, div_b)
    dc = rs.DivideCurve(crv_dc, div_a)
    ad = rs.DivideCurve(crv_ad, div_b)

    # compute coons patch
    vertices, faces = discrete_coons_patch(ab, bc, dc, ad)
    coons = Mesh.from_vertices_and_faces(vertices, faces)

    # draw coons patch
    mesh_draw_faces(coons, join_faces=True)



Torsion-free Elements for Coons Patch Gridshells
------------------------------------------------

Create a 3D coons patch with close-to planar fins.

.. seealso::

    * :func:`compas.geometry.planarize_faces`
    * :func:`compas.geometry.flatness`
    * :func:`compas.utilities.i_to_rgb`


.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import add_vectors
    from compas.geometry import scale_vector

    from compas.datastructures.mesh import Mesh
    from compas.geometry import discrete_coons_patch

    from compas_rhino import mesh_draw_faces

    from compas.geometry import planarize_faces
    from compas.geometry import flatness
    from compas.utilities import i_to_rgb

    def draw_fins(vertices, faces):
        # don't refresh viewport
        rs.EnableRedraw(False)
        # compute level of flatness
        flat_vals = flatness(vertices, faces, maxdev=0.02)
        srfs = []
        for i, face in enumerate(faces):
            # vertex coordinates for face
            pts = [vertices[key] for key in face]
            # create Rhino surface
            srfs.append(rs.AddSrfPt(pts))
            # color surface based on flatness
            rgb = i_to_rgb(flat_vals[i])
            rs.ObjectColor(srfs[-1], rgb)
        rs.AddObjectsToGroup(srfs, rs.AddGroup())
        # refresh viewport
        rs.EnableRedraw(True)
        return srfs

    # Select objects in Rhino
    crv_ab = rs.GetObject("Select ab",4)
    crv_bc = rs.GetObject("Select bc",4)
    crv_dc = rs.GetObject("Select cd",4)
    crv_ad = rs.GetObject("Select ad",4)

    # Define devisions
    div_a = 15
    div_b = 15

    # height of fons
    height = 0.3

    # divide boundary curves of coons patch
    ab = rs.DivideCurve(crv_ab, div_a)
    bc = rs.DivideCurve(crv_bc, div_b)
    dc = rs.DivideCurve(crv_dc, div_a)
    ad = rs.DivideCurve(crv_ad, div_b)

    # compute coons patch
    vertices, faces = discrete_coons_patch(ab, bc, dc, ad)
    coons = Mesh.from_vertices_and_faces(vertices, faces)

    # draw coons patch
    mesh_draw_faces(coons, join_faces=True)

    # build index-key and key-index maps
    index_key = {i : key for i, key in enumerate(coons.vertices())}
    key_index = {key : i for i, key in enumerate(coons.vertices())}

    # convert vertices dictionary to vertices list
    vertices_list = [coons.vertex_coordinates(key) for key in coons.vertices()]
    # number of vertices of coons mesh
    n = coons.number_of_vertices()

    # compute offset vertices
    for i in range(len(vertices)):
        normal = scale_vector(coons.vertex_normal(index_key[i]), height)
        vertices_list.append(add_vectors(vertices_list[i], normal))

    # convert faces with vertex keys to vertex indices
    faces_list = []
    for u, v in coons.edges():
        faces_list.append([key_index[u], key_index[v], key_index[v] + n, key_index[u] + n])

    # visualize fins
    draw_fins(vertices_list, faces_list)
        
    # define callback
    def callback(k, callback_args=None):
        rs.Prompt('Iteration: {0} '.format(k))

    # planarize fins
    planarize_faces(vertices_list, faces_list, kmax=200, callback=callback)

    # visualize planarized fins
    draw_fins(vertices_list, faces_list)


**Exercise**: Fix the lower vertices of the fins during the planarization optimization. Relate the 
height of the fins to the z-values of the vertices. The largest fins should be at the supports.  




Volumetric Network Structures with Subdivision Meshes
-----------------------------------------------------

The following code computes a solidified smooth mesh from a spatial network of lines.
The shown method yields similar results as the exoskeleton plugin for Grasshopper
to create meshes for 3D printing.

.. figure:: /_images/node.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Smooth volumetric mesh from lines

The steps of the algorithm are:

* Align quad frames for each adjacent edge per node
* One quad frame close to the node, the other one at the midpoint of the edge
* Compute convex hull with the verticies of the inner frames
* Add rectangular pipe between convex hull and midpoints for each edge
* Create a joined mesh and subdivides using Catmull-Clark subdivision

.. seealso::

    * :func:`compas.geometry.orient_points`
    * :func:`compas.geometry.convex_hull`
    * :func:`compas.datastructures.mesh_subdivide_catmullclark`
    
.. seealso::

    * https://en.wikipedia.org/wiki/Convex_hull
    * https://en.wikipedia.org/wiki/Catmull-Clark_subdivision_surface


Rhino file for the following examples:

* :download:`tree.3dm </../../examples/workshops/acadia2017/tree.3dm>`


.. code-block:: python

    import math

    from compas.geometry import convex_hull
    from compas.geometry import orient_points

    from compas.geometry import subtract_vectors
    from compas.geometry import normalize_vector
    from compas.geometry import add_vectors
    from compas.geometry import scale_vector

    from compas.datastructures.mesh import Mesh
    from compas.datastructures.mesh import mesh_subdivide_catmullclark

    from compas.datastructures.network import Network

    from compas_rhino import mesh_draw_faces

    import rhinoscriptsyntax as rs


    def generate_section(radius, target_plane, flag):
        num_p = 4  # discretization of the circle
        theta = 2 * math.pi / num_p  # angle step size
        # create cross section points around the origin
        points = [(radius * math.cos(theta * i), radius * math.sin(theta * i), 0.) for i in range(num_p)]
        # align cross section points with the edge
        if flag < 0:
            target_plane[1] = scale_vector(target_plane[1],-1)
            points.reverse()
        return orient_points(points, target_plane=target_plane)


    def generate_node(network, key, radius, fac):
        # initialize mesh object
        mesh = Mesh()
        mesh.attributes['name'] = 'mesh' + str(key)
        # coordinates of the node
        pt_cent = network.vertex_coordinates(key)
        # u's and v's of all connected edges
        edges = network.vertex_connected_edges(key)

        # loop over all edges
        section_keys = []
        for u, v in edges:
            # create edge vector 
            # check if edges point towards or away from the node
            if u == key:
                vec_nbr = subtract_vectors(network.vertex_coordinates(v), network.vertex_coordinates(u))
                flag = -1
            else:
                flag = 1
                vec_nbr = subtract_vectors(network.vertex_coordinates(u), network.vertex_coordinates(v))
                
            # create point to locate the inner section
            pt_1 = add_vectors(pt_cent, scale_vector(vec_nbr, fac))
            # create point to locate the outer section
            pt_2 = add_vectors(pt_cent, scale_vector(vec_nbr, 0.5))
            # create inner cross section points
            points = generate_section(radius, [pt_1, normalize_vector(vec_nbr)],flag)
            
            inner_keys = [mesh.add_vertex(x=x, y=y, z=z) for x, y, z in points]
            # create outer cross section points
            points = generate_section(radius, [pt_2, normalize_vector(vec_nbr)],flag)
            outer_keys = [mesh.add_vertex(x=x, y=y, z=z) for x, y, z in points]
            
            # create faces between inner and outer cross section
            for i in range(len(inner_keys)):
                face = [inner_keys[i - 1], inner_keys[i], outer_keys[i], outer_keys[i - 1]]
                mesh.add_face(face)

            section_keys.append(inner_keys)

        # vertices coordinates of all inner cross sections
        section_keys_all = [item for sublist in section_keys for item in sublist]
        points = [mesh.vertex_coordinates(key) for key in section_keys_all]
        # key index list for mapping
        key_index = [key for i, key in enumerate(section_keys_all)]
        # compute convex hull for all inner cross section points
        faces_index = convex_hull(points)
        # add convex hull faces to the mesh
        for face_index in faces_index:
            face = [key_index[i] for i in face_index]
            add_face = True
            for section_key in section_keys:
                # don't add faces for the cross section caps
                if len(set(face) & set(section_key)) == 3:
                    add_face = False
                    break
            #add face to mesh
            if add_face:
                mesh.add_face(face)

        return mesh


    # This code computes a solidified smooth mesh from a spatial network of lines.
    # The shown method yields similar results as the exoskeleton plugin for Grasshopper 
    # to create meshes for 3D pinting.

    # select a network of lines
    objs = rs.GetObjects("lines", 4)

    radius = 0.3    # global radius for pipes
    fac = 0.15     # global scale for smooth corners (<0.5)
    sub_level = 2   # steps of subdivisions (<3 gets very slow quickly)

    # create network from lines in Rhino
    lines = [(rs.CurveStartPoint(obj), rs.CurveEndPoint(obj)) for obj in objs]
    network = Network.from_lines(lines)

    for key in network.vertices():
        # skip if node is not connected to any neighbour (leaf)
        if network.is_vertex_leaf(key):
            continue
        # generate mesh per node
        mesh = generate_node(network, key, radius, fac)
        # subdivide mesh
        mesh = mesh_subdivide_catmullclark(mesh, sub_level)
        # draw mesh
        mesh_draw_faces(mesh, redraw=False, join_faces=True)



.. figure:: /_images/tree.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Volumetric tree structure


The shown tree structure can be structurally improved by finding a more 
"balanced" network geometry. A spatial smoothing can help to improve the
given configuration.


.. seealso::

    * :class:`compas.datastructures.Network`
    * :func:`compas.geometry.network_smooth_centroid`
    * :func:`compas_rhino.network_draw_edges`


.. code-block:: python

    from compas.geometry import network_smooth_centroid

    from compas.datastructures.network import Network
    from compas_rhino import network_draw_edges

    import rhinoscriptsyntax as rs
        
        
    # select a network of lines
    objs = rs.GetObjects("lines", 4)

    # create network from lines in Rhino
    lines = [(rs.CurveStartPoint(obj), rs.CurveEndPoint(obj)) for obj in objs]
    network = Network.from_lines(lines)

    # create list of keys for fixed vertices
    fixed = [key for key in network.vertices() if network.vertex_degree(key) == 1]

    # smooth network
    network_smooth_centroid(network, fixed=fixed, kmax=100, damping=0.1, callback=None, callback_args=None)

    # draw relaxed network
    network_draw_edges(network)


A callback function can be used to show the iterations:

.. code-block:: python

    from compas.geometry import network_smooth_centroid

    from compas.datastructures.network import Network
    from compas_rhino import network_draw_edges

    import rhinoscriptsyntax as rs

    # callback function get called in every interation step
    def callback(network, k, args):
        # unpack arguments
        step = args[0]
        # print iterations and draw network
        if k % step == 0:
            rs.Prompt("Iteration: {0}".format(k))
            network_draw_edges(network)
        

    # select a network of lines
    objs = rs.GetObjects("lines", 4)

    # create network from lines in Rhino
    lines = [(rs.CurveStartPoint(obj), rs.CurveEndPoint(obj)) for obj in objs]
    network = Network.from_lines(lines)

    # create list of keys for fixed vertices
    fixed = [key for key in network.vertices() if network.vertex_degree(key) == 1]

    # define callback variables
    step = 1

    # set callback arguments
    callback_args = [step]

    # smooth network
    network_smooth_centroid(network, fixed=fixed, kmax=100, damping=0.1, callback=callback, callback_args=callback_args)

    # draw relaxed network
    network_draw_edges(network)


**Exercise**: Let the network vertex with y = 0.0 freely slide on the y-z-plane during the smoothing.

Hint code snippet:

.. code-block:: python

    # get vertex key for a vertex on the x-z-plane
    for key in network.vertices():
        # do something here
            
    # remove x-z-plane vertex key from fixed
    # do something here


    # in the callback function :
    # ...
    if k % step == 0:
        rs.Prompt("Iteration: {0}".format(k))
        network_draw_edges(network)
    
    # constrain y-coordinate to 0.0 for vertex with specific key
    # do something here


.. seealso::

    * :func:`compas_rhino.mesh_draw_faces`
    * :func:`compas.geometry.add_vectors`
    * :func:`compas.geometry.scale_vector`
    * :class:`compas.datastructures.Mesh`
    * mesh.vertex_normal()
    * mesh.vertex_coordinates()

Solution:

* :download:`tree_02.py </../../examples/workshops/acadia2017/tree_02.py>`


**Exercise**: Let the network vertex with y = 0.0 slide on the y-z-plane during the smoothing.
Additionally, the vertex must stay within a user-defined distance in respect to its original location.


.. seealso::

    * :func:`compas.geometry.add_vectors`
    * :func:`compas.geometry.scale_vector`
    * :func:`compas.geometry.subtract_vectors`
    * :func:`compas.geometry.length_vector`
    * :func:`compas.geometry.normalize_vector`
    * :func:`compas.geometry.distance_point_point`

Solution:

* :download:`tree_03.py </../../examples/workshops/acadia2017/tree_03.py>`



Tessellation of a freeform barrel vault
---------------------------------------

wip...



Generate uv staggered pattern:

.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas_rhino import uv_points_from_surface

    srf = rs.GetObject("Select Surface",8)

    u_div = 30
    v_div = 30

    #create initial mesh
    pts_uv = uv_points_from_surface(srf,u_div,v_div)

    for u in xrange(u_div - 1):
        rs.AddPolyline(pts_uv[u])
        for v in xrange(0, v_div - 1, 2):
            if u % 2:
                rs.AddLine(pts_uv[u][v],pts_uv[u + 1][v])
            else:
                rs.AddLine(pts_uv[u][v + 1],pts_uv[u + 1][v + 1])
