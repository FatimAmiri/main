.. _tutorial_interop:

********************************************************************************
Using C/C++ code
********************************************************************************

Summary
=======

In this tutorial we will write a smoothing function in C++ and make it available
directly in Python. We will also use a callback to live visualise the iterations
of the algorithm and to dynamically change the boundary conditions. An
implementation of the code in this tutorial is available in the geometry package:

* :func:`compas.geometry.smooth_centroid_cpp`


Requirements
============

* a C++ compiler (for example g++, which is part of the GNU compiler collection)

Setup
=====

For this tutorial, we will use the following files and folders::

    + smoothing_cpp
        + src
            - main.cpp
        - smoothing.so
        - smoothing.py


The smoothing function
======================

First, the C++ code. The smoothing function will implement a simple barycentric
smoothing algorithm, in which at every iteration, each vertex is moved to the
barycentre of its neighbours.

By the way, I have no real experience in writing C++ code, so i am sure that this
can be done a lot more elegantly and efficiently.
I would be happy to hear about any and all suggestions (vanmelet@ethz.ch).

.. code-block:: cpp

    #include <vector>

    using namespace std;

    extern "C"
    {
        typedef void callback(int k);

        void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback func);
    }

    void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback func) 
    {
        int k;
        int i;
        int j, n;
        double cx, cy, cz;

        vector< vector<double> > xyz(v, vector<double>(3, 0.0));

        for (k = 0; k < kmax; k++) {

            // make a copy of the current vertex positions

            for (i = 0; i < v; i++) {
                xyz[i][0] = vertices[i][0];
                xyz[i][1] = vertices[i][1];
                xyz[i][2] = vertices[i][2];
            }

            // move each vertex to the barycentre of its neighbours

            for (i = 0; i < v; i++) {

                // skip the vertex if it is fixed
    
                if (fixed[i]) {
                    continue;
                }

                cx = 0.0;
                cy = 0.0;
                cz = 0.0;

                for (j = 0; j < nbrs[i]; j++) {
                    n = neighbours[i][j];

                    cx += xyz[n][0];
                    cy += xyz[n][1];
                    cz += xyz[n][2];
                }

                vertices[i][0] = cx / nbrs[i];
                vertices[i][1] = cy / nbrs[i];
                vertices[i][2] = cz / nbrs[i];
            }

            // call the callback

            func(k);
        }
    }


The ``ctypes`` wrapper
======================

Looking a the signature of the C++ function, the code is expecting the following
input arguments:

1. ``int v``
2. ``int *nbrs``
3. ``int *fixed``
4. ``double **vertices``
5. ``int **neighbours``
6. ``int kmax``
7. ``callback func``

Or, in other words:

1. the number of vertices, as an integer
2. the number of neighbours per vertex, as a an array of integers
3. a mask identifying the fixed vertices, as an array of integers (0/1)
4. the vertex coordinates, as a two-dimensional array of doubles
5. the vertex neighbours, as a two-dimensional array of integers
6. the maximum number of iterations, as an integer
7. the callback function, as a function of type callback

Note that the sizes of the arrays are unknown at compile time, since they depend
on the number of vertices in the system. Therefore they are passed as pointers.
My understanding of this is based on whatever google spat out and a few SO posts...

* https://stackoverflow.com/questions/8767166/passing-a-2d-array-to-a-c-function
* https://stackoverflow.com/questions/8767166/passing-a-2d-array-to-a-c-function/17569578#17569578
* http://www.cplusplus.com/doc/tutorial/arrays/

We want to be able to call the function from Python, which essentially boils down
to something like this:

.. code-block:: python

    import ctypes
    import compas
    from compas.datastructures import Mesh
    from compas.plotters import MeshPlotter

    # get the C++ smoothing library

    smoothing = ctypes.cdll.LoadLibrary('smoothing.so')

    # make a mesh

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    # extract the required data for smoothing

    vertices   = mesh.get_vertices_attributes('xyz')
    adjacency  = [mesh.vertex_neighbours(key) for key in mesh.vertices()]
    fixed      = [int(mesh.vertex_degree(key) == 2) for key in mesh.vertices()]
    v          = len(vertices)
    nbrs       = [len(adjacency[i]) for i in range(v)]
    neighbours = [adjacency[i] + [0] * (10 - nbrs[i]) for i in range(v)]

    # ==============================================================================
    # convert the python data to C-compatible types
    # ==============================================================================

    # ...

    # ==============================================================================

    # make a plotter for visualisation

    plotter = MeshPlotter(mesh, figsize=(10, 7))

    # plot the original line geometry as a reference

    lines = []
    for u, v in mesh.edges():
        lines.append({
            'start': mesh.vertex_coordinates(u, 'xy'),
            'end'  : mesh.vertex_coordinates(v, 'xy'),
            'color': '#cccccc',
            'width': 0.5
        })

    plotter.draw_lines(lines)

    # plot the starting point

    plotter.draw_vertices()
    plotter.draw_edges()

    plotter.update(pause=0.5)

    # ==============================================================================
    # define the callback function
    # ==============================================================================

    def callback(k):
        print(k)

        # update the plot
        # and change the boundary conditions

        # ...

    # ==============================================================================

    # ==============================================================================
    # set the C-type of each of the arguments
    # ==============================================================================

    # ...

    # ==============================================================================

    # ==============================================================================
    # run the smoothing function
    # ==============================================================================

    smoothing.smooth_centroid(...)    

    # ==============================================================================


Convert the Python data to C-compatible types
---------------------------------------------


