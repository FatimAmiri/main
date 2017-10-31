from __future__ import print_function

import os

import compas
import compas_rhino

from compas.datastructures import Network
from compas_rhino.ui import MacroController
from compas.geometry import network_relax
from compas_rhino.conduits import LinesConduit


HERE = os.path.abspath(os.path.dirname(__file__))


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
            'rz': 0.0
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
            'scale.reaction_forces': 0.1,
            'scale.loads': 1.0,
            'scale.axial_forces': 0.01
        }
        self.network = None
        self._conduit = LinesConduit([])

    def _draw(self):
        compas_rhino.network_draw(
            self.network,
            layer='FormFinder::Network',
            clear_layer=True,
            vertexcolor={key: (255, 0, 0) for key in self.network.vertices_where({'is_fixed': True})}
        )
        compas_rhino.network_draw_reaction_forces(
            self.network,
            self.settings['scale.reaction_forces'],
            layer='FormFinder::Network'
        )
        compas_rhino.network_draw_loads(
            self.network,
            self.settings['scale.loads'],
            layer='FormFinder::Network'
        )
        compas_rhino.network_draw_axial_forces(
            self.network,
            self.settings['scale.axial_forces'],
            layer='FormFinder::Network'
        )

    def _callback(self, k, args):
        self._conduit.lines = [self.network.edge_coordinates(u, v) for u, v in self.network.edges()]
        self._conduit.redraw(k)

    def init(self):
        compas_rhino.create_layers_from_paths(self.layers)
        compas_rhino.clear_layers(self.layers)

    def update_settings(self):
        if compas_rhino.update_settings(self.settings):
            self._draw()

    def from_obj(self):
        file = compas_rhino.browse_for_file(folder=HERE, filter='OBJ files (*.obj)|*.obj')
        if file:
            self.network = Cablenet.from_obj(file)
            self.network.fix_leaves()
            self._draw()

    def from_lines(self):
        guids = compas_rhino.select_lines()
        lines = compas_rhino.get_line_coordinates(guids)
        self.network = Cablenet.from_lines(lines)
        self.network.fix_leaves()
        self._draw()

    def update_vertex_attributes(self):
        keys = compas_rhino.network_select_vertices(self.network)
        if keys:
            if compas_rhino.network_update_vertex_attributes(self.network, keys):
                self._draw()

    def update_edge_attributes(self):
        keys = compas_rhino.network_select_edges(self.network)
        if keys:
            if compas_rhino.network_update_edge_attributes(self.network, keys):
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
