# use:
from compas.datastructures import Mesh
from compas_rhino import mesh_draw_faces
trans_mesh = Mesh()

# add vertices to mesh object
for u in xrange(len(pts_uv)):
    for v in xrange(len(pts_uv[u])):
        x, y, z = pts_uv[u][v]

        # do something here:
        # trans_mesh.add_vertex(...)

# add faces to mesh object
for u in xrange(len(pts_uv)-1):
    for v in xrange(len(pts_uv[u])-1):

        # do something here
        # trans_mesh.add_face(...)

mesh_draw_faces(trans_mesh)

for u, v in trans_mesh.edges():
    # do something here