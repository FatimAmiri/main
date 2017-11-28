.. _compas.topology:

********************************************************************************
topology
********************************************************************************

.. currentmodule:: compas.topology


combinatorial
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    vertex_coloring

orientation
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_flip_cycles
    mesh_unify_cycles

planarity
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    network_is_crossed
    network_count_crossings
    network_find_crossings
    network_is_xy
    network_is_planar
    network_is_planar_embedding
    network_embed_in_plane

subdivision
-----------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mesh_subdivide
    mesh_subdivide_tri
    mesh_subdivide_catmullclark
    mesh_subdivide_doosabin

traversal
---------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    depth_first_ordering
    depth_first_tree
    breadth_first_ordering
    breadth_first_traverse
    breadth_first_paths
    shortest_path
    dijkstra_distances
    dijkstra_path

triangulation
-------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    delaunay_from_points
    voronoi_from_delaunay
    mesh_quads_to_triangles
    trimesh_remesh


