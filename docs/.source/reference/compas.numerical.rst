.. _compas.numerical:

********************************************************************************
numerical
********************************************************************************

.. module:: compas.numerical

.. note::

    The array and matrix-based implementations of the numerical package are built around NumPy and SciPy.

    * NumPy: http://www.numpy.org/
    * SciPy: https://www.scipy.org/


Algorithms
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    dr
    dr_numpy
    drx_numpy
    fd_numpy
    pca_numpy


Solvers
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    descent
    devo_numpy
    ga
    moga


Functions
=========

**linalg**

.. autosummary::
    :toctree: generated/
    :nosignatures:

    nullspace
    rank
    dof
    pivots
    nonpivots
    rref
    rref_sympy
    rref_matlab
    chofactor
    lufactorized
    uvw_lengths
    normrow
    normalizerow
    rot90
    solve_with_known
    spsolve_with_known


**matrices**

.. autosummary::
    :toctree: generated/
    :nosignatures:

    adjacency_matrix
    degree_matrix
    connectivity_matrix
    laplacian_matrix
    face_matrix
    mass_matrix
    equilibrium_matrix
    network_adjacency_matrix
    network_degree_matrix
    network_connectivity_matrix
    network_laplacian_matrix
    mesh_adjacency_matrix
    mesh_degree_matrix
    mesh_face_matrix
    mesh_connectivity_matrix
    mesh_laplacian_matrix
    trimesh_cotangent_laplacian_matrix


**operators**

.. autosummary::
    :toctree: generated/
    :nosignatures:

    grad


Utilities
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    float_formatter
    set_array_print_precision
    unset_array_print_precision


