.. _acadia2017_day2_formfinding:

********************************************************************************
Form Finding
********************************************************************************

Compute equilibrium geometry of a network (cablenet) with DR
============================================================

.. plot::

    import random

    import compas
    from compas.datastructures import Network
    from compas.visualization import NetworkPlotter
    from compas.geometry import network_relax
    from compas.utilities import i_to_rgb

    network = Network.from_obj(compas.get('lines.obj'))

    dva = {
        'is_fixed': False,
        'px': 0.0,
        'py': 0.0,
        'pz': 0.0,
    }
    dea = {
        'q': 1.0,
        'f': 0.0,
        'l': 0.0
    }

    network.update_default_vertex_attributes(dva)
    network.update_default_edge_attributes(dea)

    for key, attr in network.vertices(True):
        attr['is_fixed'] = network.is_vertex_leaf(key)

    for index, (u, v, attr) in enumerate(network.edges(True)):
        attr['q'] = 1.0 * random.randint(1, 7)

    plotter = NetworkPlotter(network, figsize=(10, 7))

    lines = []
    for u, v in network.edges():
        lines.append({
            'start' : network.vertex_coordinates(u, 'xy'),
            'end'   : network.vertex_coordinates(v, 'xy'),
            'color' : '#cccccc',
            'width' : 0.5
        })

    plotter.draw_lines(lines)

    network_relax(network, kmax=50)

    fmax = max(network.get_edges_attribute('f'))

    plotter.draw_vertices(
        facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})}
    )

    plotter.draw_edges(
        color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in network.edges(True)},
        width={(u, v): 10 * attr['f'] / fmax for u, v, attr in network.edges(True)}
    )

    plotter.show()


.. seealso::

    * :class:`compas.datastructures.Network`
    * :class:`compas.geometry.network_relax`
    * :class:`compas.visualization.NetworkPlotter`
    * :class:`compas.numerical.dr`


.. code-block:: python

    # Pure Python dynamic relaxation method
    #
    # - create a network (for example from a sample *.obj)
    # - fix the *anchored* vertices
    # - set the force densities of the edges
    # - run it through the network relaxation method
    # - visualize the result
    #

    import random

    import compas
    from compas.datastructures import Network
    from compas.visualization import NetworkPlotter
    from compas.utilities import i_to_rgb

    # create a network from sample data
    # and set the default vertex and edge attributes

    network = Network.from_obj(compas.get('lines.obj'))

    dva = {
        'is_fixed': False,
        'px': 0.0,
        'py': 0.0,
        'pz': 0.0,
    }
    dea = {
        'q': 1.0,
        'f': 0.0,
        'l': 0.0
    }

    network.update_default_vertex_attributes(dva)
    network.update_default_edge_attributes(dea)

    # fix the vertices with only one neighbour (the *leaves*)
    # assign random force densities to the edges

    for key, attr in network.vertices(True):
        attr['is_fixed'] = network.is_vertex_leaf(key)

    for index, (u, v, attr) in enumerate(network.edges(True)):
        attr['q'] = 1.0 * random.randint(1, 7)

    # make a plotter
    # draw the original geometry of the network as lines
    # draw the vertices and edges
    # pause for a second before starting the relaxation

    plotter = NetworkPlotter(network, figsize=(10, 7))

    lines = []
    for u, v in network.edges():
        lines.append({
            'start' : network.vertex_coordinates(u, 'xy'),
            'end'   : network.vertex_coordinates(v, 'xy'),
            'color' : '#cccccc',
            'width' : 0.5
        })

    plotter.draw_lines(lines)
    plotter.draw_vertices(facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})})
    plotter.draw_edges()

    plotter.update(pause=1.0)

    # define a callback function for updating the plot
    # and for printing the number of the current iteration

    def callback(k, args):
        print(k)
        plotter.update_vertices()
        plotter.update_edges()
        plotter.update(pause=0.001)

    # run the relaxation algorithm

    network_relax(network, kmax=50, callback=callback)

    # compute the maximum force in the edges
    # for normalising colors and widths

    fmax = max(network.get_edges_attribute('f'))

    # clear the vertices and edges
    # that were used for visualising the iterations

    plotter.clear_vertices()
    plotter.clear_edges()

    # draw the final geometry
    # with color and width of the edges corresponding to the internal forces

    plotter.draw_vertices(
        facecolor={key: '#000000' for key in network.vertices_where({'is_fixed': True})}
    )

    plotter.draw_edges(
        color={(u, v): i_to_rgb(attr['f'] / fmax) for u, v, attr in network.edges(True)},
        width={(u, v): 10 * attr['f'] / fmax for u, v, attr in network.edges(True)}
    )

    # update the plot

    plotter.update()
    plotter.show()


