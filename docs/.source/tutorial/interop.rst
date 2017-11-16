.. _tutorial_interop:

********************************************************************************
Using C/C++ code
********************************************************************************

Requirements
============

* a c++ compiler (for example g++, which is part of the GNU compiler collection)


Setup
=====

For this tutorial, we will use the following files and folders::

    - smoothing_cpp
        - src
            * main.cpp
        * smoothing.so
        * smoothing.py


The smoothing function
======================

First, the C++ code. By the way, I have no experience in writing C++ code, so i am sure
that this can be done a lot better, and i would happy to hear about any and all
suggestions (vanmelet@ethz.ch).

.. code-block:: cpp

    // smoothing_cpp/src/main.cpp

    #include <vector>

    using namespace std;

    extern "C"
    {
        typedef void callback_smoothing(int k);

        void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback_smoothing func);
    }

    void smooth_centroid(int v, int *nbrs, int *fixed, double **vertices, int **neighbours, int kmax, callback_smoothing func) 
    {
        int k;
        int i;
        int j, n;
        double cx, cy, cz;
        double c;

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

                c = 0.0;

                for (j = 0; j < nbrs[i]; j++) {
                    n = neighbours[i][j];

                    cx += xyz[n][0];
                    cy += xyz[n][1];
                    cz += xyz[n][2];

                    c += 1.0;
                }

                vertices[i][0] = cx / c;
                vertices[i][1] = cy / c;
                vertices[i][2] = cz / c;
            }

            // call the callback

            func(k);
        }
    }


The ``ctypes`` wrapper
======================




