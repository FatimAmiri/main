plotter = NetworkPlotter(network, figsize=(16, 9))
plotter.draw_vertices(
    facecolor={key: '#ff0000' for key in network.vertices_where({'vertex_degree': 1})},
    text={key: str(key) for key in network.vertices_where({'vertex_degree': 4})},
    radius={key: 0.3 for key in network.vertices_where({'vertex_degree': 4})}
)
plotter.draw_edges()
plotter.show()