Make a custom class
===================

.. code-block:: python

    class Cablenet(Network):

        def __init__(self):
            super(Cablenet, self).__init__()
            self.default_vertex_attributes.update({
                'is_fixed': False,
                'px': 0.0,
                'py': 0.0,
                'pz': 0.0,
                'rx': 0.0,
                'ry': 0.0,
                'rz': 0.0,
            })
            self.default_edge_attributes.update({
                'q': 1.0,
                'f': 0.0,
                'l': 0.0
            })

        def fix_leaves(self):
            for key, attr in self.vertices(True):
                attr['is_fixed'] = self.vertex_degree(key) == 1


    network = Cablenet.from_obj(compas.get('lines.obj'))

    network.fix_leaves()


Use Rhino as interface
======================

.. figure:: /_images/fofin-rhino.*
    :figclass: figure
    :class: figure-img img-fluid

.. code-block:: python
    
    import compas
    import compas_rhino

    from compas.datastructures import Network
    from compas.geometry import network_relax
    from compas_rhino.conduits import LinesConduit

    class Cablenet(Network):

        def __init__(self):
            super(Cablenet, self).__init__()
            self.default_vertex_attributes.update({
                'is_fixed': False,
                'px': 0.0,
                'py': 0.0,
                'pz': 0.0,
                'rx': 0.0,
                'ry': 0.0,
                'rz': 0.0,
            })
            self.default_edge_attributes.update({
                'q': 1.0,
                'f': 0.0,
                'l': 0.0
            })

        def fix_leaves(self):
            for key, attr in self.vertices(True):
                attr['is_fixed'] = self.vertex_degree(key) == 1


    network = Cablenet.from_obj(compas.get('saddle.obj'))
    network.fix_leaves()

    compas_rhino.network_draw(
        network,
        layer='FoFin',
        clear_layer=True,
        vertexcolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})}
    )

    network_relax(network, kmax=100)

    compas_rhino.network_draw(
        network,
        layer='FoFin',
        clear_layer=True,
        vertexcolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})}
    )


**Next Steps**


* Use a conduit and a callback to visualize the relaxation process.

.. code-block:: python

    lines = [network.edge_coordinates(u, v) for u, v in network.edges()]
    conduit = LinesConduit(lines)

    def callback(k, args):
        print(k)
        conduit.lines = [[network.vertex_coordinates(u), network.vertex_coordinates(v)] for u, v in network.edges()]
        conduit.redraw(k)

    with conduit.enabled():
        network_relax(network, kmax=100, callback=callback)


* Visualize the reaction forces, loads, and axial forces in the network.

.. code-block:: python

    compas_rhino.network_draw_reaction_forces(
        network,
        0.5,
        layer='FoFin'
    )
    compas_rhino.network_draw_loads(
        network,
        1.0,
        layer='FoFin'
    )
    compas_rhino.network_draw_axial_forces(
        network,
        0.01,
        layer='FoFin'
    )


Add user interaction
====================

* Update vertex attributes to add loads and change geometry.

.. code-block:: python
    
    # update the vertex attributes

    while True:
        keys = compas_rhino.network_select_vertices(network)
        if not keys:
            break
        compas_rhino.network_update_vertex_attributes(network, keys)
        compas_rhino.network_draw(
            network,
            layer='FoFin',
            clear_layer=True,
            vertexcolor={key: '#ff0000' for key in network.vertices_where({'is_fixed': True})}
        )

* Update edge attributes to change force densities and control the equilibrium shape.

    # update the edge attributes

    while True:
        pass


**Optional**

* Use a :obj:`functools.partial` to create a shortcut to the draw function with
  fixed options already filled in.

.. code-block:: python

    from functools import partial


Start from Rhino geometry
=========================

* Draw/Generate a set of lines representing the topology of the network.
* Initialise vertex and edge attributes based on geometry object names.


