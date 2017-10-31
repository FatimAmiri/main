.. _acadia2017_day2_geometry:

********************************************************************************
Geometry
********************************************************************************
<<<<<<< HEAD

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
======================================

The geometry package features an object-oriented interface:

.. plot::
    :include-source:

    from compas.geometry import Vector

    u = Vector(1.0, 0.0, 0.0)
    v = Vector(0.0, 1.0, 0.0)

    r = u + v

    print(r)
    print(r.length)


The same vector calculations can be computed using functions and 
lists (or tuples) as vectors:

.. plot::
    :include-source:

    from compas.geometry import add_vectors
    from compas.geometry import length_vector

    u = (1.0, 0.0, 0.0)
    v = (0.0, 1.0, 0.0)

    r = add_vectors(u, v)

    print(r)
    print(length_vector(r))


Adding Multiple Vectors 
-----------------------

Create a set of 10.000 random vectors with the origin (1. ,2. ,3.) and compute their
resultant. Compare the preformance of an object-based and function-based method.  

.. seealso::

    * :meth:`compas.geometry.Vector.from_start_end`
    * :meth:`compas.geometry.Vector.from_start_end`

    * :func:`compas.geometry.vector_from_points`
    * :func:`compas.geometry.add_vectors`
    * :func:`compas.geometry.sum_vectors`


Solution:

.. plot::
    :include-source:


    from random import random as rnd
    import time

    from compas.geometry import Vector

    from compas.geometry import add_vectors
    from compas.geometry import sum_vectors
    from compas.geometry import vector_from_points


    # create random points
    points = [(rnd(), rnd(), rnd()) for _ in range(10000)]
    # define origin
    origin = [1., 2., 3.]


    # Object-based method
    vecs = [Vector.from_start_end(origin, pt) for pt in points]
    res = Vector(0., 0., 0.)
    for v in vecs:
        res += v
    print('{0} computed with object-based method'.format(res))


    # Function-based method A
    vecs = [vector_from_points(origin, pt) for pt in points]
    res = [0., 0., 0.]
    for v in vecs:
        res = add_vectors(res, v)
    print('{0} computed with function-based method A'.format(res))


    # Function-based method B
    vecs = [vector_from_points(origin, pt) for pt in points]
    res = sum_vectors(vecs)
    print('{0} computed with function-based method B'.format(res))



Creating Geometric Algorithms from Simple Functions
===================================================

Introduction text... Algorithms can ....


Simple Translational Surfaces for Gridshelss
--------------------------------------------

Using translational surfaces for the design of gridshells allows to explore freeform
spaces that can be built from planar (glass) panels. Jörg Schlaich together with Hans 
Schober developed several geometric design methods for various gridshells built in the 
last decades.

.. figure:: /_images/sbp.jpg
    :figclass: figure
    :class: figure-img img-fluid

    Cabot Circus Bristol and Deutsches Historisches Museum (Photo: SBP)


.. note::

    The following examples are made to be visualised in Rhino. Please check if you 
    have the right IronPython version installed.

    Open the script editor in Rhino (Command: _EditPythonScript) and run:

     .. code-block:: python

        import sys
        print(sys.version_info)

    Make sure to have version 2.7.5 installed!


The following example shows the generation of a simple tanslation surface based on a
given profile and rail curve. 

.. note::

    The following examples are based on the 3dm file:

    * :download:`trans_srf.3dm </../../examples/trans_srf.3dm>`


.. figure:: /_images/trans_srf_01.jpg
    :figclass: figure
    :class: figure-img img-fluid

    See 3dm file for details 


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



The following example shows the generation of a tanslation surface with profile
curves aligned with the rail curve.

.. figure:: /_images/trans_srf_03.jpg
    :figclass: figure
    :class: figure-img img-fluid

    See 3dm file for details 

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

Exercise: 
---------

The following figure shows the generation of a tanslation surface with two profile
curves. The method geneartes planes along the two rail curves and subsequentely uses
intersections with conical extrusions to guarantee the planarity of resulting mesh.

.. figure:: /_images/trans_srf_04.jpg
    :figclass: figure
    :class: figure-img img-fluid

    See 3dm file for details 

The steps of the algorithm are:

* blabla bl lal lsldd bllbblb
  blblblbl bldlbl
  (:func:`compas.geometry.add_vectors`)
* ...

.. note::

    The following examples is also available for Grasshopper:

    * :download:`trans_srf.3dm </../../examples/trans_srf.gh>`


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




Torsion-free Elements for Gridshells
====================================

- Create a 3D coons patch.


.. code-block:: python

    import rhinoscriptsyntax as rs

    from compas.geometry import add_vectors

    from compas.datastructures.mesh import Mesh
    from compas_rhino.helpers.artists.meshartist import MeshArtist
    from compas.geometry.algorithms.interpolation import discrete_coons_patch
    from compas.datastructures import mesh_cull_duplicate_vertices



    crv_ab = rs.GetObject("Select ab",4)
    crv_bc = rs.GetObject("Select bc",4)
    crv_dc = rs.GetObject("Select cd",4)
    crv_ad = rs.GetObject("Select ad",4)

    div_a = 15
    div_b = 15

    ab, bc, dc, ad = None, None, None, None

    if crv_ab: ab = rs.DivideCurve(crv_ab, div_a)
    if crv_bc: bc = rs.DivideCurve(crv_bc, div_b)
    if crv_dc: dc = rs.DivideCurve(crv_dc, div_a)
    if crv_ad: ad = rs.DivideCurve(crv_ad, div_b)

    vertices, face_vertices = discrete_coons_patch(ab, bc, dc, ad)
    coon = Mesh.from_vertices_and_faces(vertices, face_vertices)

    artist = MeshArtist(coon, layer='MeshArtist')
    artist.draw_edges()
    artist.draw_vertices()
    artist.draw_faces()
    #artist.redraw(1.0)


    for u, v in coon.edges():
        pt_u = coon.vertex_coordinates(u)
        pt_v = coon.vertex_coordinates(v)
        vec_u = coon.vertex_normal(u)
        vec_v = coon.vertex_normal(v)
        pt_uu = add_vectors(pt_u, vec_u)
        pt_vv = add_vectors(pt_v, vec_v)
        rs.AddPolyline([pt_u,pt_v,pt_vv,pt_uu,pt_u])




- make a mesh.
- populate fins

- planarize fins
- constrain fins to a specific height



Smoothen on surface
===================






Tessellation of a freeform barrel vault
=======================================

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





subdivision stuff
=================


subdivision stuff
=================



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
=======
>>>>>>> d1144cc015660b52049211e6e09dc011cbebf3a6
