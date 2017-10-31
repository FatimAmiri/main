# get vertex key for a vertex on the x-z-plane
for key in network.vertices():
    # do something here

# remove x-z-plane vertex key from fixed
# do something here


# in the callback function :
# ...
if k % step == 0:
    rs.Prompt("Iteration: {0}".format(k))
    network_draw_edges(network)

# constrain y-coordinate to 0.0 for vertex with specific key
# do something here