.. code-block:: python

    guids = compas_rhino.get_lines()
    lines = compas_rhino.get_line_coordinates(guids)

    network = Network.from_lines(lines)


Use a toolbar to make a form finding tool
=========================================

* Understand variable scope in toolbars.
* Link functionality to toolbar buttons by using a controller.
* Generate a RUI file from the controller.
* Let Rhino know where your code is.


.. code-block:: python

    from __future__ import print_function

    import compas
    import compas_rhino

    from compas.datastructures import Network
    from compas_rhino.ui import MacroController
    from compas.geometry import network_relax
    from compas_rhino.conduits import LinesConduit


    class Cablenet(Network):

        def __init__(self):
            super(Cablenet, self).__init__()
            self.default_vertex_attributes.update({
                'is_fixed': False,
                'px': 0.0,
                'py': 0.0,
                'pz': 0.0,
            })
            self.default_edge_attributes.update({
                'q': 1.0,
                'f': 0.0,
                'l': 0.0
            })

        def fix_leaves(self):
            for key, attr in self.vertices(True):
                attr['is_fixed'] = self.vertex_degree(key) == 1


    class FormFinder(MacroController):

        instancename = 'formfinder'
        name = 'FormFinder'

        def __init__(self):
            super(FormFinder, self).__init__()
            self.layers = [
                'FormFinder::Network',
            ]
            self.settings = {
                'kmax': 100,
            }
            self.network = None
            self._conduit = LinesConduit([])

        def _draw(self):
            compas_rhino.network_draw(
                self.network,
                layer='FormFinder::Network',
                clear_layer=True,
                vertexcolor={key: (255, 0, 0) for key in self.network.vertices_where({'is_fixed': True})})

        def _callback(self, k, args):
            self._conduit.lines = [self.network.edge_coordinates(u, v) for u, v in self.network.edges()]
            self._conduit.redraw(k)

        def init(self):
            compas_rhino.create_layers_from_paths(self.layers)
            compas_rhino.clear_layers(self.layers)

        def update_settings(self):
            if compas_rhino.update_settings(self.settings):
                pass

        def from_obj(self):
            file = compas_rhino.browse_for_file(folder=HERE, filter='OBJ files (*.obj)|*.obj')
            if file:
                self.network = Cablenet.from_obj(file)
                self.network.fix_leaves()
                self._draw()

        def relax(self):
            with self._conduit.enabled():
                network_relax(self.network, kmax=self.settings['kmax'], callback=self._callback)
            self._draw()


    # ==============================================================================
    # Debugging
    # ==============================================================================

    if __name__ == "__main__":

        from compas_rhino.ui.rui import compile_rui

        compile_rui(FormFinder, 'fofin_controller', 'fofin_config.json')


.. code-block:: none

    # fofin_config.json
    
    {
        "menus": [],
        "toolbars": [
            {
                "name"  : "FormFinder", 
                "items" : [
                    {
                        "type"        : "normal",
                        "left_macro"  : "formfinder.init",
                        "right_macro" : null
                    },
                    {
                        "type" : "separator"
                    },
                    {
                        "type"        : "normal",
                        "left_macro"  : "formfinder.update_settings",
                        "right_macro" : null
                    }
                ]
            },
            {
                "name"  : "FormFinder.Network", 
                "items" : [
                    {
                        "type"        : "normal",
                        "left_macro"  : "formfinder.from_obj",
                        "right_macro" : null
                    }
                ]
            },
            {
                "name"  : "FormFinder.Solvers", 
                "items" : [
                    {
                        "type"        : "normal",
                        "left_macro"  : "formfinder.relax",
                        "right_macro" : null
                    }
                ]
            }
        ],
        "toolbargroups": [
            {
                "name"     : "FormFinder",
                "toolbars" : [
                    "FormFinder",
                    "FormFinder.Network",
                    "FormFinder.Solvers"
                ]
            }
        ]
    }


**Next steps**

* Add ``from_lines`` method.
* Add ``update_vertex_attributes`` method.
* Add ``update_edge_attributes`` method.


.. note::

    * :download:`fofin_controller.py </../../examples/workshops/acadia2017/fofin_controller.py>`
    * :download:`fofin_config.json </../../examples/workshops/acadia2017/fofin_config.json>`
