.. _overview:

********************************************************************************
Overview
********************************************************************************

.. The main library of compas defines the core functionality of the framework
.. and provides packages for easy integration with CAD software.
.. The core package (:mod:`compas`) provides viewers and plotters such that it can
.. be used entirely standalone. The CAD intergation packages simplify working with
.. three-dimensional geometric data. They provide functionality for processing
.. geometric models, for visualizing and interacting with :mod:`compas` datastructures,
.. and for ...

The main library consists of a core package and several additional packages for
integration of the core into CAD software. The core package defines all *real*
functionality. The CAD packages simply provide a unified framework for processing,
visualising and interacting with datastructures and geometrical objects, and for
building user interfaces in different CAD software.


Core functionality
==================

.. naming conventions

To deal with the different academic backgrounds, programming skills, computational
experience, and best/accepted practices of its users and their respective fields,
**compas** is implemented primarily in Python and designed to be entirely independent
of the functionality of CAD software. As a result, it can be used on different
platforms and in combination with external software and libraries, and at the same
time take advantage of the various scientific and non-scientific libraries available
in the Python ecosystem itself. Furthermore, and perhaps more importantly, it ensures
that research based on **compas** is not tied to a specific CAD-based ecosystem.

Currently **compas** contains several sub-packages, which can be divided into four
sub-packages.

.. * :mod:`compas.com`: provides functionality for communicating with external software.
.. * :mod:`compas.datastructures`: defines a mesh datastructure, a network, and a volumetric or cellular mesh.
.. * :mod:`compas.files`: provides support for file types related to geometry definition, manufacturing processes, CAD interoperability, ...
.. * :mod:`compas.geometry`: is a geometry processing library.
.. * :mod:`compas.hpc`: is a high-performance computing library, which provides GPU-accelerated or JIT-compiled versions of many geometry, numerical and topological functions and algorithms.
.. * :mod:`compas.interop`: includes utility functions for seamless integration of C and C++ code, and wrappers for external libraries.
.. * :mod:`compas.numerical`: implements numerical solvers and methods for form finding and analysis of structures.
.. * :mod:`compas.plotters`: wraps the Matplotlib plotting library to create a two-dimensional visualization toolbox geared towards the datastructures, dynamic visualization of algorithm progress, and simple user interaction.
.. * :mod:`compas.topology`: implements ...
.. * :mod:`compas.utilities`: provides a wide range of, well, utility functions.
.. * :mod:`compas.viewers`: wraps PyOpenGL and PySide to provide three-dimensional viewers with basic visualization and user interaction capabilities.


Helpers
-------
  
* :mod:`compas.com`: communication with external software
* :mod:`compas.files`: handlers for file formats related to geometry definition, cad interoperability, manufacturing
* :mod:`compas.interop`: interoperability with C/C++ code and libraries
* :mod:`compas.utilities`: other useful things


Datastructures
--------------
  
* :mod:`compas.datastructures`: mesh (half-edge), network (graph), volmesh (half-plane)


Algorithms
----------
  
* :mod:`compas.geometry`: geometry processing
* :mod:`compas.numerical`: numerical methods, solvers, ...
* :mod:`compas.topology`: combinatorics, traversal, subdivision, ...


Visualisation
-------------

* :mod:`compas.plotters`: 2D visualisation, dynamic plots, basic interaction
* :mod:`compas.viewers`: basic 3D visualisation


CAD integration
===============

The core functionality of **compas** is implemented independent of the functionality
provided by CAD software. This ensures that research based on **compas** is not tied
to a specific tool chain en can be used more flexibly in different environments
and on different platforms. 

However, in the context of this framework CAD tools are obviously indispensible
tools to construct and manipulate geometry, apply constraints interactively, make
user interfaces, or even just to use as viewer for running scripts. The CAD helper
packages (:mod:`compas_blender`, :mod:`compas_maya`, :mod:`compas_rhino`) provide
a unified and consistent interface to CAD tools and their ecosystems.

* **compas_x.artists**: visualization of datastructures
* **compas_x.forms**: *not available yet*
* **compas_x.geometry**: wrappers for native geometry objects
* **compas_x.helpers**: select, modify, inspect datastructures
* **compas_x.ui**: rui builder, ui elements, mouse events
* **compas_x.utilities**: other useful stuff

