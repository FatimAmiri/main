
.. _compas.topology:

********************************************************************************
topology
********************************************************************************

.. currentmodule:: compas.topology


combinatorial
-------------

.. autosummary::
    :toctree: generated/

    vertex_coloring

orientation
-----------

.. autosummary::
    :toctree: generated/

    mesh_flip_cycles
    mesh_unify_cycles

planarity
---------

.. autosummary::
    :toctree: generated/

    'network_is_crossed',
    'network_count_crossings',
    'network_find_crossings',
    'network_is_xy',
    'network_is_planar',
    'network_is_planar_embedding',
    'network_embed_in_plane',


subdivision
-----------

.. autosummary::
    :toctree: generated/

    mesh_subdivide
    mesh_subdivide_tri
    mesh_subdivide_catmullclark
    mesh_subdivide_doosabin

traversal
---------

.. autosummary::
    :toctree: generated/

    dfs_ordering
    dfs_paths
    bfs_ordering
    bfs_traverse
    bfs_paths
    shortest_path
    dijkstra_distances
    dijkstra_path

triangulation
-------------

.. autosummary::
    :toctree: generated/

    delaunay_from_points
    voronoi_from_delaunay
    mesh_quads_to_triangles
    trimesh_remesh


